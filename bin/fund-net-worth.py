#!/usr/bin/env python
# -*- coding=utf-8 -*-
import sys
from functions import *


if __name__ == '__main__':
    if len(sys.argv) != 2:
        exit(-1)

    fundCode = sys.argv[1]
    startDate = '2002-01-01'
    endDate = time.strftime('%Y-%m-%d', time.localtime())

    data = get_fund_data(fundCode, per=49, startDate=startDate, endDate=endDate)

    print(data)

    exit(0)
