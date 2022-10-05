from stars7 import settings
from stars7.coordinate import Coordinate
from typing import List
import pandas as pd


class Feed(object):

    def __init__(self) -> None:
        # self.star7_data = pd.read_csv(settings.data_path, skiprows=range(1, 5))
        self.star7_data = pd.read_csv(settings.data_path)
        self.df = self.star7_data[settings.col_names]
        print(self.df.head(15))

    def get_values(self, coordinates: List[Coordinate]):
        return [self.df.at[c.row, c.col] for c in coordinates]


if __name__ == '__main__':
    feed = Feed()