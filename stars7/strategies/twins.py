from stars7.strategies import MultiRoundsStrategy
from stars7.round import Round
from stars7.rectangle import Rectangle
# from stars7.utils import list_to_str
from typing import List


class TwinsStrategy(MultiRoundsStrategy):
    """某两个位置值相同"""

    def __init__(self, rect: Rectangle, offset=0, works_at_least=2) -> None:
        super().__init__(rect=rect, offset=offset, elements=2, works_at_least=works_at_least)

    def verify(self, round_list: List[Round]):
        # print(list_to_str(round_list))
        delta_list = [c.values[0] - c.values[1] for c in round_list]
        return all(s == 0 for s in delta_list)
