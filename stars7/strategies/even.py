# 点的总个数是偶数
from stars7.round import Round
from stars7.rectangle import Rectangle
from stars7.strategies import AssociatedRoundsStrategy
from stars7 import utils
from typing import List
from loguru import logger


class AlternatedSumStrategy(AssociatedRoundsStrategy):
    """奇偶数位交叉合数相等"""

    def __init__(self, rect: Rectangle, offset, works_at_least=2) -> None:
        super().__init__(rect=rect, offset=offset, elements=range(2, 6, 2), works_at_least=works_at_least)

    def verify(self, round_list: List[Round]):
        works = 1
        for c in round_list:
            even_idx_vals = [v for i, v in enumerate(c.values) if i % 2 == 0]
            odd_idx_vals = [v for i, v in enumerate(c.values) if i % 2 != 0]
            if sum(even_idx_vals) % 10 != sum(odd_idx_vals) % 10:
                return works - 1
            works += 1
        return works

    def predict(self, predict_index: int, round_list: List[Round]):
        zero_round_values = round_list[0].values
        even_sum = sum([v for i, v in enumerate(zero_round_values) if v != '?' and i % 2 == 0])
        odd_sum = sum([v for i, v in enumerate(zero_round_values) if v != '?' and i % 2 != 0])
        if predict_index % 2 == 0:
            predict_val = (utils.next_greater_than(odd_sum, even_sum) - even_sum) % 10
        else:
            predict_val = (utils.next_greater_than(even_sum, odd_sum) - odd_sum) % 10

        logger.debug(
            "predict index {index}, predict value {val}, rounds:\n{rounds}",
            index=predict_index,
            val=predict_val,
            rounds=utils.list_to_str(round_list, join_str="\n"))
        zero_round_values[predict_index] = predict_val
