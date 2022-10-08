from stars7 import settings
from stars7.coordinate import Coordinate
from typing import List
import pandas as pd


class Feed(object):

    def __init__(self) -> None:
        # self.star7_data = pd.read_csv(settings.data_path, skiprows=range(1, 5))
        self.star7_data = pd.read_csv(settings.DATA_PATH)
        self.next_num = self.star7_data.at[0, 'num'] + 1
        self.split_row = 0
        for i in range(4):
            if self.star7_data.at[i, 'num'] % 4 == 0:
                self.split_row = i
                break
        print(self.split_row)
        self.df = self.star7_data[settings.COL_NAMES]
        print(self.df.head(15))

    def get_values(self, coordinates: List[Coordinate]):
        return [self.df.at[c.row, c.col] for c in coordinates]

    def get_value_at(self, row, col):
        return self.df.at[row,  settings.COL_NAMES[col]]
