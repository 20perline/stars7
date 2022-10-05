from stars7 import utils


class Round(object):

    def __init__(self, round_num, coordinates, values, last_values=None) -> None:
        self.round_num = round_num
        self.coordinates = coordinates
        self.values = values
        self.last_values = last_values

    def __str__(self):
        return "Round(num=%s, coordinates=%s, values=%s)" % (self.round_num, utils.list_to_str(self.coordinates), self.values)
