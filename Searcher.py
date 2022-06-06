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

stock_list = []
with open('./stock_data/ALL_value.csv') as csv_file:
    rows = csv.reader(csv_file, delimiter=',')
    data = list(rows)

for i in range(1, len(data[:])):
    if float(data[i][3]) > 5000000:
        stock_list.append(data[i][0])
#stock_list = text2list('ALL.txt')
print(stock_list)

bird = []
body_up = []
body_down_up = []
body_over = []
i = 0

input_list = ['Type_name', 'stock', 'CP_upper', 'CP_lower', 'OP_td', 'CP_yd', 'OP_yd', '5D', '20D', 'CP_slope',
              'OP_slope', '5D_slope', '20D_slope', 'HP', 'LP', 'HP_slope', 'LP_slope', 'Quantity', 'Deal', 'Year',
              'Month', 'Date', '60D', '100D', '300D', '60D_slope', '100D_slope', '300D_slope', 'CP_yd', 'Last5low',
              'Last5high', 'LastLast5low', 'LastLast5high', 'condition']
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
23 前一日收盤價
24 上一個五日線低點
25 上一個五日線高點
26 上上一個五日線低點
27 上上一個五日線高點
'''
TOE = 0
NSE = 0
file_date = year + '_' + month + '_' + day
Negative_list = []


i = 0
while os.path.isfile('./stock_search_purchase/' + file_date + '_' + str(i) + '.csv'):
    i = i+1
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
            if int(temp[len(temp[:])-1][12]) > 4000 and len(temp[:]) > 301:  # and 350 > int(temp[len(temp[:])-1][0]) > 10:
                print(temp[len(temp[:]) - 1][12])
                data = [0] * 301
                date_list = [0] * 301
                for i in range(301):
                    data[i] = temp[len(temp[:])-(301-i)][0]
                    date_list[i] = temp[len(temp[:])-(301-i)][16]

                delay = 3  # seconds
                try:
                    driver.get("https://invest.cnyes.com/twstock/TWS/" + stock + "/overview")
                    myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="_profile-TWS:' + stock + ':STOCK"]/div[2]/div[2]/div[5]/div[2]')))
                    #print("Page is ready!")
                    OP_td = float(driver.find_element_by_xpath(
                        '//*[@id="_profile-TWS:' + stock + ':STOCK"]/div[2]/div[2]/div[5]/div[2]').text.replace('--',
                                                                                                                '0').replace(
                        ',', ''))

                    CP_yd = float(temp[len(temp[:]) - 1][0])
                    CP_yyd = float(temp[len(temp[:]) - 2][0])
                    OP_yd = float(temp[len(temp[:]) - 1][1])
                    OP_yyd = float(temp[len(temp[:]) - 2][1])

                    #print(len(data[len(data) - 20:len(data)]))
                    avr_300_yyd = temp[len(temp[:]) - 2][19]
                    avr_300_yd = temp[len(temp[:])-1][19]
                    avr_300_td = sum(data[len(data) - 299:len(data)]) / 300
                    avr_100_yyd = temp[len(temp[:]) - 2][18]
                    avr_100_yd = temp[len(temp[:])-1][18]
                    avr_100_td = sum(data[len(data) - 99:len(data)]) / 100
                    avr_60_yyd = temp[len(temp[:]) - 2][17]
                    avr_60_yd = temp[len(temp[:])-1][17]
                    avr_60_td = sum(data[len(data) - 59:len(data)]) / 60
                    print(len(data[len(data) - 59:len(data)]))
                    print(data[len(data) - 59:len(data)])
                    avr_20_yyd = temp[len(temp[:]) - 2][3]
                    avr_20_yd = temp[len(temp[:])-1][3]
                    avr_20_td = sum(data[len(data) - 19:len(data)]) / 20
                    avr_5_yyd = temp[len(temp[:]) - 2][2]
                    avr_5_yd = temp[len(temp[:])-1][2]
                    avr_5_td = sum(data[len(data) - 4:len(data)]) / 5

                    threshold = 1.1
                    x = CP_yd * threshold

                    a5_td = avr_5_td + CP_yd * 1.04 / 5
                    a20_td = avr_20_td + CP_yd * 1.04 / 20
                    a60_td = avr_60_td + CP_yd * 1.04 / 60

                    x_lower = CP_yd

                    last_low = temp[len(temp[:]) - 1][24]
                    last_high = temp[len(temp[:]) - 1][25]
                    last_last_low = temp[len(temp[:]) - 1][26]
                    last_last_high = temp[len(temp[:]) - 1][27]

                    '''因為NON的狀況下會有較多的不確定性，在準PPP的條件達成後的趨勢較為穩定可靠。另外也提供高/低於上一個低/高點的半身'''

                    if avr_20_yd > avr_5_yd and avr_5_td + x/5 > avr_20_td + x/20:
                        x_lower = (avr_20_td - avr_5_td) * 20 / 3
                        if OP_td < x_lower < CP_yd * 1.1:  #CP_yd * 0.9 <
                            writer.writerow(
                                ["1_+bird_5_20", stock, x, x_lower, OP_td] + temp[len(temp[:])-1] + [1])
                    elif avr_60_yd > avr_5_yd > avr_20_yd and avr_5_td + x/5 > avr_60_td + x/60:
                        x_lower = (avr_60_td - avr_20_td) * 30
                        if OP_td < x_lower < CP_yd * 1.1:  #CP_yd * 0.9 <
                            writer.writerow(
                                ["1_+bird_5_60", stock, x, x_lower, OP_td] + temp[len(temp[:])-1] + [1])

                    elif CP_yd <= float(avr_5_yd) <= x and avr_5_yd >= avr_20_yd >= avr_60_yd:
                        x_lower = OP_td
                        if OP_td > float(avr_5_yd):
                            x_lower = OP_td
                        else:
                            x_lower = float(avr_5_yd) + abs(float(avr_5_yd) - OP_td)
                        if x_lower < x:
                            writer.writerow(
                                ["2_+body_5_20_60", stock, x, x_lower, OP_td] + temp[len(temp[:]) - 1] + [1])
                    elif CP_yd <= float(avr_5_yd) <= x and avr_5_yd >= avr_20_yd and avr_5_yd > last_low:
                        x_lower = OP_td
                        if OP_td > float(avr_5_yd):
                            x_lower = OP_td
                        else:
                            x_lower = float(avr_5_yd) + abs(float(avr_5_yd) - OP_td)
                        if x_lower < x:
                            writer.writerow(
                                ["2_+body_5_20", stock, x, x_lower, OP_td] + temp[len(temp[:]) - 1] + [1])
                    elif CP_yd <= float(avr_5_yd) <= x and avr_5_yd >= avr_20_yd and avr_5_yd > last_low:
                        x_lower = OP_td
                        if OP_td > float(avr_5_yd):
                            x_lower = OP_td
                        else:
                            x_lower = float(avr_5_yd) + abs(float(avr_5_yd) - OP_td)
                        if x_lower < x:
                            writer.writerow(
                                ["2_+body_5", stock, x, x_lower, OP_td] + temp[len(temp[:]) - 1] + [1])
                    elif CP_yd >= float(avr_5_yd) >= CP_yd * 0.9 and avr_60_yd < avr_5_yd < avr_20_yd and OP_td < last_high:
                        x_upper = OP_td
                        if OP_td < float(avr_5_yd):
                            x_upper = OP_td
                        else:
                            x_upper = float(avr_5_yd) - abs(float(avr_5_yd) - OP_td)
                        if x_upper > CP_yd * 0.9:
                            writer.writerow(
                                ["4_-body_20_5_60_down hill", stock, x, x_upper, OP_td] + temp[len(temp[:])-1] + [2])
                    elif CP_yd >= float(avr_5_yd) >= CP_yd * 0.9 and avr_5_yd < avr_20_yd and avr_5_yd < last_high:
                        x_upper = OP_td
                        if OP_td < float(avr_5_yd):
                            x_upper = OP_td
                        else:
                            x_upper = float(avr_5_yd) - abs(float(avr_5_yd) - OP_td)
                        if x_upper > CP_yd * 0.9:
                            writer.writerow(
                                ["4_-body_20_5", stock, x, x_upper, OP_td] + temp[len(temp[:])-1] + [2])
                    elif CP_yd >= float(avr_5_yd) >= CP_yd * 0.9 and avr_5_yd < last_high:
                        x_upper = OP_td
                        if OP_td < float(avr_5_yd):
                            x_upper = OP_td
                        else:
                            x_upper = float(avr_5_yd) - abs(float(avr_5_yd) - OP_td)
                        if x_upper > CP_yd * 0.9:
                            writer.writerow(
                                ["4_-body_5", stock, x, x_upper, OP_td] + temp[len(temp[:])-1] + [2])

                    if avr_5_yd > avr_20_yd > avr_60_yd > avr_100_yd:
                        x_lower = OP_td
                        writer.writerow(
                            ["5_+PPP", stock, x, x_lower, OP_td] + temp[len(temp[:])-1] + [1])
                    elif avr_5_yd > avr_20_yd > avr_60_yd:
                        x_lower = OP_td
                        writer.writerow(
                            ["6_+PP", stock, x, x_lower, OP_td] + temp[len(temp[:]) - 1] + [1])
                    elif avr_100_yd > avr_60_yd > avr_20_yd > avr_5_yd:
                        x_upper = OP_td
                        writer.writerow(
                            ["7_-PPP", stock, x, x_upper, OP_td] + temp[len(temp[:]) - 1] + [2])
                    elif avr_60_yd > avr_20_yd > avr_5_yd:
                        x_upper = OP_td
                        writer.writerow(
                            ["8_-PP", stock, x, x_upper, OP_td] + temp[len(temp[:]) - 1] + [2])

                    '''
                    elif avr_60_yd > avr_20_yd and avr_20_td + x/20 > avr_60_td + x/60 and avr_5_yd > avr_20_yd:
                        x_lower = (avr_60_td - avr_20_td) * 30
                        if OP_td < x_lower < CP_yd * 1.1:  #CP_yd * 0.9 <
                            writer.writerow(
                                ["1_+bird_20_60", stock, x, x_lower, OP_td] + temp[len(temp[:])-1] + [1])
                    elif avr_60_yd <= avr_20_yd and avr_20_td + x/20 < avr_60_td + x/60 and avr_5_yd < avr_20_yd:
                        x_upper = (avr_60_td - avr_20_td) * 30
                        if OP_td < x_lower < CP_yd * 1.1:  #CP_yd * 0.9 <
                            writer.writerow(
                                ["3_-bird_20_60", stock, x, x_upper, OP_td] + temp[len(temp[:])-1] + [2])
                    if CP_yd <= float(avr_20_yd) <= x and avr_5_yd > avr_20_yd:
                        x_lower = OP_td
                        if OP_td > float(avr_20_yd):
                            x_lower = OP_td
                        else:
                            x_lower = float(avr_20_yd) + abs(float(avr_20_yd) - OP_td)
                        if x_lower < x:
                            writer.writerow(
                                ["2_+body_20", stock, x, x_lower, OP_td] + temp[len(temp[:])-1] + [1])
                    elif CP_yd <= float(avr_60_yd) <= x and avr_5_yd > avr_20_yd:
                        x_lower = 0
                        if OP_td > float(avr_60_yd):
                            x_lower = OP_td
                        else:
                            x_lower = float(avr_60_yd) + abs(float(avr_60_yd) - OP_td)
                        if x_lower < x:
                            writer.writerow(
                                ["2_+body_60", stock, x, x_lower, OP_td] + temp[len(temp[:])-1] + [1])
                    elif CP_yd >= float(avr_20_yd) <= x and avr_5_yd < avr_20_yd:
                        x_lower = OP_td
                        if OP_td > float(avr_20_yd):
                            x_lower = OP_td
                        else:
                            x_lower = float(avr_20_yd) + abs(float(avr_20_yd) - OP_td)
                        if x_lower < x:
                            writer.writerow(
                                ["2_-body_20", stock, x, x_lower, OP_td] + temp[len(temp[:]) - 1] + [1])
                    elif CP_yd >= float(avr_60_yd) <= x and avr_5_yd < avr_20_yd:
                        x_lower = 0
                        if OP_td > float(avr_60_yd):
                            x_lower = OP_td
                        else:
                            x_lower = float(avr_60_yd) + abs(float(avr_60_yd) - OP_td)
                        if x_lower < x:
                            writer.writerow(
                                ["2_-body_60", stock, x, x_lower, OP_td] + temp[len(temp[:]) - 1] + [1])
                    
                    if temp[len(temp[:])-6][0] > temp[len(temp[:])-5][0] > temp[len(temp[:])-4][0] > temp[len(temp[:])-3][0] > temp[len(temp[:])-2][0] > temp[len(temp[:])-1][0]:
                        x_lower = 0
                        writer.writerow(
                            ["7D_Rule_downward_6D", stock, x, x_lower, OP_td] + temp[len(temp[:]) - 1] + [0])
                    elif temp[len(temp[:])-6][0] < temp[len(temp[:])-5][0] < temp[len(temp[:])-4][0] < temp[len(temp[:])-3][0] < temp[len(temp[:])-2][0] < temp[len(temp[:])-1][0]:
                        x_lower = 0
                        writer.writerow(
                            ["7D_Rule_upward_6D", stock, x, x_lower, OP_td] + temp[len(temp[:]) - 1] + [0])

                    if temp[len(temp[:])-9][0] > temp[len(temp[:])-9][2] \
                            and temp[len(temp[:])-8][0] > temp[len(temp[:])-8][2] \
                            and temp[len(temp[:])-7][0] > temp[len(temp[:])-7][2] \
                            and temp[len(temp[:])-6][0] > temp[len(temp[:])-6][2] \
                            and temp[len(temp[:])-5][0] > temp[len(temp[:])-5][2] \
                            and temp[len(temp[:])-4][0] > temp[len(temp[:])-4][2] \
                            and temp[len(temp[:])-3][0] > temp[len(temp[:])-3][2] \
                            and temp[len(temp[:])-2][0] > temp[len(temp[:])-2][2] \
                            and temp[len(temp[:])-1][0] > temp[len(temp[:])-1][2]:
                        x_lower = 0
                        writer.writerow(
                            ["9D_Rule_upward_9D", stock, x, x_lower, OP_td] + temp[len(temp[:]) - 1] + [0])
                    elif temp[len(temp[:])-9][0] > temp[len(temp[:])-9][2] \
                            and temp[len(temp[:])-8][0] < temp[len(temp[:])-8][2] \
                            and temp[len(temp[:])-7][0] < temp[len(temp[:])-7][2] \
                            and temp[len(temp[:])-6][0] < temp[len(temp[:])-6][2] \
                            and temp[len(temp[:])-5][0] < temp[len(temp[:])-5][2] \
                            and temp[len(temp[:])-4][0] < temp[len(temp[:])-4][2] \
                            and temp[len(temp[:])-3][0] < temp[len(temp[:])-3][2] \
                            and temp[len(temp[:])-2][0] < temp[len(temp[:])-2][2] \
                            and temp[len(temp[:])-1][0] < temp[len(temp[:])-1][2]:
                        x_lower = 0
                        writer.writerow(
                            ["9D_Rule_downward_9D", stock, x, x_lower, OP_td] + temp[len(temp[:]) - 1] + [0])
                    elif temp[len(temp[:])-8][0] > temp[len(temp[:])-8][2] \
                            and temp[len(temp[:])-7][0] > temp[len(temp[:])-7][2] \
                            and temp[len(temp[:])-6][0] > temp[len(temp[:])-6][2] \
                            and temp[len(temp[:])-5][0] > temp[len(temp[:])-5][2] \
                            and temp[len(temp[:])-4][0] > temp[len(temp[:])-4][2] \
                            and temp[len(temp[:])-3][0] > temp[len(temp[:])-3][2] \
                            and temp[len(temp[:])-2][0] > temp[len(temp[:])-2][2] \
                            and temp[len(temp[:])-1][0] > temp[len(temp[:])-1][2]:
                        x_lower = 0
                        writer.writerow(
                            ["9D_Rule_upward_8D", stock, x, x_lower, OP_td] + temp[len(temp[:]) - 1] + [0])
                    elif temp[len(temp[:])-8][0] < temp[len(temp[:])-8][2] \
                            and temp[len(temp[:])-7][0] < temp[len(temp[:])-7][2] \
                            and temp[len(temp[:])-6][0] < temp[len(temp[:])-6][2] \
                            and temp[len(temp[:])-5][0] < temp[len(temp[:])-5][2] \
                            and temp[len(temp[:])-4][0] < temp[len(temp[:])-4][2] \
                            and temp[len(temp[:])-3][0] < temp[len(temp[:])-3][2] \
                            and temp[len(temp[:])-2][0] < temp[len(temp[:])-2][2] \
                            and temp[len(temp[:])-1][0] < temp[len(temp[:])-1][2]:
                        x_lower = 0
                        writer.writerow(
                            ["9D_Rule_downward_8D", stock, x, x_lower, OP_td] + temp[len(temp[:]) - 1] + [0])
                    '''

                    '''
                    D3 = abs(temp[len(temp[:]) - 3][8] - temp[len(temp[:]) - 3][9]) / temp[len(temp[:]) - 4][0]
                    D2 = abs(temp[len(temp[:]) - 2][8] - temp[len(temp[:]) - 2][9]) / temp[len(temp[:]) - 3][0]
                    D1 = abs(temp[len(temp[:]) - 1][8] - temp[len(temp[:]) - 1][9]) / temp[len(temp[:]) - 2][0]
                    if D3 > 0.08 and D2 > 0.08 and D1 > 0.08:
                        x_lower = 0
                        writer.writerow(
                            ["Big_wave_3D", stock, x, x_lower, OP_td] + temp[len(temp[:]) - 1] + [0])
                    '''

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
