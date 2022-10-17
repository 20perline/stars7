from stars7.strategies import Strategy
from stars7.printer import Printer
from stars7.feed import Feed
from stars7.statistics import Statistics
from stars7.database import SportDatabase


class Engine(object):

    def __init__(self) -> None:
        db = SportDatabase()
        db.refresh()
        self.strategies = []

    def add_strategy(self, strategy: Strategy):
        self.strategies.append(strategy)

    def execute(self, backward=0):
        feed = Feed(backward=backward)
        printer = Printer(feed=feed)
        for strategy in self.strategies:
            for pattern in strategy.execute(feed):
                printer.do_print(pattern)

    def analyze(self, num_count=100):
        statistics = Statistics()
        for backward in range(1, num_count):
            feed = Feed(backward=backward)
            for strategy in self.strategies:
                for pattern in strategy.execute(feed):
                    statistics.add_data(pattern)
        statistics.show()
