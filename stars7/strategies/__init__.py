from itertools import combinations
from stars7.coordinate import Coordinate
from stars7.rectangle import Rectangle
from stars7.render import Render
from stars7.round import Round
from stars7.feed import Feed
from stars7 import utils
from abc import abstractmethod, ABCMeta
from typing import List


class Strategy(metaclass=ABCMeta):

    def __init__(self, rect: Rectangle, offset=0, elements=1, works_at_least=2) -> None:
        if offset < 0:
            raise Exception('offset can not be less than 0')
        self.rect = rect
        self.offset = offset
        self.elements = elements
        self.works_at_least = works_at_least
        self.max_execute_round = 10

    def get_name(self):
        return self.__class__.__name__

    def points_generator(self):
        rect_rows = self.rect.rows
        rect_cols = self.rect.cols
        total_idx = rect_rows * rect_cols
        for points in combinations(range(total_idx), self.elements):
            yield points

    @abstractmethod
    def next_round_coord(self, rect_indexes, round_num) -> List[Coordinate]:
        pass

    def execute(self, feed: Feed):
        name = self.get_name()
        print(name, ' started')
        render = Render(feed)
        for points in self.points_generator():
            round_list = self.execute_for_points(feed, points)
            if round_list is not None:
                render.save(round_list=round_list)
        print(name, ' stopped')

    @abstractmethod
    def execute_for_points(self, feed: Feed, points):
        pass


class SingleRoundStrategy(Strategy, metaclass=ABCMeta):

    def __init__(self, rect: Rectangle, offset=0, pos=1, elements=1, works_at_least=2) -> None:
        self.rect = rect
        self.offset = offset
        self.pos = pos
        self.elements = elements
        self.works_at_least = works_at_least
        self.max_execute_round = 10

    def next_round_pos(self, round_num) -> Coordinate:
        return Coordinate(row=self.offset + self.rect.rows * (round_num - 1), col='c{}'.format(self.pos))

    def next_round_coord(self, points, round_num) -> List[Coordinate]:
        rect_cols = self.rect.cols
        coord = []
        for point in points:
            row = self.offset + self.rect.rows * (round_num - 1) + 1 + point // rect_cols
            col = self.rect.start_col + point % rect_cols
            coord.append(Coordinate(row=row, col='c{}'.format(col)))
        return coord

    def execute_for_points(self, feed: Feed, points):
        round_idx = 0
        round_list = []
        for round_num in range(1, self.max_execute_round):
            coord_list = []
            pos_coord = self.next_round_pos(round_num=round_num)
            coord_list.append(pos_coord)
            for coord in self.next_round_coord(points, round_num=round_num):
                coord_list.append(coord)
            if len(coord_list) == 1:
                break
            values = feed.get_values(coord_list)
            round = Round(round_num=round_num, coordinates=coord_list, values=values)
            res = self.verify(round=round)
            if not res:
                break
            else:
                round_list.append(round)
            round_idx = round_num

        if round_idx >= self.works_at_least:
            print('found pattern: ', utils.list_to_str(round_list))
            return round_list

    @abstractmethod
    def verify(self, round: Round):
        pass


class MultiRoundsStrategy(Strategy, metaclass=ABCMeta):

    def __init__(self, rect: Rectangle, column_offset=0, offset=0, elements=1, works_at_least=2) -> None:
        self.rect = rect
        self.offset = offset
        # 是否跟随偏移纵轴
        self.column_offset = column_offset
        self.elements = elements
        self.works_at_least = works_at_least
        self.max_execute_round = 10

    def next_round_coord(self, points, round_num) -> List[Coordinate]:
        rect_cols = self.rect.cols
        coord = []
        for point in points:
            row = self.offset + self.rect.rows * (round_num - 1) + point // rect_cols
            col = self.rect.start_col + point % rect_cols + self.column_offset * (round_num - 1)
            if col < self.rect.start_col or col > self.rect.start_col + self.rect.cols:
                break
            coord.append(Coordinate(row=row, col='c{}'.format(col)))
        return coord

    def execute_for_points(self, feed: Feed, points):
        round_list = []
        for round_num in range(1, self.max_execute_round + 1):
            coord_list = []
            for coord in self.next_round_coord(points, round_num=round_num):
                coord_list.append(coord)
            if len(coord_list) != self.elements:
                break
            values = feed.get_values(coord_list)
            round = Round(round_num=round_num, coordinates=coord_list, values=values)
            round_list.append(round)

        if len(round_list) < self.works_at_least:
            return None
        works_cnt = self.verify(round_list=round_list)
        if works_cnt >= self.works_at_least:
            print('found pattern works for', works_cnt, 'rounds: ', utils.list_to_str(round_list))
            return round_list[:works_cnt]

    @abstractmethod
    def verify(self, round: Round):
        pass
