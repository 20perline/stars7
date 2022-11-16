
class Coordinate(object):

    def __init__(self, row: int, col: str) -> None:
        self.row = row
        self.col = col

    def __str__(self):
        return "[%s %s]" % (self.row, self.col)
