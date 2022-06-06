from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import random
from datetime import datetime
from ToolBox import write2csv
from ToolBox import text2list
import os.path
from os import path
import time
import re
from ToolBox import write2text
import csv
import codecs

tic = time.perf_counter()
now = datetime.now() # current date and time

year = now.strftime("%Y")
year = str(int(year)-1911)
month = now.strftime("%m")
day = now.strftime("%d")

date_ = year + '/' + month + '/' + day
print(date_)

# setup the webdriver
PATH = "C:\Program Files (x86)\chromedriver.exe"

options = webdriver.ChromeOptions()
options.add_argument("headless")
driver = webdriver.Chrome(PATH, options=options)

file_date = year + '_' + month + '_' + day
Interest_list = ['stock', 'stop date Year', 'stop date Month', 'stop date Day', 'reason', 'short percentage', 'short/borrow', 'Big buyer', 'remaining days']

driver.get("https://www.twse.com.tw/zh/page/trading/exchange/MI_MARGN.html")
time.sleep(3)

type_stock = driver.find_element_by_xpath('//*[@id="main-form"]/div/div/form/select')

with codecs.open('./stock_data/stock_class1.csv', 'w', encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    for i in range(7, 38):
        data = []
        type_stock.click()
        time.sleep(1)
        stock_type = driver.find_element_by_xpath('//*[@id="main-form"]/div/div/form/select/option[' + str(i) + ']')
        print(stock_type.text)
        data.append(stock_type.text)
        stock_type.click()
        time.sleep(1)
        button = driver.find_element_by_xpath('//*[@id="main-form"]/div/div/form/a')
        button.click()
        time.sleep(3)

        showAll = driver.find_element_by_xpath('//*[@id="report-table_length"]/label/select')
        showAll.click()
        time.sleep(1)
        All = driver.find_element_by_xpath('//*[@id="report-table_length"]/label/select/option[5]')
        All.click()
        time.sleep(1)

        list_len = len(driver.find_elements_by_xpath('//*[@id="report-table"]/tbody/tr'))
        for j in range(2, list_len):
            stock_num = driver.find_element_by_xpath('//*[@id="report-table"]/tbody/tr[' + str(j) + ']/td[1]').text
            data.append(stock_num)
            print(stock_num)
        writer.writerow([item.encode('utf8') for item in data])


num_List = len(driver.find_elements_by_xpath('//*[@id="report-table"]/tbody/tr'))
data = []
