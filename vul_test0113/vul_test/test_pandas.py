#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025-01-08 16:54
# @Author  : skilywen
import pandas as pd

df = pd.read_excel('IP1.xlsx')
for index, row in df.iterrows():
    print(row['脚本名'])