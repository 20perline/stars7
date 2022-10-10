# 一对点
from stars7.strategies import MultiRoundsStrategy
from stars7.round import Round
from stars7.rectangle import Rectangle
from typing import List


class TwinsStrategy(MultiRoundsStrategy):
    """两个位置值相同"""

    def __init__(self, rect: Rectangle, offset=0, works_at_least=2) -> None:
        super().__init__(rect=rect, offset=offset, elements=2, works_at_least=works_at_least)

    def verify(self, round_list: List[Round]):
        works = 1
        for c in round_list:
            a = c.values[0]
            b = c.values[1]
            if abs(a-b) != 0:
                return works - 1
            works += 1
        return works


class OppositeStrategy(MultiRoundsStrategy):
    """两数成对数"""

    def __init__(self, rect: Rectangle, offset=0, works_at_least=2) -> None:
        super().__init__(rect=rect, offset=offset, elements=2, works_at_least=works_at_least)

    def verify(self, round_list: List[Round]):
        works = 1
        for c in round_list:
            a = c.values[0]
            b = c.values[1]
            if abs(a-b) != 5:
                return works - 1
            works += 1
        return works