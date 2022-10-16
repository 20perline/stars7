from stars7.coordinate import Coordinate
from stars7 import utils
from typing import List


class Round(object):

    def __init__(self, round_num: int, coordinates: List[Coordinate], values: List[int], last_values=None) -> None:
        self.round_num = round_num
        self.coordinates = coordinates
        self.values = values
        self.last_values = last_values

    def __str__(self):
        return "Round(num=%s, coordinates=%s, values=%s)" % (self.round_num, utils.list_to_str(self.coordinates), self.values)
