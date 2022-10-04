
from operator import le
from feed import Feed
from rectangle import Rectangle
from round import Round
from strategy import EqSiblingsStrategy, SlashStrategy
from utils import coordinates_to_str

feed = Feed()
rect = Rectangle(start_col=1, cols=5, rows=3)
# strategy = EqSiblingsStrategy(rect=rect, offset=2, elements=2)
strategy = SlashStrategy(rect=rect, offset=0, elements=1, works_at_least=3)


for idx in strategy.indexes_generator():
    # print(idx)
    round_idx = 0
    last_values = None
    for round_num in range(1, 10):
        # print(round_num)
        coord_list = []
        pos_coord = strategy.next_round_pos(round_num=round_num)
        coord_list.append(pos_coord)
        for coord in strategy.next_round_coord(idx, round_num=round_num):
            coord_list.append(coord)
        if len(coord_list) == 1:
            break
        values = feed.get_values(coord_list)
        print('aaa', idx, round_num, coordinates_to_str(coord_list), values)
        round = Round(round_num=round_num, coordinates=coord_list, values=values, last_values=last_values)
        res = strategy.verify(round=round)
        if not res:
            break
        # else:
            # print(coordinates_to_str(coord_list))
        last_values = values
        round_idx = round_num

    if round_idx >= strategy.works_at_least:
        coords = strategy.next_round_coord(idx, round_num=1)
        string1 = coordinates_to_str(coords)
        print(round_idx, string1, strategy)
