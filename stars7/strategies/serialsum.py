from stars7.round import Round
from stars7.strategies import MultiRoundsStrategy
from typing import List


class EqualSumStrategy(MultiRoundsStrategy):
    """合数相同"""

    def verify(self, round_list: List[Round]):
        # print(utils.list_to_str(round_list))
        # 合数相同
        sum_list = [sum(c.values) % 10 for c in round_list]
        for i in range(self.works_at_least - 1, self.max_execute_round):
            sub_list = sum_list[:i]
            if not self._list_the_same(sub_list):
                return i - 1
        return 0

    def _list_the_same(self, list1):
        return all(s == list1[0] for s in list1)
