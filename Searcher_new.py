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


def signal_type(temp_, total_indices_, CP_td_, OP_td_):
    """
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
    23 前一日收盤價
    24 上一個五日線低點
    25 上一個五日線高點
    26 上上一個五日線低點
    27 上上一個五日線高點
    """
    CP_yd_ = temp_[-1][0]
    avr_5_yd_ = temp_[-1][2]
    avr_20_yd_ = temp_[-1][3]
    avr_60_yd_ = temp_[- 1][17]
    avr_5_td_ = 0
    avr_20_td_ = 0
    avr_60_td_ = 0
    for i_ in range(4):
        avr_5_td_ = avr_5_td_ + temp_[-i - 1][0] / 5
    avr_5_td_ = avr_5_td_ + CP_td_ / 5
    for i_ in range(19):
        avr_20_td_ = avr_20_td_ + temp_[-i - 1][0] / 20
    avr_20_td_ = avr_20_td_ + CP_td_ / 20
    for i_ in range(59):
        avr_60_td_ = avr_60_td_ + temp_[-i - 1][0] / 60
    avr_60_td_ = avr_60_td_ + CP_td_ / 60

    slope_5_yd_ = temp_[- 1][6]
    last_low_ = temp_[-1][24]
    last_high_ = temp_[-1][25]
    last_last_low_ = temp_[-1][26]
    last_last_high_ = temp_[-1][27]
    vol = temp_[-1][12]
    body_ = CP_td_ - OP_td

    if avr_5_td_ > avr_20_td_ > avr_60_td_:
        align_t_ = '5>20>60'
    elif avr_5_td_ > avr_60_td_ > avr_20_td_:
        align_t_ = '5>60>20'
    elif avr_60_td_ > avr_5_td_ > avr_20_td_:
        align_t_ = '60>5>20'
    elif avr_60_td_ > avr_20_td_ > avr_5_td_:
        align_t_ = '60>20>5'
    elif avr_20_td_ > avr_60_td_ > avr_5_td_:
        align_t_ = '20>60>5'
    elif avr_20_td_ > avr_5_td_ > avr_60_td_:
        align_t_ = '20>5>60'
    else:
        align_t_ = '0'

    if avr_5_yd_ > avr_20_yd_ > avr_60_yd_:
        align_y_ = '5>20>60'
    elif avr_5_yd_ > avr_60_yd_ > avr_20_yd_:
        align_y_ = '5>60>20'
    elif avr_60_yd_ > avr_5_yd_ > avr_20_yd_:
        align_y_ = '60>5>20'
    elif avr_60_yd_ > avr_20_yd_ > avr_5_yd_:
        align_y_ = '60>20>5'
    elif avr_20_yd_ > avr_60_yd_ > avr_5_yd_:
        align_y_ = '20>60>5'
    elif avr_20_yd_ > avr_5_yd_ > avr_60_yd_:
        align_y_ = '20>5>60'
    else:
        align_y_ = '0'

    if avr_5_yd_ > last_low_:
        last_ = '>LastLow'
    elif avr_5_yd_ > last_last_high_:
        last_ = '>Last2High'
    elif avr_5_yd_ < last_high_:
        last_ = '<LastHigh'
    elif avr_5_yd_ < last_last_low_:
        last_ = '<Last2low'
    else:
        last_ = 'LastNone'

    if slope_5_yd_ >= 0:
        slope_ = 'slp>0'
    else:
        slope_ = 'slp<0'

    if vol > 2000:
        if CP_yd_ < avr_5_yd_ and CP_td_ - avr_5_td_ > abs(OP_td_ - avr_5_td_) and body_ > 0:
            name_ = 'Body+'
        elif CP_yd_ < avr_5_yd_ and CP_yd_ < avr_20_yd_ and CP_td_ > avr_5_td_ \
                and CP_td_ > avr_20_td_ and vol > 2000 and body_ > 0:
            name_ = 'Body2+'
        elif CP_yd_ > avr_5_yd_ and avr_5_td_ - CP_td_ > abs(OP_td_ - avr_5_td_) and vol > 2000 \
                and body_ < 0:
            name_ = 'Body-'
        elif CP_yd_ > avr_5_yd_ and CP_yd_ > avr_20_yd_ and CP_td_ < avr_5_td_ \
                and CP_td_ < avr_20_td_ and vol > 2000 and body_ < 0:
            name_ = 'Body2-'
        else:
            name_ = 'None'

    rank5 = 0
    rank10 = 0
    rank20 = 0
    rank30 = 0
    rank60 = 0
    rank_total = 0
    for j_ in range(1, len(total_indices_[:])):
        if total_indices_[j_][0] == name_ and total_indices_[j_][2] == last_ and total_indices_[j_][3] == align_y_ \
                and total_indices_[j_][4] == align_t_ and total_indices_[j_][5] == slope_:
            rank5 = total_indices_[j_][19]
            rank10 = total_indices_[j_][20]
            rank20 = total_indices_[j_][21]
            rank30 = total_indices_[j_][22]
            rank60 = total_indices_[j_][23]
            rank_total = total_indices_[j_][24]

    return [name_, last_, slope_, align_t_, align_y_, avr_5_td_, rank5, rank10, rank20, rank30, rank60, rank_total]


