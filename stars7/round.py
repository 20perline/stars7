from stars7.coordinate import Coordinate
from stars7 import utils
from typing import List


class Round(object):

    def __init__(self, round_num: int, coordinates: List[Coordinate], values: List[int], offset: int) -> None:
        self.round_num = round_num
        self.coordinates = coordinates
        self.values = values
        self.offset = offset

    def __str__(self):
        return "Round(num=%s, coordinates=%s, values=%s, ↑offset=%s)" % (self.round_num, utils.list_to_str(self.coordinates), self.values, self.offset)
