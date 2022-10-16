from stars7.strategies import Strategy
from stars7.printer import Printer
from stars7.feed import Feed
from stars7.statistics import Statistics
from stars7.database import SportDatabase


class Engine(object):

    def __init__(self, backward=0) -> None:
        db = SportDatabase()
        db.refresh()
        self.backward = backward
        self.feed = Feed(backward=self.backward)
        self.printer = Printer(feed=self.feed)
        self.strategies = []

    def add_strategy(self, strategy: Strategy):
        self.strategies.append(strategy)

    def execute(self):
        for strategy in self.strategies:
            for pattern in strategy.execute(self.feed):
                self.printer.do_print(pattern)

    def analyze(self):
        statistics = Statistics()
        for backward in range(1, 20):
            feed = Feed(backward=backward)
            for strategy in self.strategies:
                for pattern in strategy.execute(feed):
                    statistics.add_data(pattern)
        statistics.show()
