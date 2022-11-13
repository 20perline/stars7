# download data from the internet
import requests
from loguru import logger
from stars7 import utils
from stars7.database import Database


class Updater(object):
    """中国体彩网首页"""

    HOST = 'https://www.lottery.gov.cn'
    BASE_URL = "https://webapi.sporttery.cn/gateway/lottery/getHistoryPageListV1.qry"
    HEADERS = {
        "content-type": "application/json",
        "user-agent": "stars7 engine"
    }
    MAX_PAGE = 10

    _logger = logger

    @staticmethod
    def set_logger(logger_):
        Updater._logger = logger_

    def update(self):
        last_draw_day = utils.get_last_draw_day()
        database = Database()
        latest_draw_day = database.get_latest_draw_day()

        if latest_draw_day == last_draw_day:
            self._logger.info("stars7 data was already up to date {day}", day=last_draw_day)
            return
        elif latest_draw_day is None:
            # no data, update all
            total_pages = self.MAX_PAGE
        else:
            # update last draw only
            total_pages = 1

        data_rows = self.fetch(total_pages)
        if len(data_rows) > 0:
            database.save_draw_records(data_rows)
        else:
            self._logger.warning('no data fetched, update aborted')

    def fetch(self, total_pages) -> list:
        self._logger.info('start to download data from from {}'.format(
            self.HOST))
        page_num = 1
        payload = {
            "gameNo": "04",
            "provinceId": "0",
            "isVerify": 1,
            "pageNo": 1,
            "pageSize": 30
        }
        data_rows = []
        while page_num <= total_pages:
            payload['pageNo'] = page_num
            resp = requests.get(self.BASE_URL,
                                params=payload,
                                headers=self.HEADERS)
            arr = self._parse(resp)
            if len(arr) == 0:
                break
            data_rows.extend(arr)
            self._logger.info('download page {} done.'.format(resp.url))
            page_num += 1
        self._logger.info('download data done')
        return data_rows

    def _parse(self, resp):
        data = resp.json()
        val = data['value']
        if val['total'] == 0:
            return []
        arr = []
        for l1 in val['list']:
            a = [l1['lotteryDrawTime'], int(l1['lotteryDrawNum'])]
            columns = l1['lotteryDrawResult'].split(' ')
            sum = int(columns[0]) + int(columns[1]) + int(columns[2]) + int(
                columns[3])
            a.append(sum)
            a.extend(columns)
            arr.append(a)
        return tuple(arr)
