#!/usr/bin/env python
# -*- coding=utf-8 -*-
import sys

import matplotlib
import matplotlib.pyplot as plt

from functions import *


if __name__ == '__main__':
    if len(sys.argv) < 3:
        exit(-1)

    fundCode = sys.argv[1]
    saveDir = sys.argv[2]
    startDate = '2002-01-01'
    days = -1
    if len(sys.argv) >= 4:
        try:
            days = int(sys.argv[3])
            startDate = get_start_date(days)
        except Exception as e:
            days = -1

    endDate = time.strftime('%Y-%m-%d', time.localtime())

    savePath = "{dataDir}/{fundCode}.csv".format(dataDir=saveDir, fundCode=fundCode)

    data = get_fund_data(fundCode, per=46, startDate=startDate, endDate=endDate)
    if -1 == days:
        oldData = read_fun_data_as_df(savePath)
        if None is not oldData:
            data = pd.concat([data, oldData])
            data.drop_duplicates(subset='净值日期', keep='first', inplace=True, ignore_index=True)
    data.to_csv(savePath, index=False, sep='|')

    rateBase = 0    # 增长率基准
    # print(data)
    # https://blog.csdn.net/u012710043/article/details/111590428#:~:text=1.%E8%8E%B7%E5%8F%96%E6%89%80%E6%9C%89%E7%A7%8D%E7%B1%BB%E5%9F%BA%E9%87%91%E6%95%B0%E6%8D%AE,1.1%E5%AF%BC%E5%85%A5%E7%9B%B8%E5%85%B3%E5%8C%85%201.2%E9%80%9A%E8%BF%87%E5%A4%A9%E5%A4%A9%E5%9F%BA%E9%87%91%E7%BD%91%E6%8E%A5%E5%8F%A3%E8%8E%B7%E5%8F%96%E5%9F%BA%E9%87%91%E6%95%B0%E6%8D%AE
    data['净值日期'] = pd.to_datetime(data['净值日期'], format='%Y-%m-%d')
    data['单位净值'] = data['单位净值'].astype(float)
    data['累计净值'] = data['累计净值'].astype(float)
    data['日增长率'] = data['日增长率'].str.strip('%').astype(float)
    data['基准值'] = rateBase

    # 按照日期升序排序并重建索引
    data = data.sort_values(by='净值日期', axis=0, ascending=True).reset_index(drop=True)

    vDate = data['净值日期']
    vAsset = data['单位净值']
    vAN = data['累计净值']
    vDailyRate = data['日增长率']
    vDailyBase = data['基准值']

    # 从此处挑选中文字体
    # for font in matplotlib.font_manager.fontManager.ttflist:
    #    print(font.name)
    plt.rcParams["axes.unicode_minus"] = False
    plt.rcParams['font.family'] = 'sans-serif'
    if system_is_linux():
        plt.rcParams["font.sans-serif"] = ['Source Han Mono SC']
    elif system_is_mac():
        plt.rcParams["font.sans-serif"] = ['Songti SC']

    # 做图
    fig = plt.figure(figsize=(16, 10))

    #
    ax1 = fig.add_subplot(211)
    ax1.plot(vDate, vAsset, label='基金净值')
    ax1.plot(vDate, vAN, label='累计净值')
    ax1.set_ylabel('净值数据')
    ax1.set_xlabel('日期')
    plt.legend(loc='upper left')

    #
    ax2 = fig.add_subplot(212)
    ax2.plot(vDate, vDailyRate, 'r', label='日增长率')
    ax2.plot(vDate, vDailyBase, 'b', label='增长率基准值')
    ax2.set_ylabel('日增长率(%)')
    plt.legend(loc='upper right')
    plt.title('基金净值数据')

    plt.show()

    exit(0)
