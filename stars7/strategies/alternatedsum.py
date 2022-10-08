from stars7.round import Round
from stars7.rectangle import Rectangle
from stars7.strategies import MultiRoundsStrategy
from typing import List


class AlternatedSumStrategy(MultiRoundsStrategy):
    """偶数位交叉和相等"""

    def __init__(self, rect: Rectangle, offset=0, elements=2, works_at_least=2) -> None:
        if elements % 2 != 0:
            raise Exception('invalid elements value, even number only')
        super().__init__(rect=rect, offset=offset, elements=elements, works_at_least=works_at_least)

    def verify(self, round_list: List[Round]):
        # print(utils.list_to_str(round_list))
        works = 0
        for c in round_list:
            even_idx_vals = [v for i, v in enumerate(c.values) if i % 2 == 0]
            odd_idx_vals = [v for i, v in enumerate(c.values) if i % 2 != 0]
            if sum(even_idx_vals) % 10 != sum(odd_idx_vals) % 10:
                break
            works += 1
        if works >= self.works_at_least:
            return True
        return False
