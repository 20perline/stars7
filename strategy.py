from itertools import combinations
from coordinate import Coordinate
from rectangle import Rectangle
from round import Round
from typing import List


class Strategy(object):

    def __init__(self, rect: Rectangle, offset=0, pos=1, elements=1, works_at_least=2) -> None:
        self.rect = rect
        self.offset = offset
        self.pos = pos
        self.elements = elements
        self.works_at_least = works_at_least

    def indexes_generator(self):
        rect_rows = self.rect.rows
        rect_cols = self.rect.cols
        total_idx = rect_rows * rect_cols
        for points in combinations(range(total_idx), self.elements):
            yield points

    def next_round_pos(self, round_num) -> Coordinate:
        return Coordinate(row=self.offset + self.rect.rows * (round_num - 1), col='c{}'.format(self.pos))

    def next_round_coord(self, rect_indexes, round_num) -> List[Coordinate]:
        rect_cols = self.rect.cols
        coord = []
        for point in rect_indexes:
            row = self.offset + self.rect.rows * (round_num - 1) + 1 + point // rect_cols
            col = self.rect.start_col + point % rect_cols
            coord.append(Coordinate(row=row, col='c{}'.format(col)))
        return coord

    def verify(self, round: Round):
        return False

    def __str__(self):
        return "offset=%s, rect=%s, pos=%s, elements=%s" % (self.offset, self.rect, self.pos, self.elements)


class SimpleStrategy(Strategy):
    "相同单个位置上值相同"""

    def verify(self, round: Round):
        if round is None:
            return False
        values = round.values
        return values[0] == values[1]


class EqSiblingsStrategy(Strategy):
    """某两个位置值相同"""

    def verify(self, round: Round):
        if round is None:
            return False
        values = round.values
        return values[-2] == values[-1]


class SlashStrategy(Strategy):
    """一条斜线上值相同"""

    def next_round_coord(self, rect_indexes, round_num) -> List[Coordinate]:
        rect_cols = self.rect.cols
        coord = []
        for point in rect_indexes:
            row = self.offset + self.rect.rows * (round_num - 1) + 1 + point // rect_cols
            col = self.rect.start_col + point % rect_cols - 1 * round_num
            if col >= self.rect.start_col:
                coord.append(Coordinate(row=row, col='c{}'.format(col)))
        return coord

    def verify(self, round: Round):
        if round is None:
            return False
        values = round.values
        last_values = round.last_values
        if last_values is None:
            return True
        for i in range(1, self.elements + 1):
            if values[i] != last_values[i]:
                return False
        return True


class BackSlashStrategy(SlashStrategy):
    """一条反向斜线上值相同"""

    def next_round_coord(self, rect_indexes, round_num) -> List[Coordinate]:
        rect_cols = self.rect.cols
        coord = []
        for point in rect_indexes:
            row = self.offset + self.rect.rows * (round_num - 1) + 1 + point // rect_cols
            col = self.rect.start_col + point % rect_cols + 1 * round_num
            if col <= self.rect.start_col + rect_cols:
                coord.append(Coordinate(row=row, col='c{}'.format(col)))
        return coord


if __name__ == '__main__':
    a = Strategy(rect=Rectangle())
    coord = a.next_round_pos(2)
    print(coord)
    for i in a.indexes_generator():
        for c in a.next_round_coord(i, 2):
            print(i, c)
