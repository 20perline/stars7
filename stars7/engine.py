from loguru import logger
from stars7.strategies import Strategy
from stars7.printer import Printer
from stars7.feed import Feed
from stars7.statistics import Statistics
from stars7.updater import SportUpdater
from multiprocessing import Pool
from multiprocessing.managers import BaseManager
import time


class Engine(object):

    def __init__(self) -> None:
        updater = SportUpdater()
        updater.update()
        self.strategies = []

    def add_strategy(self, strategy: Strategy):
        self.strategies.append(strategy)

    def execute(self, num=None):
        feed = Feed(num=num)
        statistics = Statistics(analyze_mode=False)
        printer = Printer(feed=feed)
        for strategy in self.strategies:
            for pattern in strategy.execute(feed):
                statistics.add_data(pattern)
                printer.do_print(pattern)
        statistics.show()

    def analyze(self, num_count=2, process_count=None):
        start_time = time.perf_counter()
        manager = BaseManager()
        manager.register('Statistics', Statistics)
        manager.start()
        statistics = manager.Statistics()
        args_list = []
        for backward in range(1, num_count):
            feed = Feed(backward=backward)
            for strategy in self.strategies:
                args_list.append((feed, strategy, statistics))

        p = Pool(process_count)
        p.map(self._process_analyze, args_list)
        p.close()
        p.join()
        end_time = time.perf_counter()
        logger.info('time elapsed: {elapsed} seconds', elapsed=end_time - start_time)
        statistics.show()

    def _process_analyze(self, args):
        feed, strategy, statistics = args

        for pattern in strategy.execute(feed):
            statistics.add_data(pattern)
