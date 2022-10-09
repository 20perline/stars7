from stars7.round import Round
from stars7.strategies import MultiRoundsStrategy
from typing import List
from collections import Counter


class OddEvenSumStrategy(MultiRoundsStrategy):
    """和全奇或全偶且各不相同"""

    def verify(self, round_list: List[Round]):
        sum_list = [sum(c.values) % 10 for c in round_list]
        for i in range(self.works_at_least - 1, self.max_execute_round):
            sub_list = sum_list[:i]
            counter = Counter(sub_list)
            max_cnt = max(counter.values())
            if max_cnt >= 2:
                return i - 1
            if self._list_all_even(sub_list) or self._list_all_odd(sub_list):
                continue
            else:
                return i - 1
        return 0

    def _list_all_even(self, list1):
        return all(s % 2 == 0 for s in list1)

    def _list_all_odd(self, list1):
        return all(s % 2 != 0 for s in list1)
