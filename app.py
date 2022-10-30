from stars7.strategies import even, serialsum, single, twins, isolated
from stars7.engine import Engine


if __name__ == '__main__':

    engine = Engine()

    offset = range(4)
    elements = range(1, 4)

    strategy8 = isolated.SumToLastStrategy(offset=offset, elements=elements, works_at_least=3)
    engine.add_strategy(strategy8)

    strategy5 = serialsum.OddEvenSumStrategy(offset=offset, elements=elements, works_at_least=4)
    engine.add_strategy(strategy5)

    strategy7 = serialsum.SequenceSumStrategy(offset=offset, elements=elements, works_at_least=3)
    engine.add_strategy(strategy7)

    strategy1 = serialsum.EqualSumStrategy(offset=offset, column_offset=0, elements=elements, works_at_least=3)
    engine.add_strategy(strategy1)

    strategy3 = twins.TwinsStrategy(offset=offset, works_at_least=3)
    engine.add_strategy(strategy3)

    strategy6 = twins.OppositeStrategy(offset=offset, works_at_least=3)
    engine.add_strategy(strategy6)

    strategy4 = even.AlternatedSumStrategy(offset=offset, works_at_least=3)
    engine.add_strategy(strategy4)

    for column_offset in range(-1, 2):
        strategy21 = single.SingleSameStrategy(offset=offset, column_offset=column_offset, works_at_least=2)
        strategy22 = single.SingleIncreaseStrategy(offset=offset, column_offset=column_offset, works_at_least=2)
        strategy23 = single.SingleDecreaseStrategy(offset=offset, column_offset=column_offset, works_at_least=2)

        engine.add_strategy(strategy21)
        engine.add_strategy(strategy22)
        engine.add_strategy(strategy23)

    engine.execute()
    # engine.execute(num=22122)
    # engine.analyze(num_count=100, process_count=None)
