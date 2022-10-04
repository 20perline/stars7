# download data from the internet
import requests
import csv
import os
import settings

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

header = ['day', 'num', 'c0', 'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7']

dir_path = os.path.dirname(os.path.realpath(__file__))

with open(settings.data_path, 'w') as file:
    writer = csv.writer(file)
    writer.writerow(header)
    writer.writerows(data_row)
