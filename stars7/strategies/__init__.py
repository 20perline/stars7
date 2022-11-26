from itertools import combinations
from stars7.coordinate import Coordinate
from stars7.rectangle import Rectangle
from stars7.round import Round
from stars7.feed import Feed
from stars7.pattern import Pattern
from stars7 import settings
from stars7 import utils
from loguru import logger
from abc import abstractmethod, ABCMeta
from typing import List, Iterator, Sequence, Tuple


class Strategy(metaclass=ABCMeta):
    """策略基类"""

    _logger = logger

    @staticmethod
    def set_logger(logger_):
        Strategy._logger = logger_

    def __init__(self,
                 offset: Sequence[int],
                 elements: Sequence[int],
                 rect_rows: Sequence[int],
                 works_at_least: int = 2
                 ) -> None:
        self.offset = offset
        self.elements = elements
        self.rect_rows = rect_rows
        self.works_at_least = works_at_least
        self.max_execute_round = 10
        self.key_col_names = settings.KEY_COL_NAMES
        self.found_signatures = set()

    def get_name(self):
        return self.__class__.__name__.replace('Strategy', '')

    @abstractmethod
    def predict(self, predict_index: int, round_list: List[Round]) -> int:
        pass

    @abstractmethod
    def next_round_coord(self, rect: Rectangle, points: Tuple[int], round_num: int) -> List[Coordinate]:
        pass

    @abstractmethod
    def execute_for_points(self, rect: Rectangle, points: Tuple[int], feed: Feed) -> List[Round]:
        pass

    def execute(self, feed: Feed) -> Iterator[Pattern]:
        for offset in self.offset:
            if offset < 0:
                continue
            for rows in self.rect_rows:
                rect = Rectangle(offset=offset, rows=rows)
                for pattern in self._execute(rect, feed):
                    yield pattern

    def points_generator(self, rect: Rectangle):
        total_idx = rect.rows * rect.cols
        for elements in self.elements:
            for points in combinations(range(total_idx), elements):
                yield points

    def get_signature(self, offset, zero_round_coords: List[Coordinate]):
        list1 = []
        for coord in zero_round_coords:
            list1.append(str(coord.row).replace('-', 'N') + coord.col)
        return self.get_name() + 'O' + str(offset) + (''.join(list1)).upper()

    def _execute(self, rect: Rectangle, feed: Feed):
        offset = rect.offset
        name = self.get_name()
        next_num = feed.next_num
        for points in self.points_generator(rect):
            # duplicate filter
            zero_round_coords = self.next_round_coord(rect, points, 0)
            signature = self.get_signature(offset, zero_round_coords)
            if signature not in self.found_signatures:
                self.found_signatures.add(signature)
            else:
                continue

            round_list = self.execute_for_points(rect, points, feed)
            if round_list is None:
                continue

            # make sure there's only one position in prediction row
            if len([c.row for c in zero_round_coords if c.row < -1]) > 0:
                predictable = False
            elif len([c.row for c in zero_round_coords if c.row == -1]) == 1:
                predictable = True
            else:
                predictable = False

            if not predictable:
                continue

            prediction_success = False

            predict_index = [i for i, c in enumerate(zero_round_coords) if c.row == -1][0]
            predict_col_name = zero_round_coords[predict_index].col
            if predict_col_name not in self.key_col_names:
                continue
            zero_round_values = feed.get_values(zero_round_coords)
            round_list.insert(0, Round(round_num=0, coordinates=zero_round_coords, offset=offset, values=zero_round_values))
            predict_value = self.predict(predict_index, round_list)
            if predict_value is None:
                continue
            self._logger.debug(
                "[{num}] {signature} rounds: \n{rounds}",
                num=next_num, signature=signature, rounds=utils.list_to_str(reversed(round_list), join_str="\n"))

            round_list[0].values[predict_index] = predict_value
            actual_value = feed.get_next_value_at(predict_col_name)
            prediction_mask = ''.join(['*' if c != predict_col_name else str(predict_value) for c in self.key_col_names])
            self._logger.info(
                '[{num}] {signature} predict value: {mask}, actual value: {av}',
                num=next_num, signature=signature, mask=prediction_mask, av=actual_value)

            if actual_value == predict_value:
                prediction_success = True

            yield Pattern(signature=signature, strategy=name, predict_success=prediction_success,
                          prediction_num=next_num, prediction_mask=prediction_mask, rect=rect,
                          round_list=round_list, winning_ticket=feed.winning_ticket)


class AssociatedRoundsStrategy(Strategy, metaclass=ABCMeta):
    """Rounds之间有关系的"""

    def __init__(self,
                 offset: Sequence[int] = range(4),
                 elements: Sequence[int] = range(1, 5),
                 rect_rows: Sequence[int] = range(1, 5),
                 works_at_least: int = 2,
                 column_offset: int = 0) -> None:
        super().__init__(offset=offset, elements=elements, rect_rows=rect_rows, works_at_least=works_at_least)
        # 是否跟随偏移纵轴
        self.column_offset = column_offset
        self.max_execute_round = 10

    def next_round_coord(self, rect: Rectangle, points: Tuple[int], round_num: int) -> List[Coordinate]:
        rect_cols = rect.cols
        coord = []
        for point in points:
            row = rect.offset + rect.rows * (round_num - 1) + point // rect_cols
            col = rect.start_col + point % rect_cols + self.column_offset * (round_num - 1)
            if col < rect.start_col or col > rect.start_col + rect.cols:
                break
            coord.append(Coordinate(row=row, col='c{}'.format(col)))
        return coord

    def execute_for_points(self, rect: Rectangle, points: Tuple[int], feed: Feed) -> List[Round]:
        offset = rect.offset
        round_list = []
        for round_num in range(1, self.max_execute_round + 1):
            coord_list = []
            for coord in self.next_round_coord(rect, points, round_num=round_num):
                coord_list.append(coord)
            if len(coord_list) != len(points):
                break
            values = feed.get_values(coord_list)
            round = Round(round_num=round_num, coordinates=coord_list, offset=offset, values=values)
            round_list.append(round)

        if len(round_list) < self.works_at_least:
            return None
        works_cnt = self.verify(round_list=round_list)
        if works_cnt >= self.works_at_least:
            self._logger.trace(
                "found {strategy} works for {works_cnt} times: \n{round_list}",
                strategy=self.get_name(),
                works_cnt=works_cnt,
                round_list=utils.list_to_str(round_list[:works_cnt], join_str="\n"))
            return round_list[:works_cnt]

    @abstractmethod
    def verify(self, round_list: List[Round]):
        pass
