
class Coordinate(object):

    def __init__(self, row: int, col: int) -> None:
        self.row = row
        self.col = col

    def __str__(self):
        return "[%s %s]" % (self.row, self.col)
