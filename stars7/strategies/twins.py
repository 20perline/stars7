# 一对点
from stars7.strategies import AssociatedRoundsStrategy
from stars7.round import Round
from stars7.rectangle import Rectangle
from stars7 import utils
from loguru import logger
from typing import List


class TwinsStrategy(AssociatedRoundsStrategy):
    """两个位置值相同"""

    def __init__(self, rect: Rectangle, offset, works_at_least=2) -> None:
        super().__init__(rect=rect, offset=offset, elements=[2], works_at_least=works_at_least)

    def verify(self, round_list: List[Round]):
        works = 1
        for c in round_list:
            a = c.values[0]
            b = c.values[1]
            if abs(a-b) != 0:
                return works - 1
            works += 1
        return works

    def predict(self, predict_index: str, round_list: List[Round]):
        predict_val = round_list[0].values[abs(1-predict_index)]
        logger.debug(
            "predict index {index}, predict value {val}, rounds:\n{rounds}",
            index=predict_index,
            val=predict_val,
            rounds=utils.list_to_str(round_list, join_str="\n"))
        round_list[0].values[predict_index] = predict_val


class OppositeStrategy(AssociatedRoundsStrategy):
    """两数成对数"""

    def __init__(self, rect: Rectangle, offset, works_at_least=2) -> None:
        super().__init__(rect=rect, offset=offset, elements=[2], works_at_least=works_at_least)

    def verify(self, round_list: List[Round]):
        works = 1
        for c in round_list:
            a = c.values[0]
            b = c.values[1]
            if abs(a-b) != 5:
                return works - 1
            works += 1
        return works

    def predict(self, predict_index: int, round_list: List[Round]):
        predict_val = (round_list[0].values[abs(1-predict_index)] + 5) % 10
        logger.debug(
            "predict index {index}, predict value {val}, rounds:\n{rounds}",
            index=predict_index,
            val=predict_val,
            rounds=utils.list_to_str(round_list, join_str="\n"))
        round_list[0].values[predict_index] = predict_val
