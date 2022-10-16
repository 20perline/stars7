from itertools import combinations
from stars7.coordinate import Coordinate
from stars7.rectangle import Rectangle
from stars7.round import Round
from stars7.feed import Feed
from stars7.pattern import Pattern
from stars7 import utils
from loguru import logger
from abc import abstractmethod, ABCMeta
from typing import List, Iterator, Sequence
from collections import defaultdict


class Strategy(metaclass=ABCMeta):
    def __init__(self,
                 rect: Rectangle,
                 offset: Sequence[int],
                 elements: Sequence[int],
                 works_at_least=2
                 ) -> None:
        self.rect = rect
        self.offset = offset
        self.elements = elements
        self.works_at_least = works_at_least
        self.max_execute_round = 10
        self.pattern_counter = defaultdict(int)

    def get_name(self):
        return self.__class__.__name__

    @abstractmethod
    def predict(self, predict_index: int, round_list: List[Round]):
        pass

    @abstractmethod
    def next_round_coord(self, offset, points, round_num) -> List[Coordinate]:
        pass

    @abstractmethod
    def execute_for_points(self, offset, points, feed: Feed) -> List[Round]:
        pass

    def execute(self, feed: Feed) -> Iterator[Pattern]:
        for offset in self.offset:
            if offset < 0:
                continue
            for pattern in self._execute_for_offset(offset, feed):
                yield pattern

    def points_generator(self):
        rect_rows = self.rect.rows
        rect_cols = self.rect.cols
        total_idx = rect_rows * rect_cols
        for elements in self.elements:
            for points in combinations(range(total_idx), elements):
                yield points

    def _execute_for_offset(self, offset, feed: Feed):
        for points in self.points_generator():
            round_list = self.execute_for_points(offset, points, feed)
            if round_list is None:
                continue
            zero_round_coords = [Coordinate(row=coord.row - self.rect.rows, col=coord.col) for coord in round_list[0].coordinates]

            # make sure there's only one position in prediction row
            if len([c.row for c in zero_round_coords if c.row < -1]) > 0:
                predictable = False
            elif len([c.row for c in zero_round_coords if c.row == -1]) == 1:
                predictable = True
            else:
                predictable = False

            predict_index = None
            predict_success = False
            if predictable:
                predict_index = [i for i, c in enumerate(zero_round_coords) if c.row == -1][0]
                zero_round_values = feed.get_values(zero_round_coords)
                round_list.insert(0, Round(round_num=0, coordinates=zero_round_coords, offset=offset, values=zero_round_values))
                self.predict(predict_index, round_list)
                predict_value = round_list[0].values[predict_index]
                actual_value = feed.get_next_value_at(predict_index)
                logger.debug("predict value {val1}, actual value {val2} compare {res}", val1=predict_value, val2=actual_value, res=(actual_value == predict_value))
                if actual_value is not None and actual_value == predict_value:
                    predict_success = True

            name = '{}-E{}O{}-R{}C{}'.format(self.get_name(), len(points), offset, self.rect.rows, self.rect.cols)
            signature = '{}-P{}'.format(name, utils.list_to_str(points, join_str=''))
            self.pattern_counter[name] += 1
            yield Pattern(index=self.pattern_counter[name],
                          name=name,
                          signature=signature,
                          predictable=predictable,
                          predict_success=predict_success,
                          round_list=round_list)


class AssociatedRoundsStrategy(Strategy, metaclass=ABCMeta):
    """Rounds之间有关系的"""

    def __init__(self,
                 rect: Rectangle,
                 offset,
                 elements,
                 column_offset: int = 0,
                 works_at_least=2) -> None:
        super().__init__(rect=rect, offset=offset, elements=elements, works_at_least=works_at_least)
        # 是否跟随偏移纵轴
        self.column_offset = column_offset
        self.max_execute_round = 10

    def next_round_coord(self, offset, points, round_num) -> List[Coordinate]:
        rect_cols = self.rect.cols
        coord = []
        for point in points:
            row = offset + self.rect.rows * (round_num - 1) + point // rect_cols
            col = self.rect.start_col + point % rect_cols + self.column_offset * (round_num - 1)
            if col < self.rect.start_col or col > self.rect.start_col + self.rect.cols:
                break
            coord.append(Coordinate(row=row, col='c{}'.format(col)))
        return coord

    def execute_for_points(self, offset, points, feed: Feed):
        round_list = []
        for round_num in range(1, self.max_execute_round + 1):
            coord_list = []
            for coord in self.next_round_coord(offset, points, round_num=round_num):
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
            logger.trace(
                "found {strategy} works for {works_cnt} times: \n{round_list}",
                strategy=self.get_name(),
                works_cnt=works_cnt,
                round_list=utils.list_to_str(round_list[:works_cnt], join_str="\n"))
            return round_list[:works_cnt]

    @abstractmethod
    def verify(self, round_list: List[Round]):
        pass
