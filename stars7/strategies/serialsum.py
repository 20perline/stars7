# 每轮之和成某种序列
from stars7.round import Round
from stars7.strategies import AssociatedRoundsStrategy
from stars7 import utils
from collections import Counter
from typing import List


class EqualSumStrategy(AssociatedRoundsStrategy):
    """合数相同"""

    def verify(self, round_list: List[Round]):
        sum_list = [sum(c.values) % 10 for c in round_list]
        for i in range(self.works_at_least - 1, self.max_execute_round):
            sub_list = sum_list[:i]
            if not utils.list_all_same(sub_list):
                return i - 1
        return 0

    def predict(self, predict_index: int, round_list: List[Round]):
        sum_val = sum(round_list[1].values)
        zero_round_values = round_list[0].values
        current_sum = sum([v for v in zero_round_values if v != '?'])
        predict_val = (utils.next_greater_than(sum_val, current_sum) - current_sum) % 10

        return predict_val


class OddEvenSumStrategy(AssociatedRoundsStrategy):
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

    def predict(self, predict_index: int, round_list: List[Round]):
        if len(round_list) != 5:
            return None
        sum_list = [sum(c.values) % 10 for i, c in enumerate(round_list) if i > 0]
        a = [0, 2, 4, 6, 8]
        if sum_list[0] % 2 != 0:
            a = [1, 3, 5, 7, 9]
        diff = [x for x in a if x not in set(sum_list)]
        next_sum = diff[0]
        zero_round_values = round_list[0].values
        current_sum = sum([v for v in zero_round_values if v != '?'])
        predict_val = (utils.next_greater_than(next_sum, current_sum) - current_sum) % 10

        return predict_val


class SequenceSumStrategy(AssociatedRoundsStrategy):
    """合数顺序或逆序"""

    def verify(self, round_list: List[Round]):
        sum_list = [sum(c.values) % 10 for c in round_list]
        for i in range(self.works_at_least - 1, self.max_execute_round):
            sub_list = sum_list[:i]
            if sum_list[0] == 0:
                return i - 1
            if utils.list_in_decrement(sub_list) or utils.list_in_increment(sub_list):
                continue
            else:
                return i - 1
        return 0

    def predict(self, predict_index: int, round_list: List[Round]):
        sum_list = [sum(c.values) % 10 for i, c in enumerate(round_list) if i > 0]
        if utils.list_in_increment(sum_list):
            next_sum = abs(sum_list[0] - 1) % 10
        else:
            next_sum = abs(sum_list[0] + 1) % 10
        zero_round_values = round_list[0].values
        current_sum = sum([v for v in zero_round_values if v != '?'])
        predict_val = (utils.next_greater_than(next_sum, current_sum) - current_sum) % 10

        return predict_val
