from stars7.rectangle import Rectangle
from stars7.strategies import even, serialsum, single, twins
from stars7.engine import Engine


engine = Engine(backward=0)
rect1 = Rectangle(start_col=1, rows=4, cols=5)

offset = range(4)
elements = range(1, 4)

strategy5 = serialsum.OddEvenSumStrategy(rect=rect1, offset=offset, elements=elements, works_at_least=3)
engine.add_strategy(strategy5)

strategy1 = serialsum.EqualSumStrategy(rect=rect1, offset=offset, column_offset=0, elements=elements, works_at_least=3)
engine.add_strategy(strategy1)

strategy3 = twins.TwinsStrategy(rect=rect1, offset=offset, works_at_least=2)
engine.add_strategy(strategy3)

strategy6 = twins.OppositeStrategy(rect=rect1, offset=offset, works_at_least=3)
engine.add_strategy(strategy6)

strategy4 = even.AlternatedSumStrategy(rect=rect1, offset=offset, works_at_least=3)
engine.add_strategy(strategy4)

for column_offset in range(-1, 2):
    strategy21 = single.SingleSameStrategy(rect=rect1, offset=offset, column_offset=column_offset, works_at_least=3)
    strategy22 = single.SingleIncreaseStrategy(rect=rect1, offset=offset, column_offset=column_offset, works_at_least=3)
    strategy23 = single.SingleDecreaseStrategy(rect=rect1, offset=offset, column_offset=column_offset, works_at_least=3)

    engine.add_strategy(strategy21)
    engine.add_strategy(strategy22)
    engine.add_strategy(strategy23)

engine.execute()
