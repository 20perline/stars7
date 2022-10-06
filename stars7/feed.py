from stars7 import settings
from stars7.coordinate import Coordinate
from typing import List
import pandas as pd


class Feed(object):

    def __init__(self) -> None:
        # self.star7_data = pd.read_csv(settings.data_path, skiprows=range(1, 5))
        self.star7_data = pd.read_csv(settings.DATA_PATH)
        self.df = self.star7_data[settings.COL_NAMES]
        print(self.df.head(15))

    def get_values(self, coordinates: List[Coordinate]):
        return [self.df.at[c.row, c.col] for c in coordinates]

    def get_value_at(self, row, col):
        return self.df.at[row,  settings.COL_NAMES[col]]
