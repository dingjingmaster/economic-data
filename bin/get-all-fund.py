#!/usr/bin/env python
# -*- coding=utf-8 -*-
import re
import os
import sys
import requests
import pandas as pd

from functions import *


fundInfo = {}
URL = 'http://fund.eastmoney.com/js/fundcode_search.js'


def save_fund_data(new: dict, path: str):
    code = []
    name = []
    category = []
    for iKey in new:
        code.append(iKey)
        name.append(new[iKey][0])
        category.append(new[iKey][1])
    df = pd.DataFrame({'基金代码': code, '基金名称': name, '基金类别': category})
    df.to_csv(path, index=False, sep='|')
    return


def union_fun_data(old: dict, new: dict):
    for iKey in old:
        if iKey not in new:
            new[iKey] = old[iKey]
        else:
            o = old[iKey]
            n = new[iKey]
            if n[0] != o[0]:
                name = n[0]
                if len(n[0]) < len(o[0]):
                    name = n[0]
                else:
                    name = o[0]
                new[iKey] = (name, n[1])
            elif n[1] != o[1]:
                print('信息变更(old) -- 基金代码:"{code}", 基金名称:"{name}", 基金类别:"{category}"'.format(code=iKey, name=o[0], category=o[1]))
                print('信息变更(new) -- 基金代码:"{code}", 基金名称:"{name}", 基金类别:"{category}"'.format(code=iKey, name=n[0], category=n[1]))
    return new


if __name__ == '__main__':
    if len(sys.argv) != 2:
        exit(-1)
    fundSavePath = sys.argv[1]

    reqGet = requests.get(URL)
    fundContent = re.findall(r'"(\d*?)","(.*?)","(.*?)","(.*?)","(.*?)"', reqGet.text)

    for it in fundContent:
        c = list(it)
        # 0:基金代码; 2:表示基金名称; 3:表示基金类型
        if '' == c[0] or '' == c[2] or '' == c[3]:
            continue
        fundInfo['J' + c[0].strip()] = (c[2].strip(), c[3].strip())

    fundOldInfo = read_fun_data(fundSavePath)
    if None is not fundOldInfo:
        print("历史基金数  : {size}".format(size=len(fundOldInfo)))
        fundInfo = union_fun_data(fundOldInfo, fundInfo)
    print("新获取基金数: {size}".format(size=len(fundInfo)))
    save_fund_data(fundInfo, fundSavePath)

    exit(0)
