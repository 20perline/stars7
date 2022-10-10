# 每轮之和成某种序列
from stars7.round import Round
from stars7.strategies import MultiRoundsStrategy
from stars7 import utils
from collections import Counter
from typing import List


class EqualSumStrategy(MultiRoundsStrategy):
    """合数相同"""

    def verify(self, round_list: List[Round]):
        sum_list = [sum(c.values) % 10 for c in round_list]
        for i in range(self.works_at_least - 1, self.max_execute_round):
            sub_list = sum_list[:i]
            if not utils.list_all_same(sub_list):
                return i - 1
        return 0


class OddEvenSumStrategy(MultiRoundsStrategy):
    """合数全奇或全偶且各不相同"""

    def verify(self, round_list: List[Round]):
        sum_list = [sum(c.values) % 10 for c in round_list]
        for i in range(self.works_at_least - 1, self.max_execute_round):
            sub_list = sum_list[:i]
            counter = Counter(sub_list)
            max_cnt = max(counter.values())
            if max_cnt >= 2:
                return i - 1
            if utils.list_all_even(sub_list) or utils.list_all_odd(sub_list):
                continue
            else:
                return i - 1
        return 0
