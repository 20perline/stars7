# download data from the internet
import requests
import csv
import settings
from abc import abstractmethod, ABCMeta


class Database(metaclass=ABCMeta):

    def __init__(self) -> None:
        data_row = self.fetch()
        self.update(data_row)

    @abstractmethod
    def fetch(self) -> list:
        pass

    def update(self, data_row):
        with open(settings.data_path, 'w') as file:
            writer = csv.writer(file)
            writer.writerow(settings.csv_headers)
            writer.writerows(data_row)


class SportDatabase(Database):

    def fetch(self) -> list:

        total_page = 100
        page_num = 1
        page_size = 30
        max_total = 250
        idx = 1
        url_tpl = """https://webapi.sporttery.cn/gateway/lottery/getHistoryPageListV1.qry?gameNo=04&provinceId=0&pageNo={}&pageSize={}&isVerify=1"""

        data_row = []
        while page_num <= total_page:
            url = url_tpl.format(page_num, page_size)
            resp = requests.get(url=url)
            data = resp.json()
            val = data['value']
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
                print('total rows reach maximum {}'.format(max_total))
                break
            print('download page {} done.'.format(page_num))
            page_num += 1

        return data_row


if __name__ == '__main__':
    db = SportDatabase()
