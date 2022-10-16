# 单点
from stars7.rectangle import Rectangle
from stars7.round import Round
from stars7.strategies import AssociatedRoundsStrategy
from stars7 import utils
from typing import List


class SingleSameStrategy(AssociatedRoundsStrategy):
    """单个数 坚或斜着 重复"""

    def __init__(self, rect: Rectangle, offset, column_offset, works_at_least=2) -> None:
        super().__init__(rect=rect, offset=offset, column_offset=column_offset, elements=[1], works_at_least=works_at_least)

    def verify(self, round_list: List[Round]):
        sum_list = [c.values[0] for c in round_list]
        for i in range(self.works_at_least - 1, self.max_execute_round):
            sub_list = sum_list[:i]
            if utils.list_all_same(sub_list):
                continue
            else:
                return i - 1
        return 0

    def predict(self, round_list: List[Round]):
        predict_val = round_list[1].values[0]
        round_list[0].values[0] = predict_val


class SingleDecreaseStrategy(SingleSameStrategy):
    """单个数 坚或斜着 递减"""

    def verify(self, round_list: List[Round]):
        sum_list = [c.values[0] for c in round_list]
        if 0 in sum_list:
            return 0
        for i in range(self.works_at_least - 1, self.max_execute_round):
            sub_list = sum_list[:i]
            if utils.list_in_decrement(sub_list):
                continue
            else:
                return i - 1
        return 0

    def predict(self, round_list: List[Round]):
        predict_val = round_list[1].values[0]
        round_list[0].values[0] = predict_val - 1


class SingleIncreaseStrategy(SingleSameStrategy):
    """单个数 坚或斜着 递增"""

    def verify(self, round_list: List[Round]):
        sum_list = [c.values[0] for c in round_list]
        if 0 in sum_list:
            return 0
        for i in range(self.works_at_least - 1, self.max_execute_round):
            sub_list = sum_list[:i]
            if utils.list_in_increment(sub_list):
                continue
            else:
                return i - 1
        return 0

    def predict(self, round_list: List[Round]):
        predict_val = round_list[1].values[0]
        round_list[0].values[0] = predict_val + 1