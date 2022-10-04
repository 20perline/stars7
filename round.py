
class Round(object):

    def __init__(self, round_num, coordinates, values, last_values=None) -> None:
        self.round_num = round_num
        self.coordinates = coordinates
        self.values = values
        self.last_values = last_values
