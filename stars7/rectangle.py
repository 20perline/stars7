
class Rectangle(object):

    def __init__(self, offset=0, rows=4, start_col=0, cols=7) -> None:
        self.offset = offset
        self.start_col = start_col
        self.cols = cols
        self.rows = rows

    def __str__(self):
        return "[offset=%s, rows=%s, start_col=%s, cols=%s]" % (self.offset, self.rows, self.start_col, self.cols)
