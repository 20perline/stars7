from collections import defaultdict
from stars7.pattern import Pattern
from stars7 import settings
from loguru import logger
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
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
        self.mask_counter_by_num = dict()
        self.strategy_counter_by_num = dict()
        self.strategy_counter_by_works_num = dict()
        self.success_mask_by_num = defaultdict(set)
        self.winning_tickets = defaultdict(str)

    def add_data(self, pattern: Pattern):
        p_num = pattern.prediction_num
        p_mask = pattern.prediction_mask
        mask_counter = self.mask_counter_by_num.get(p_num, defaultdict(int))
        mask_counter[p_mask] += 1
        self.mask_counter_by_num[p_num] = mask_counter

        # by strategy
        p_strategy = pattern.strategy
        strategy_num_counter = self.strategy_counter_by_num.get(p_num, defaultdict(int))
        strategy_num_counter[p_strategy] += 0
        strategy_num_counter[p_strategy + 'Total'] += 1

        # by works and then by strategy
        p_works = len(pattern.round_list)
        strategy_works_counter = self.strategy_counter_by_works_num.get(p_works, defaultdict(dict))
        strategy_works_num_counter = strategy_works_counter.get(p_num, defaultdict(int))
        strategy_works_num_counter[p_strategy] += 0
        strategy_works_num_counter[p_strategy + 'Total'] += 1

        if pattern.predict_success:
            self.winning_tickets[p_num] = pattern.winning_ticket
            self.success_mask_by_num[p_num].add(p_mask)
            strategy_num_counter[p_strategy] += 1
            strategy_works_num_counter[p_strategy] += 1

        self.strategy_counter_by_num[p_num] = strategy_num_counter
        strategy_works_counter[p_num] = strategy_works_num_counter
        self.strategy_counter_by_works_num[p_works] = strategy_works_counter

    def display_result(self):
        try:
            self._save_stat_per_num()
            self._save_success_rate_per_strategy()
        except Exception:
            self._logger.exception("What?!")

    def _save_stat_per_num(self):
        for num, mc_dict in self.mask_counter_by_num.items():
            mask_list = list(mc_dict.keys())
            num_column_df = pd.DataFrame({'mask': mask_list, 'cnt': list(mc_dict.values())})
            correct_masks = self.success_mask_by_num[num]
            color_list = ['#ff7f0e' if m in correct_masks else '#1f77b4' for m in mask_list]
            winning_ticket = self.winning_tickets[num]
            title = 'NO. {} Prediction {}'.format(num, winning_ticket)
            ax = num_column_df.plot.barh(x='mask', y='cnt', title=title, rot=0, color=color_list, figsize=(10, 8), fontsize=8)
            ax.get_xaxis().set_major_locator(MaxNLocator(integer=True, nbins='auto'))
            if self.analyze_mode:
                num_dir = os.path.join(settings.DATA_DIR, 'analysis')
            else:
                num_dir = os.path.join(settings.DATA_DIR, str(num))

            if not os.path.exists(num_dir):
                os.makedirs(num_dir)
            plt.savefig(os.path.join(num_dir, '{}_mask_stat.jpg'.format(num)))
            plt.close()

    def _save_success_rate_per_strategy(self):
        if not self.analyze_mode:
            return
        if len(self.strategy_counter_by_num) == 0:
            self._logger.info('no statistics data found.')
            return
        df = pd.DataFrame(self.strategy_counter_by_num).T
        df = df.sort_index()
        st_num_stat_file = os.path.join(settings.DATA_DIR, 'strategy_num_stat.csv')
        df.to_csv(st_num_stat_file)
        total_df = df.sum(numeric_only=True, axis=0)
        st_columns = [c for c in df.columns if not c.endswith('Total')]
        st_rate_columns = []
        for st in st_columns:
            rate_c = st + 'Rate'
            st_rate_columns.append(rate_c)
            df[rate_c] = (df[st] / df[st + 'Total']) * 100
            total_df[rate_c] = (total_df[st] / total_df[st + 'Total']) * 100

        df.fillna(0, inplace=True)
        total_df.fillna(0, inplace=True)

        rate_df = df[st_rate_columns]
        total_rate_df = total_df[st_rate_columns]

        works_len = len(self.strategy_counter_by_works_num)
        height_ratios = [2]
        height_ratios.extend([3] * (works_len + 1))
        fig, axes = plt.subplots(nrows=2 + works_len, ncols=1, figsize=(16, 32), gridspec_kw={'height_ratios': height_ratios})

        total_rate_df.plot.bar(ax=axes[0], rot=0, fontsize=8, title='Summary SuccessRate')

        ax1 = rate_df.plot(ax=axes[1], ylim=[0, 100], title='Summary SuccessRate Trends')
        ax1.ticklabel_format(useOffset=False)
        ax1.get_xaxis().set_major_locator(MaxNLocator(integer=True, nbins='auto'))

        ax_idx = 2
        # by works + strategy plot
        for works, counter in self.strategy_counter_by_works_num.items():
            if len(counter) == 0:
                continue
            df = pd.DataFrame(counter).T
            df = df.sort_index()
            total_df = df.sum(numeric_only=True, axis=0)
            st_columns = [c for c in df.columns if not c.endswith('Total')]
            st_rate_columns = []
            for st in st_columns:
                rate_c = st + 'Rate'
                st_rate_columns.append(rate_c)
                df[rate_c] = (df[st] / df[st + 'Total']) * 100
                total_df[rate_c] = (total_df[st] / total_df[st + 'Total']) * 100

            df.fillna(0, inplace=True)
            total_df.fillna(0, inplace=True)

            rate_df = df[st_rate_columns]

            ax = rate_df.plot(ax=axes[ax_idx], ylim=[0, 100], title='SuccessRate Trends for works {} times'.format(works))
            ax.ticklabel_format(useOffset=False)
            ax.get_xaxis().set_major_locator(MaxNLocator(integer=True, nbins='auto'))

            ax_idx += 1

        filename = 'success_rate.jpg'
        success_stat_file = os.path.join(settings.DATA_DIR, filename)
        plt.savefig(success_stat_file)
        plt.close()
