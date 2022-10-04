
class Rectangle(object):

    def __init__(self, rows=4, start_col=1, cols=7) -> None:
        self.start_col = start_col
        self.cols = cols
        self.rows = rows

    def __str__(self):
        return "[rows=%s, start_col=%s, cols=%s]" % (self.rows, self.start_col, self.cols)
