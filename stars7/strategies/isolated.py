from stars7.round import Round
from stars7.strategies import AssociatedRoundsStrategy
from typing import List


class SumToLastStrategy(AssociatedRoundsStrategy):
    """前面n个合数等于最下面一个"""

    def verify(self, round_list: List[Round]):
        works = 1
        for round in round_list:
            row_indexes = [c.row for c in round.coordinates]
            lowest_row_idx = min(row_indexes)
            if row_indexes.count(lowest_row_idx) > 1:
                return works - 1
            round_values = round.values.copy()
            last_val = round_values[row_indexes.index(lowest_row_idx)]
            round_values.remove(last_val)
            rest_sum = sum(round_values)
            if last_val % 10 != rest_sum % 10:
                return works - 1
            works += 1
        return works

    def predict(self, predict_index: int, round_list: List[Round]):
        return sum([v for v in round_list[0].values if v != '?']) % 10