tic = time.perf_counter()
now = datetime.now()  # current date and time

year = now.strftime("%Y")
year = str(int(year) - 1911)
month = now.strftime("%m")
day = now.strftime("%d")

date_ = year + '/' + month + '/' + day
print(date_)

# setup the webdriver
PATH = "C:\Program Files (x86)\chromedriver.exe"

options = webdriver.ChromeOptions()
options.add_argument("headless")
driver = webdriver.Chrome(PATH, options=options)

stock_list = []
with open('./stock_data/ALL_value.csv') as csv_file:
    rows = csv.reader(csv_file, delimiter=',')
    data = list(rows)

for i in range(1, len(data[:])):
    if float(data[i][3]) > 5000000:
        stock_list.append(data[i][0])

print(stock_list)

bird = []
body_up = []
body_down_up = []
body_over = []
i = 0
input_list = ['stock', 'type', 'last', 'slope', 'align_t', 'align_y', 'avr5', 'OP', 'CP', 'r5', 'r10', 'r20', 'r30', 'r60', 'r_total']

TOE = 0
NSE = 0
file_date = year + '_' + month + '_' + day
Negative_list = []

total_indices = []
with open('./Comparison/Total_list.csv') as csvfile:
    reader = csv.reader(csvfile)  # change contents to floats
    # each row is a list
    for row in reader:
        total_indices.append(row)

i = 0
while os.path.isfile('./stock_search_purchase/' + file_date + '_' + str(i) + '.csv'):
    i = i + 1
with open('./stock_search_purchase/' + file_date + '_' + str(i) + '.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(input_list)
    for stock in stock_list:
        if os.path.isfile('./stock_data/DATA/DATA_' + stock + '.csv'):
            print(stock)
            temp = []
            with open('./stock_data/DATA/DATA_' + stock + '.csv') as csvfile:
                reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)  # change contents to floats
                # each row is a list
                for row in reader:
                    temp.append(row)
            if int((temp[- 1][12] + temp[- 2][12])) / 2 > 4000 and len(temp[:]) > 301:
                print(int((temp[- 1][12] + temp[- 2][12])) / 2)
                delay = 3  # seconds
                try:
                    driver.get("https://invest.cnyes.com/twstock/TWS/" + stock + "/overview")
                    myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="_profile-TWS:' + stock + ':STOCK"]/div[2]/div[2]/div[5]/div[2]')))
                    # print("Page is ready!")
                    OP_td = float(driver.find_element_by_xpath(
                        '//*[@id="_profile-TWS:' + stock + ':STOCK"]/div[2]/div[2]/div[5]/div[2]').text.replace('--',
                                                                                                                '0').replace(
                        ',', ''))
                    CP_td = float(driver.find_element_by_xpath(
                        '//*[@id="_profile-TWS:' + stock + ':STOCK"]/div[1]/div[3]/div[1]/div/span').text.replace('--',
                                                                                                                  '0').replace(
                        ',', ''))
                    [name, last, slope, align_t, align_y, avr_5_td, r5, r10, r20, r30, r60, r_total] = signal_type(temp, total_indices, CP_td, OP_td)
                    writer.writerow([stock, name, last, slope, align_t, align_y, avr_5_td, OP_td, CP_td, r5, r10, r20, r30, r60, r_total])
                    print([stock, name, last, slope, align_t, align_y, avr_5_td, OP_td, CP_td, r5, r10, r20, r30, r60, r_total])

                except TimeoutException:
                    print("Loading took too much time!")
                    TOE = TOE + 1
                except NoSuchElementException:
                    print("No Such Element Exception!")
                    NSE = NSE + 1

toc = time.perf_counter()
print('TOE' + str(TOE))
print('NSE' + str(NSE))
print(f"Downloaded the tutorial in {(toc - tic) / 60:0.4f} mins")

win32api.MessageBox(0, 'Finished', 'Reminder', 0x00001000)
