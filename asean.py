# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File    : asean.py
# @Desc    : 抓取https://aseanpartner.siemens.com/的信息
# @Author  : liantian
# @Date    : 2023/12/23
import pprint
import uuid
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

service = Service(executable_path=pathlib.Path(__file__).parent.joinpath('msedgedriver.exe').__str__())

options = webdriver.EdgeOptions()

driver = webdriver.Edge(options=options)

driver.get('https://aseanpartner.siemens.com/')

# 定义一个变量select_PartnerType并使用driver的find_element方法找到id为"filterSearchPartner_PartnerType"的元素
# select_PartnerType = Select(driver.find_element(By.ID, "filterSearchPartner_PartnerType"))

# 通过列表推导式将select_PartnerType的选项的文本提取出来并存储在option_list_PartnerType中，跳过第一个选项
# option_list_PartnerType = [o.text for o in select_PartnerType.options][1:]

# 打印option_list_PartnerType
# print(option_list_PartnerType)

# 遍历option_list_PartnerType中的每一个PartnerType
# for PartnerType in option_list_PartnerType:
# 重新定义select_PartnerType并使用driver的find_element方法找到id为"filterSearchPartner_PartnerType"的元素
# select_PartnerType = Select(driver.find_element(By.ID, "filterSearchPartner_PartnerType"))

# 通过可见文本选择相应的选项
# select_PartnerType.select_by_visible_text(PartnerType)

# time.sleep(5)

# 重新定义select_Country并使用driver的find_element方法找到id为"filterSearchPartner_Country"的元素
select_Country = Select(driver.find_element(By.ID, "filterSearchPartner_Country"))

# 通过列表推导式将select_Country的选项的文本提取出来并存储在option_list_select_Country中，跳过第一个选项
option_list_select_Country = [o.text for o in select_Country.options][1:]

# 打印option_list_select_Country
# print(option_list_select_Country)

for country in option_list_select_Country:
    # 重新定义select_Country并使用driver的find_element方法找到id为"filterSearchPartner_Country"的元素
    select_Country = Select(driver.find_element(By.ID, "filterSearchPartner_Country"))

    # 选择国家
    select_Country.select_by_visible_text(country)

    # 延迟5秒
    time.sleep(1)

    # 选择区域
    select_Region = Select(driver.find_element(By.ID, "filterSearchPartner_Region"))

    # 获取除第一个选项之外的所有区域选项的文本
    option_list_select_Region = [o.text for o in select_Region.options][1:]

    for region in option_list_select_Region:
        # 重新定义select_Region并使用driver的find_element方法找到id为"filterSearchPartner_Region"的元素
        select_Region = Select(driver.find_element(By.ID, "filterSearchPartner_Region"))

        # 选择地区
        select_Region.select_by_visible_text(region)

        # 延迟5秒
        time.sleep(1)

        # 选择BU下拉框
        select_BU = Select(driver.find_element(By.ID, "filterSearchPartner_Bu"))
        # 通过可见文本选择'FA (PLC, HMI, SCADA)'选项
        select_BU.select_by_visible_text('FA (PLC, HMI, SCADA)')
        # 等待5秒
        time.sleep(1)



        # 定位搜索按钮
        search_button = driver.find_element(By.XPATH, "//button[contains(text(),'Search')]")
        # 点击搜索按钮
        search_button.click()
        # 打印国家-地区
        print(f'{country}-{region}')
        # 等待5秒
        time.sleep(5)


        entries = driver.find_elements(By.XPATH, "//div[contains(@class,'row item-result')]")

        # 遍历搜索结果列表
        for entry in entries:
            html = entry.get_attribute('innerHTML')  # 获取搜索结果的html代码

            # 使用BeautifulSoup解析html代码
            soup = BeautifulSoup(html, "html.parser")

            # 清除空格并获取搜索结果的子元素
            div = [i for i in list(soup.children) if str(i).strip() != '']

            # 创建一个字典用于存储各字段的值
            e = dict({})

            # 解析各字段的值
            e['Partner Name'] = div[0].text.strip()  # 合作方名称
            e['Business Unit'] = div[1].text.strip()  # 业务部门
            e['Location'] = div[2].text.strip()  # 位置
            e['Contact'] = div[3].text.strip()  # 联系人
            try:
                if div[4].text.strip() == 'Website':
                    e['Website'] = div[4].find('a')['href']  # 网站链接
            except:
                pass
            div2 = [i for i in list(div[5].children) if str(i).strip() != '']  # 获取搜索结果的子元素
            div3 = [i for i in list(div2[0].children) if str(i).strip() != '']  # 获取子元素的子元素
            e['Address'] = div3[1].text.strip()  # 地址
            e['Contact2'] = div3[2].text.strip()  # 联系人2
            e['Region'] = region  # 地区
            e['Country'] = country  # 国家

            # 生成随机的json文件名，并将解析出的数据保存到json文件中
            json_file = pathlib.Path(__file__).parent.joinpath('asean').joinpath(f'{uuid.uuid4()}.json')
            json.dump(e, open(json_file, 'w'))

