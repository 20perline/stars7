from stars7.round import Round
from stars7.strategies import MultiRoundsStrategy
from typing import List


class SerialSumStrategy(MultiRoundsStrategy):
    """每轮和形成某种序列"""

    def verify(self, round_list: List[Round]):
        # print(utils.list_to_str(round_list))
        # 合数相同
        sum_list = [sum(c.values) % 10 for c in round_list]
        all_same = self._list_the_same(sum_list)
        if all_same:
            return True
        # 合数全偶或全奇
        # if self._list_all_even(sum_list) or self._list_all_odd(sum_list):
            # return True
        # 合数奇偶轮流
        if len(round_list) >= 2:
            even_list = [x for i, x in enumerate(sum_list) if i % 2 == 0]
            odd_list = [x for i, x in enumerate(sum_list) if i % 2 != 0]
            return self._list_the_same(even_list) and self._list_the_same(odd_list)
        return False

    def _list_the_same(self, list1):
        return all(s == list1[0] for s in list1)

    def _list_all_even(self, list1):
        return all(s % 2 == 0 for s in list1)

    def _list_all_odd(self, list1):
        return all(s % 2 != 0 for s in list1)
