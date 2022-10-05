from stars7.rectangle import Rectangle
from stars7.round import Round
from stars7.strategies import SingleRoundStrategy


class SimpleStrategy(SingleRoundStrategy):
    "相同单个位置上值相同"""

    def __init__(self, rect: Rectangle, offset=0, pos=1, works_at_least=2) -> None:
        super().__init__(rect=rect, offset=offset, pos=pos, elements=1, works_at_least=works_at_least)

    def verify(self, round: Round):
        # print(round)
        if round is None:
            return False
        values = round.values
        return values[0] == values[1]
