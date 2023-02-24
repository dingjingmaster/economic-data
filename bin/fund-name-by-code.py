#!/usr/bin/env python
# -*- coding=utf-8 -*-
import sys
from functions import *
from prettytable import PrettyTable


if __name__ == '__main__':
    if len(sys.argv) != 3:
        exit(-1)

    fundName = sys.argv[1]
    fundSavePath = sys.argv[2]

    table = PrettyTable(['编码', '名称', '类型'])

    fundInfo = read_fun_data(fundSavePath)

    if None is fundInfo:
        print("input file: '{path}' is not exists!".format(path=fundSavePath))

    for iKey in fundInfo:
        p = fundInfo[iKey]
        name = p[0]
        category = p[1]
        if string_similar(name, fundName) > 0.6 or -1 != name.find(fundName):
            table.add_row([iKey[1:], name, category])
    print(table)

