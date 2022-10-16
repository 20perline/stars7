from collections import defaultdict
from stars7.pattern import Pattern
from loguru import logger


class Statistics(object):
    """统计"""

    def __init__(self) -> None:
        self.all_counter = defaultdict(int)
        self.success_counter = defaultdict(int)

    def add_data(self, pattern: Pattern):
        p_name = pattern.name
        self.all_counter[p_name] += 1
        if pattern.predict_success:
            self.success_counter[p_name] += 1

    def show(self):
        for p_name, cnt in self.all_counter.items():
            success_cnt = self.success_counter.get(p_name)
            if success_cnt is None:
                success_cnt = 0
            if cnt is None:
                cnt = 0
                rate = '0%'
            else:
                rate = "{0:.0%}".format(success_cnt / cnt)
            logger.info(
                "pattern {name} \t\trate: {rate} ({cnt1}/{cnt2})",
                name=p_name,
                rate=rate,
                cnt1=success_cnt,
                cnt2=cnt)
        pass
