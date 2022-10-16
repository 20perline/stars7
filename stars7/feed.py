from stars7 import settings
from stars7.coordinate import Coordinate
from loguru import logger
from typing import List
import pandas as pd


class Feed(object):

    def __init__(self, backward=0) -> None:
        if backward > 0:
            self.star7_data = pd.read_csv(settings.DATA_PATH, skiprows=range(1, backward+2))
        else:
            self.star7_data = pd.read_csv(settings.DATA_PATH)
        total_rows = len(self.star7_data.index)
        self.next_num = self.star7_data.at[0, 'num'] + 1
        self.first_split_row = 0
        for i in range(4):
            if self.star7_data.at[i, 'num'] % 4 == 0:
                self.first_split_row = i
                break
        self.df = self.star7_data[settings.COL_NAMES]
        logger.info("feed loaded from databases successfully, total rows {rows}", rows=total_rows)
        # logger.info(self.df.head(15))

    def get_values(self, coordinates: List[Coordinate]):
        return [self.df.at[c.row, c.col] if c.row >= 0 else '?' for c in coordinates]

    def get_value_at(self, row, col):
        return self.df.at[row,  settings.COL_NAMES[col]]
