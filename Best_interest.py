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
import win32api

tic = time.perf_counter()
now = datetime.now()  # current date and time

year = now.strftime("%Y")
year = str(int(year) - 1911)
month = now.strftime("%m")
day = now.strftime("%d")

date_ = year + '/' + month + '/' + day
print(date_)

Class = []
with open('./stock_data/stock_class.csv') as csvfile:
    reader = csv.reader(csvfile)  # change contents to floats
    # each row is a list
    for row in reader:
        Class.append(row)


def search_class(num, c):
    for i_ in range(31):
        for j_ in range(len(c[i_][:])):
            if num == c[i_][j_]:
                return i_


# setup the webdriver
PATH = "C:\Program Files (x86)\chromedriver.exe"

options = webdriver.ChromeOptions()
options.add_argument("headless")
driver = webdriver.Chrome(PATH, options=options)

i = 0

'''
0 收盤價
1 開盤價
2 5日均價
3 20日均價
4 收盤價近1日趨勢
5 開盤價近1日趨勢
6 5日均價近1日趨勢
7 20日均價近1日趨勢
8 最高價
9 最低價
10 最高價近1日趨勢
11 最低價近1日趨勢
12 成交股數
13 成交筆數
14 日期 (年/月/日)
15 日期 (月)
16 日期 (日)
17 60日均價
18 100日均價
19 300日均價
20 60日均價趨勢
21 100日均價趨勢
22 300日均價趨勢

'''
TOE = 0
NSE = 0
file_date = year + '_' + month + '_' + day
Interest_list = ['stock', 'stop date Year', 'stop date Month', 'stop date Day', 'reason', 'avr_deal', 'short > 500', 'borrow',
                 'short percentage %', 'short / borrow > 30%', 'Big buyer percentage > 40%', 'remaining days', 'CP_td']

driver.get("https://www.twse.com.tw/zh/page/trading/exchange/BFI84U.html")
time.sleep(2)

showAll = driver.find_element_by_xpath('//*[@id="report-table_length"]/label/select')
showAll.click()
time.sleep(1)
All = driver.find_element_by_xpath('//*[@id="report-table_length"]/label/select/option[5]')
All.click()
time.sleep(2)

num_List = len(driver.find_elements_by_xpath('//*[@id="report-table"]/tbody/tr'))
data = [[0] * 13 for i in range(num_List)]
print(num_List)
for i in range(num_List):
    stop_date = driver.find_element_by_xpath('//*[@id="report-table"]/tbody/tr[' + str(i + 1) + ']/td[3]').text.split(
        '.')
    stock = driver.find_element_by_xpath('//*[@id="report-table"]/tbody/tr[' + str(i + 1) + ']/td[1]').text
    data[i][0] = stock
    data[i][1] = (stop_date[0])  # stop_date year
    data[i][2] = (stop_date[1])  # stop_date month
    data[i][3] = (stop_date[2])  # stop_date day
    remain_day = (int(data[i][1]) - int(year)) * 365 + (int(data[i][2]) - int(month)) * 30 + (
                int(data[i][3]) - int(day))
    data[i][11] = remain_day
    reason = driver.find_element_by_xpath('//*[@id="report-table"]/tbody/tr[' + str(i + 1) + ']/td[5]').text
    if reason == '除息' or reason == '除權息':
        data[i][4] = 'interest'
    elif reason == '現金增資':
        data[i][4] = 'increase cash'
    else:
        data[i][4] = 'other reason'

for i in range(num_List):
    print(i)
    if data[i][11] > 4:
        print(data[i][0])
        # 取得五日平均交易量
        avr_deal = 0
        stock = data[i][0]
        if os.path.isfile('./stock_data/DATA/DATA_' + str(data[i][0]) + '.csv'):
            with open('./stock_data/DATA/DATA_' + str(data[i][0]) + '.csv') as csvfile:
                reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)  # change contents to floats
                temp = []
                for row in reader:
                    temp.append(row)
                deal = 0
                for j in range(-1, -6, -1):
                    deal += float(temp[j][12])
                data[i][12] = temp[-1][0]  # CP
                avr_deal = deal / 5
        data[i][5] = avr_deal
        print('CP = ' + str(data[i][12]))
        print('average = ' + str(data[i][5]))

        delay = 1.5  # seconds
        try:
            driver.get('https://invest.cnyes.com/twstock/TWS/' + str(data[i][0]) + '/holders/category')
            time.sleep(1)
            myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="anue-ga-wrapper"]/div[3]/div[3]/section/div[3]/table/tbody/tr[5]/td[3]')))
            big_percentage = driver.find_element_by_xpath(
                '//*[@id="anue-ga-wrapper"]/div[3]/div[3]/section/div[3]/table/tbody/tr[5]/td[3]').text
            data[i][10] = big_percentage
            print('BP = ' + big_percentage)
        except TimeoutException:
            print("Loading took too much time!")
            data[i][10] = -1
        except NoSuchElementException:
            print("No Such Element Exception!")
            data[i][10] = -1

        try:
            driver.get("https://invest.cnyes.com/twstock/TWS/" + str(data[i][0]) + "/holders/margin")
            time.sleep(1)
            myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="_marginDataTable"]/div/div[2]/table/tbody/tr[1]/td[8]')))
            stock_short = driver.find_element_by_xpath(
                '//*[@id="_marginDataTable"]/div/div[2]/table/tbody/tr[1]/td[8]').text.replace(',', '')
            stock_borrow = driver.find_element_by_xpath(
                '//*[@id="_marginDataTable"]/div/div[2]/table/tbody/tr[1]/td[4]').text.replace(',', '')
            data[i][6] = float(stock_short)
            data[i][7] = float(stock_borrow)
            print('short = ' + str(stock_short))
            print('borrow = ' + str(stock_borrow))
        except TimeoutException:
            print("Loading took too much time!")
            data[i][6] = -1
            data[i][7] = -1
        except NoSuchElementException:
            print("No Such Element Exception!")
            data[i][6] = -1
            data[i][7] = -1

        if data[i][5] != 0:
            data[i][8] = data[i][6] / data[i][5] * 100
        else:
            data[i][8] = -1
        if data[i][7] != 0:
            data[i][9] = data[i][6] / data[i][7] * 100
        else:
            data[i][9] = -1

with open('./stock_search_purchase/Best_interest_' + file_date + '.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(Interest_list)
    for i in range(num_List):
        writer.writerow(data[i])


toc = time.perf_counter()
print(f"Downloaded the tutorial in {(toc - tic) / 60:0.4f} mins")
win32api.MessageBox(0, 'Finished', 'Reminder', 0x00001000)
