from stars7.round import Round
from stars7.strategies import MultiRoundsStrategy
from typing import List


class SerialSumStrategy(MultiRoundsStrategy):
    """每轮和形成某种序列"""

    def verify(self, round_list: List[Round]):
        # print(utils.list_to_str(round_list))
        sum_list = [sum(c.values) for c in round_list]
        all_same = self._list_the_same(sum_list)
        if all_same:
            return True
        if len(round_list) >= 3:
            even_list = [x for i, x in enumerate(sum_list) if i % 2 == 0]
            odd_list = [x for i, x in enumerate(sum_list) if i % 2 != 0]
            return self._list_the_same(even_list) and self._list_the_same(odd_list)
        return False

    def _list_the_same(self, list1):
        return all(s == list1[0] for s in list1)
