# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File    : globe.py
# @Desc    : 抓取https://www.partnerfinder.automation.siemens.com/s/siemens-partner-finder?language=en_US的信息
# @Author  : liantian
# @Date    : 2023/12/24
import pprint
import uuid
import re
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import pathlib



# 设置Edge驱动程序的路径
service = Service(executable_path=pathlib.Path(__file__).parent.joinpath('msedgedriver.exe').__str__())

# 创建Edge浏览器的选项对象
options = webdriver.EdgeOptions()

options.add_argument("--start-maximized")


# 创建Edge浏览器对象并设置选项
driver = webdriver.Edge(options=options)

# 打开指定的网页
driver.get('https://www.partnerfinder.automation.siemens.com/s/siemens-partner-finder?language=en_US')

print("请手动选择基础信息")
time.sleep(30)

country_list = open('country_list.txt', 'r', encoding='utf-8').readlines()

for country in country_list:
    country = country.strip()
    print(country)

    # 定位到id为'countryId-2'的元素
    country_input = driver.find_element(By.XPATH, "//*[@id='countryId-2']")
    # 清空元素的值
    country_input.clear()
    # 向元素中输入国家名称
    country_input.send_keys(country)
    # 程序暂停1秒
    time.sleep(1)

    # 定位到包含文本为"Main & Regional Offices"的元素
    radio_office_type = driver.find_element(By.XPATH, "//span[contains(text(),'Main & Regional Offices')]")

    # 点击定位到的元素
    radio_office_type.click()

    # 程序暂停1秒
    time.sleep(1)

    # 定位搜索按钮并点击
    search_button = driver.find_element(By.XPATH,"//*[@id='searchbuttonAction-2']")
    search_button.click()
    time.sleep(10)

    # 定位并获取所有卖家列表的div元素
    div_seller_list = driver.find_elements(By.XPATH, "//*[@class='slds-col slds-size_1-of-1 slds-border_top slds-grid slds-wrap mobileborderwrap slds-p-around_small slds-grid_vertical-stretch c-container']")

    for div_seller in div_seller_list:
        div_seller_dict = dict({})

        div_div_seller = div_seller.find_elements(By.TAG_NAME, "div")

        company_logo_div = div_div_seller[0]

        name_div = div_div_seller[1]
        name_text = name_div.text
        name_text_list = name_text.splitlines()

        if name_text_list[0].upper().startswith('EXPERT'):
            div_seller_dict['Expert'] = True
            name_text_list.pop(0)
        else:
            div_seller_dict['Expert'] = False

        if len(name_text_list) > 0:
            div_seller_dict['Name'] = name_text_list[0]
            name_text_list.pop(0)

        if len(name_text_list) > 0:
            div_seller_dict['Office Type'] = name_text_list[0]
            name_text_list.pop(0)

        if len(name_text_list) > 0:
            div_seller_dict['Region'] = name_text_list[0]
            name_text_list.pop(0)

        div_seller_dict['Country'] = country

        if len(name_text_list) > 0:
            div_seller_dict['Address'] = name_text_list[0]
            name_text_list.pop(0)

        contact_div = div_div_seller[2]

        extract_email_pattern = r"\S+@\S+\.\S+"
        find_all = re.findall(extract_email_pattern, contact_div.text, re.M)
        div_seller_dict['Email'] = ";".join(find_all)

        extract_phone_pattern = "\\+?\\d{1,4}?[-.\\s]?\\(?\\d{1,3}?\\)?[-.\\s]?\\d{1,4}[-.\\s]?\\d{1,4}[-.\\s]?\\d{1,9}"
        find_all = re.findall(extract_phone_pattern, contact_div.text, re.M)
        div_seller_dict['Phone'] = ";".join(find_all)

        url_extract_pattern = "https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)"
        find_all = re.findall(url_extract_pattern, contact_div.text, re.M)
        div_seller_dict['Website'] = ";".join(find_all)

        # 生成随机的json文件名，并将解析出的数据保存到json文件中
        json_file = pathlib.Path(__file__).parent.joinpath('global').joinpath(f'{uuid.uuid4()}.json')
        json.dump(div_seller_dict, open(json_file, 'w'))









