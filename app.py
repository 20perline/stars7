from stars7.strategies import even, serialsum, single, twins, isolated
from stars7.engine import Engine


if __name__ == '__main__':

    engine = Engine()

    strategy8 = isolated.SumToLastStrategy(works_at_least=3)
    engine.add_strategy(strategy8)

    strategy5 = serialsum.OddEvenSumStrategy(works_at_least=4)
    engine.add_strategy(strategy5)

    strategy7 = serialsum.SequenceSumStrategy(works_at_least=3)
    engine.add_strategy(strategy7)

    strategy1 = serialsum.EqualSumStrategy(works_at_least=3)
    engine.add_strategy(strategy1)

    strategy3 = twins.TwinsStrategy(works_at_least=3)
    engine.add_strategy(strategy3)

    strategy6 = twins.OppositeStrategy(works_at_least=2)
    engine.add_strategy(strategy6)

    strategy4 = even.AlternatedSumStrategy(works_at_least=3)
    engine.add_strategy(strategy4)

    for column_offset in range(-1, 2):
        strategy21 = single.SingleSameStrategy(column_offset=column_offset, works_at_least=2)
        strategy22 = single.SingleDecreaseStrategy(column_offset=column_offset, works_at_least=2)
        strategy23 = single.SingleIncreaseStrategy(column_offset=column_offset, works_at_least=2)

        engine.add_strategy(strategy21)
        engine.add_strategy(strategy22)
        engine.add_strategy(strategy23)

    engine.execute()
