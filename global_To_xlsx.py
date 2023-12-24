#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import xlsxwriter
import pathlib
import json

workbook = xlsxwriter.Workbook(pathlib.Path(__file__).parent.joinpath('global.xlsx'), {'constant_memory': True})
sheet = workbook.add_worksheet()
row = 0

sheet.write(row, 0, '国家')
sheet.write(row, 1, '地区')
sheet.write(row, 2, '合作方名称')
sheet.write(row, 3, 'Expert')
sheet.write(row, 4, '办公地点类型')
sheet.write(row, 5, '办公地点')
sheet.write(row, 6, 'Email')
sheet.write(row, 7, '电话')
sheet.write(row, 8, '网址')
row = 1
for file in pathlib.Path(__file__).parent.joinpath('global').iterdir():
    e = json.load(open(file, 'r', encoding='utf-8') )

    sheet.write(row, 0, e['Country'])
    sheet.write(row, 1, e['Region'])
    sheet.write(row, 2, e['Name'])
    sheet.write(row, 3, e['Expert'])
    sheet.write(row, 4, e['Office Type'])
    sheet.write(row, 5, e['Address'])
    sheet.write(row, 6, e.get('Email',''))
    sheet.write(row, 7, e.get('Phone',''))
    sheet.write(row, 8, e.get('Website',''))
    row += 1
workbook.close()


