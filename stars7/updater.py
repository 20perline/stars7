# download data from the internet
import requests
import csv
import os
from loguru import logger
from stars7 import settings, utils
from abc import abstractmethod, ABCMeta


class Updater(metaclass=ABCMeta):

    def update(self):
        last_draw_day = utils.get_last_draw_day()
        first_row_day = None
        if os.path.exists(settings.DATABASE_PATH):
            with open(settings.DATABASE_PATH, 'r') as file:
                reader = csv.DictReader(file)
                first_row_day = next(reader)['day']
        if first_row_day == last_draw_day:
            logger.info("stars7 data was already up to date {day}", day=last_draw_day)
            return
        data_row = self.fetch()
        if len(data_row) > 0:
            self.save_to_database(data_row)
        else:
            logger.warning('no data fetched, update aborted')

    @abstractmethod
    def fetch(self) -> list:
        pass

    def save_to_database(self, data_row):
        with open(settings.DATABASE_PATH, 'w') as file:
            writer = csv.writer(file)
            writer.writerow(settings.CSV_HEADERS)
            writer.writerows(data_row)


class SportUpdater(Updater):

    def fetch(self) -> list:
        logger.info('start to download data from from https://www.lottery.gov.cn')
        total_page = 100
        page_num = 1
        max_total = 250
        idx = 1
        url = "https://webapi.sporttery.cn/gateway/lottery/getHistoryPageListV1.qry"
        payload = {
            "gameNo": "04",
            "provinceId": "0",
            "isVerify": 1,
            "pageNo": 1,
            "pageSize": 30
        }
        headers = {
            "content-type": "application/json",
            "user-agent": "stars7 engine"
        }
        data_row = []
        while page_num <= total_page:
            payload['pageNo'] = page_num
            resp = requests.get(url, params=payload, headers=headers)
            data = resp.json()
            val = data['value']
            if val['total'] == 0:
                return data_row
            total_page = val['pages']
            for l1 in val['list']:
                a = [l1['lotteryDrawTime'], l1['lotteryDrawNum']]
                columns = l1['lotteryDrawResult'].split(' ')
                columns[6] = int(columns[6]) % 10
                sum = int(columns[0]) + int(columns[1]) + int(columns[2]) + int(columns[3])
                a.append(sum % 10)
                a.extend(columns)
                data_row.append(a)
                idx += 1
            if idx >= max_total:
                logger.info('total rows reach maximum {}'.format(max_total))
                break
            logger.info('download page {} done.'.format(resp.url))
            page_num += 1
        logger.info('download data end')
        return data_row
