#!/usr/bin/env python
# -*- coding=utf-8 -*-
import sys

import matplotlib.font_manager

from functions import *
import matplotlib.pyplot as plt

if __name__ == '__main__':
    if len(sys.argv) != 2:
        exit(-1)
    fundSavePath = sys.argv[1]

    fundInfo = read_fun_data_as_df(fundSavePath)
    if None is fundInfo:
        print("input file: '{path}' is not exists!".format(path=fundSavePath))
    category = fundInfo.groupby('基金类别').agg(数量=('基金类别', 'count')) \
        .sort_values(by='数量', ascending=False).reset_index('基金类别')

    # 从此处挑选中文字体
    # for font in matplotlib.font_manager.fontManager.ttflist:
    #    print(font.name)
    plt.rcParams["axes.unicode_minus"] = False
    plt.rcParams['font.family'] = 'sans-serif'
    if system_is_linux():
        plt.rcParams["font.sans-serif"] = ['Source Han Mono SC']
    elif system_is_mac():
        plt.rcParams["font.sans-serif"] = ['Songti SC']

    print(category)
    plt.style.use('ggplot')
    plt.figure(figsize=(20, 8))
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.bar(x='基金类别', height='数量', data=category)
    for a, b in zip(range(len(category.基金类别)), category.数量):
        plt.text(a, b, b, ha='center', va='bottom', fontsize=16)
    plt.title('各类型数量', fontdict={'fontsize': 20})
    plt.show()
    exit(0)
