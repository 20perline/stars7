from collections import defaultdict
from stars7.pattern import Pattern
from stars7 import settings
from loguru import logger
import matplotlib.pyplot as plt
import pandas as pd
import os


class Statistics(object):
    """统计"""

    _logger = logger

    @staticmethod
    def set_logger(logger_):
        Statistics._logger = logger_

    def __init__(self, analyze_mode=True) -> None:
        self.analyze_mode = analyze_mode
        self.strategy_counter_all = defaultdict(int)
        self.strategy_success_counter = defaultdict(int)
        self.mask_counter_by_num = dict()
        self.strategy_counter_by_num = dict()
        self.success_mask_by_num = defaultdict(set)
        self.winning_tickets = defaultdict(str)

    def add_data(self, pattern: Pattern):
        p_num = pattern.prediction_num
        p_mask = pattern.prediction_mask
        mask_counter = self.mask_counter_by_num.get(p_num, defaultdict(int))
        mask_counter[p_mask] += 1
        self.mask_counter_by_num[p_num] = mask_counter

        p_strategy = pattern.strategy
        strategy_counter = self.strategy_counter_by_num.get(p_num, defaultdict(int))
        strategy_counter[p_strategy] += 1
        self.strategy_counter_by_num[p_num] = strategy_counter

        self.strategy_counter_all[p_strategy] += 1

        if pattern.predict_success:
            self.winning_tickets[p_num] = pattern.winning_ticket
            self.success_mask_by_num[p_num].add(p_mask)
            self.strategy_success_counter[p_strategy] += 1

    def show(self):
        self._save_stat_per_num()

        self._save_success_rate_per_strategy()

    def _save_stat_per_num(self):
        for num, mc_dict in self.mask_counter_by_num.items():
            mask_list = list(mc_dict.keys())
            num_column_df = pd.DataFrame({'mask': mask_list, 'cnt': list(mc_dict.values())})
            correct_masks = self.success_mask_by_num[num]
            color_list = ['#ff7f0e' if m in correct_masks else '#1f77b4' for m in mask_list]
            winning_ticket = self.winning_tickets[num]
            title = 'NO. {} Prediction {}'.format(num, winning_ticket)
            num_column_df.plot.barh(x='mask', y='cnt', title=title, rot=0, color=color_list, figsize=(10, 8), fontsize=8)
            if self.analyze_mode:
                num_dir = os.path.join(settings.DATA_DIR, 'analysis')
            else:
                num_dir = os.path.join(settings.DATA_DIR, str(num))

            if not os.path.exists(num_dir):
                os.makedirs(num_dir)
            plt.savefig(os.path.join(num_dir, '{}_mask_stat.jpg'.format(num)))
            plt.close()

    def _save_success_rate_per_strategy(self):
        ss_counter = self.strategy_success_counter
        if len(ss_counter) > 0:
            rate_list = [(ss_counter[s] / self.strategy_counter_all[s]) * 100 for s in ss_counter.keys()]
            success_df = pd.DataFrame({'rate': rate_list}, index=ss_counter.keys())
            ax = success_df.plot.bar(rot=0, figsize=(10, 8), fontsize=8)
            for p in ax.patches:
                ax.annotate(str(int(p.get_height())) + '%', (p.get_x() * 1.01, p.get_height() * 1.005))

            success_stat_file = os.path.join(settings.DATA_DIR, 'success_rate.jpg')
            plt.savefig(success_stat_file)
            plt.show()
