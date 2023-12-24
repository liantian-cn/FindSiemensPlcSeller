#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import xlsxwriter
import pathlib
import json

workbook = xlsxwriter.Workbook(pathlib.Path(__file__).parent.joinpath('asean.xlsx'), {'constant_memory': True})
sheet = workbook.add_worksheet()
row = 0

sheet.write(row, 0, '国家')
sheet.write(row, 1, '地区')
sheet.write(row, 2, '合作方名称')
sheet.write(row, 3, '位置')
sheet.write(row, 4, '联系人')
sheet.write(row, 5, '联系人2')
sheet.write(row, 6, '网站链接')
sheet.write(row, 7, '地址')
sheet.write(row, 8, '业务')
row = 1
for file in pathlib.Path(__file__).parent.joinpath('asean').iterdir():
    e = json.load(open(file, 'r', encoding='utf-8') )

    sheet.write(row, 0, e['Country'])
    sheet.write(row, 1, e['Region'])
    sheet.write(row, 2, e['Partner Name'])
    sheet.write(row, 3, e['Location'])
    sheet.write(row, 4, e['Contact'])
    sheet.write(row, 5, e['Contact2'])
    sheet.write(row, 6, e.get('Website',''))
    sheet.write(row, 7, e['Address'])
    sheet.write(row, 8, e['Business Unit'])
    row += 1
workbook.close()


