from stars7 import settings
from stars7.coordinate import Coordinate
from loguru import logger
from typing import List
import pandas as pd


class Feed(object):

    def __init__(self, backward=0) -> None:
        self.star7_data = pd.read_csv(settings.DATABASE_PATH)
        total_rows = len(self.star7_data.index)
        if backward > 0:
            self.df = self.star7_data.loc[backward:total_rows, settings.COL_NAMES]
            self.next_df = self.star7_data.loc[backward-1:backward-1, settings.COL_NAMES]
            self.df.reset_index(drop=True, inplace=True)
            self.next_df.reset_index(drop=True, inplace=True)
            self.winning_ticket = ''.join([str(x) for x in self.next_df[settings.COL_NAMES[1:]].values[0]])
        else:
            self.df = self.star7_data[settings.COL_NAMES]
            self.next_df = None
            self.winning_ticket = ''

        self.next_num = self.star7_data.at[0, 'num'] + 1 - backward
        self.first_split_row = 0
        for i in range(4):
            if self.star7_data.at[i, 'num'] % 4 == 0:
                self.first_split_row = i
                break
        logger.info(
            "feed loaded successfully, total rows {rows}, backward {back}, next_num {num}",
            rows=total_rows, back=backward, num=self.next_num)

    def get_values(self, coordinates: List[Coordinate]):
        return [self.df.at[c.row, c.col] if c.row >= 0 else '?' for c in coordinates]

    def get_value_at(self, row, col):
        return self.df.at[row, settings.COL_NAMES[col]]

    def get_next_value_at(self, col_name):
        if self.next_df is not None:
            return self.next_df.at[0, col_name]
        else:
            return None
