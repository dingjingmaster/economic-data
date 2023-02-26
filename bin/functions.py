import os
import re
import time

import difflib
import datetime
import platform
import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup


def system_is_mac() ->bool:
    return platform.system().lower() == 'darwin'


def system_is_linux() ->bool:
    return platform.system().lower() == 'linux'


def string_similar(s1: str, s2: str) ->float:
    return difflib.SequenceMatcher(None, s1, s2).quick_ratio()


def get_start_date(days: int) ->str:
    # 返回字符串 %Y-%m-%d
    eTime = datetime.datetime.now()
    sTime = eTime - datetime.timedelta(days)
    return sTime.strftime('%Y-%m-%d')


def read_fun_data(path: str):
    f = {}
    if os.path.exists(path):
        try:
            o = pd.read_csv(path, sep='|').values.tolist()
            for line in o:
                f[line[0]] = (line[1], line[2])
            return f
        except Exception as e:
            print(e)
            return None
    return None


def read_fun_data_as_df(path: str):
    if os.path.exists(path):
        try:
            return pd.read_csv(path, sep='|')
        except Exception as e:
            print(e)
            return None
    return None


def get_fund_data(code: str, per=10, startDate='', endDate='', proxies=None):
    def get_url(url, params=None, proxies=None):
        rsp = requests.get(url, params=params, proxies=proxies)
        rsp.raise_for_status()
        return rsp.text
    url = 'http://fund.eastmoney.com/f10/F10DataApi.aspx'
    params = {
        'type': 'lsjz',
        'code': code,
        'page': 1,
        'per': per,
        'sdate': startDate,
        'edate': endDate
    }
    html = get_url(url, params, proxies)
    soup = BeautifulSoup(html, 'html.parser')

    # 总页数
    pattern = re.compile(r'pages:(.*),')
    result = re.search(pattern, html).group(1)
    pages = int(result)

    heads = []
    for head in soup.findAll('th'):
        heads.append(head.contents[0])

    # 数据存取列表
    records = []
    page = 1

    while page <= pages:
        params = {
            'type': 'lsjz',
            'code': code,
            'page': 1,
            'per': per,
            'sdate': startDate,
            'edate': endDate
        }
        html = get_url(url, params, proxies)
        soup = BeautifulSoup(html, 'html.parser')

        # 获取数据
        for row in soup.findAll('tbody')[0].findAll('tr'):
            rowRecords = []
            for r in row.findAll('td'):
                val = r.contents
                if val == []:
                    rowRecords.append(np.nan)
                else:
                    rowRecords.append(val[0])
            records.append(rowRecords)
        # 下一页
        page += 1
    # 数据整理到 dataframe
    df = np.array(records)
    data = pd.DataFrame()
    for c, cName in enumerate(heads):
        data[cName] = df[:, c]
    # print(data)
    return data
