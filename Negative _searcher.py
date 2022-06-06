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

stock_list = text2list('ALL.txt')

bird = []
body_up = []
body_down_up = []
body_over = []
i = 0

input_list = ['CP_yd', 'OP_yd', '5D', '20D', 'CP_slope', 'OP_slope', '5D_slope', '20D_slope',
              'HP', 'LP', 'HP_slope', 'LP_slope', 'Quantity', 'Deal', 'Year', 'Month', 'Date',
              '60D', '100D', '300D', '60D_slope', '100D_slope', '300D_slope', 'CP_yd', 'condition']
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


with open('./stock_search_purchase/' + file_date + '.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Class", 'stock', 'CP_upper', 'CP_lower', 'OP_td'] + input_list)
    for stock in stock_list:
        if os.path.isfile('./stock_data/DATA_' + stock + '.csv'):
            print(stock)
            temp = []
            with open('./stock_data/DATA_' + stock + '.csv') as csvfile:
                reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)  # change contents to floats
                # each row is a list
                for row in reader:
                    temp.append(row)
            if temp[len(temp[:])-1][12] > 2000000 and 180 > temp[len(temp[:])-1][0] > 30 and len(temp[:]) > 301:
                print(temp[len(temp[:]) - 1][12])
                data = [0] * 301
                date_list = [0] * 301
                for i in range(301):
                    data[i] = temp[len(temp[:])-(301-i)][0]
                    date_list[i] = temp[len(temp[:])-(301-i)][16]

                driver.get("https://invest.cnyes.com/twstock/TWS/" + stock + "/overview")

                delay = 3  # seconds
                try:
                    myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="_profile-TWS:' + stock + ':STOCK"]/div[2]/div[2]/div[5]/div[2]')))
                    #print("Page is ready!")
                    OP_td = float(driver.find_element_by_xpath(
                        '//*[@id="_profile-TWS:' + stock + ':STOCK"]/div[2]/div[2]/div[5]/div[2]').text.replace('--',
                                                                                                                '0').replace(
                        ',', ''))

                    CP_yd = float(temp[len(temp[:]) - 1][0])
                    OP_yd = float(temp[len(temp[:]) - 1][1])

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

                    '''
                    print('昨日收盤價' + str(CP_yd))
                    print('今日開盤價' + str(OP_td))
                    print('昨日20均價' + str(avr_20_yd))
                    print('今日20均價' + str(avr_20_td))
                    print('昨日5均價' + str(avr_5_yd))
                    print('今日5均價' + str(avr_5_td))
                    print('最新日期' + str(date_list[len(data) - 1]))
                    '''

                    threshold = 1.1
                    x = CP_yd * threshold

                    a5_td = avr_5_td + CP_yd * 1.04 / 5
                    a20_td = avr_20_td + CP_yd * 1.04 / 20
                    a60_td = avr_60_td + CP_yd * 1.04 / 60

                    x_lower = CP_yd

                    if avr_20_yd >= avr_5_yd and avr_5_td + x/5 > avr_20_td + x/20:
                        x_lower = (avr_20_td - avr_5_td) / 0.15
                        if OP_td < x_lower < CP_yd * 1.1:
                            writer.writerow(
                                ["bird_5_20", stock, x, x_lower, OP_td] + temp[len(temp[:])-1] + [1])
                    elif avr_60_yd >= avr_20_yd and avr_20_td + x/20 > avr_60_td + x/60:
                        x_lower = (avr_60_td - avr_20_td) * 30
                        if OP_td < x_lower < CP_yd * 1.1:  #CP_yd * 0.9 <
                            writer.writerow(
                                ["bird_20_60", stock, x, x_lower, OP_td] + temp[len(temp[:])-1] + [1])
                    elif avr_100_yd >= avr_60_yd and avr_60_td + x/60 > avr_100_td + x/100:
                        x_lower = (avr_100_td - avr_60_td) * 150
                        if OP_td < x_lower < CP_yd * 1.1:
                            writer.writerow(
                                ["bird_60_100", stock, x, x_lower, OP_td] + temp[len(temp[:])-1] + [1])

                    if 0.5 * (CP_yd + OP_yd) <= float(avr_5_yd) <= x:
                        x_lower = OP_td
                        if OP_td > float(avr_5_yd):
                            x_lower = OP_td
                        else:
                            x_lower = float(avr_5_yd) + abs(float(avr_5_yd) - OP_td)
                        if x_lower < x:
                            writer.writerow(
                                ["1_body_5", stock, x, x_lower, OP_td] + temp[len(temp[:])-1] + [1])
                    elif 0.5 * (CP_yd + OP_yd) <= float(avr_20_yd) <= x:
                        x_lower = OP_td
                        if OP_td > float(avr_20_yd):
                            x_lower = OP_td
                        else:
                            x_lower = float(avr_20_yd) + abs(float(avr_20_yd) - OP_td)
                        if x_lower < x:
                            writer.writerow(
                                ["body_20", stock, x, x_lower, OP_td] + temp[len(temp[:])-1] + [1])
                    elif 0.5 * (CP_yd + OP_yd) <= float(avr_60_yd) <= x:
                        x_lower = 0
                        if OP_td > float(avr_60_yd):
                            x_lower = OP_td
                        else:
                            x_lower = float(avr_60_yd) + abs(float(avr_60_yd) - OP_td)
                        if x_lower < x:
                            writer.writerow(
                                ["body_60", stock, x, x_lower, OP_td] + temp[len(temp[:])-1] + [1])

                    if 0.5 * (CP_yd + OP_yd) >= float(avr_5_yd) >= CP_yd * 0.9:
                        x_upper = OP_td
                        if OP_td < float(avr_5_yd):
                            x_upper = OP_td
                        else:
                            x_upper = float(avr_5_yd) + abs(float(avr_5_yd) - OP_td)
                        if x_upper > CP_yd * 0.9:
                            writer.writerow(
                                ["1_Opposite_body_5", stock, x, x_upper, OP_td] + temp[len(temp[:])-1] + [2])

                    if not temp[len(temp[:])-7][2] > temp[len(temp[:])-7][3] > temp[len(temp[:])-7][17] > temp[len(temp[:])-7][18] > temp[len(temp[:])-7][19] and avr_5_yd > avr_20_yd > avr_60_yd > avr_100_yd > avr_300_yd:
                        writer.writerow(
                            ["Big_Bang_7", stock, x, x_lower, OP_td] + temp[len(temp[:])-1] + [0])

                    elif not temp[len(temp[:])-4][2] > temp[len(temp[:])-4][3] > temp[len(temp[:])-4][17] > temp[len(temp[:])-4][18] > temp[len(temp[:])-4][19] and avr_5_yd > avr_20_yd > avr_60_yd > avr_100_yd > avr_300_yd:
                        writer.writerow(
                            ["Big_Bang_4", stock, x, x_lower, OP_td] + temp[len(temp[:])-1] + [0])

                    elif not temp[len(temp[:]) - 2][2] > temp[len(temp[:]) - 2][3] > temp[len(temp[:]) - 2][17] > \
                           temp[len(temp[:]) - 2][18] > temp[len(temp[:]) - 2][
                               19] and avr_5_yd > avr_20_yd > avr_60_yd > avr_100_yd > avr_300_yd:
                        writer.writerow(
                            ["1_Big_Bang_2", stock, x, x_lower, OP_td] + temp[len(temp[:]) - 1] + [0])

                    elif temp[len(temp)-1][6] > 0.01 and temp[len(temp)-1][7] > 0.01 and temp[len(temp)-1][20] > 0 and temp[len(temp)-1][21] > 0 and temp[len(temp)-1][22] > 0 and avr_5_yd > avr_20_yd > avr_60_yd > avr_100_yd > avr_300_yd:
                        writer.writerow(
                            ["Big_Bang_General", stock, x, x_lower, OP_td] + temp[len(temp[:])-1] + [0])

                    if temp[len(temp[:])-6][1] > temp[len(temp[:])-5][1] > temp[len(temp[:])-4][1] > temp[len(temp[:])-3][1] > temp[len(temp[:])-2][1] > temp[len(temp[:])-1][1]:
                        x_lower = 0
                        writer.writerow(
                            ["Underdog_OP_6", stock, x, x_lower, OP_td] + temp[len(temp[:]) - 1] + [0])
                    elif temp[len(temp[:])-5][1] > temp[len(temp[:])-4][1] > temp[len(temp[:])-3][1] > temp[len(temp[:])-2][1] > temp[len(temp[:])-1][1]:
                        x_lower = 0
                        writer.writerow(
                            ["Underdog_OP_5", stock, x, x_lower, OP_td] + temp[len(temp[:]) - 1] + [0])

                    if temp[len(temp[:])-6][0] > temp[len(temp[:])-5][0] > temp[len(temp[:])-4][0] > temp[len(temp[:])-3][0] > temp[len(temp[:])-2][0] > temp[len(temp[:])-1][0]:
                        x_lower = 0
                        writer.writerow(
                            ["Underdog_CP_6", stock, x, x_lower, OP_td] + temp[len(temp[:]) - 1] + [0])

                    elif temp[len(temp[:]) - 5][0] > temp[len(temp[:]) - 4][0] > temp[len(temp[:]) - 3][0] > temp[len(temp[:]) - 2][0] > temp[len(temp[:]) - 1][0]:
                        x_lower = 0
                        writer.writerow(
                            ["Underdog_CP_5", stock, x, x_lower, OP_td] + temp[len(temp[:]) - 1] + [0])

                    if temp[len(temp[:])-4][0] > temp[len(temp[:])-3][0] > temp[len(temp[:])-2][0] > temp[len(temp[:])-1][0]:
                        x_lower = 0
                        writer.writerow(
                            ["Underdog_CP_4", stock, x, x_lower, OP_td] + temp[len(temp[:]) - 1] + [0])

                    elif temp[len(temp[:]) - 3][0] > temp[len(temp[:]) - 2][0] > temp[len(temp[:]) - 1][0] and temp[len(temp[:]) - 1][7] > 0.005:
                        x_lower = 0
                        writer.writerow(
                            ["Underdog_CP_3_Up", stock, x, x_lower, OP_td] + temp[len(temp[:]) - 1] + [0])

                    if temp[len(temp[:])-4][0] * 0.75 > temp[len(temp[:])-1][0]:
                        x_lower = 0
                        writer.writerow(
                            ["Over_fall_3D", stock, x, x_lower, OP_td] + temp[len(temp[:]) - 1] + [0])

                    D3 = abs(temp[len(temp[:]) - 3][0] - temp[len(temp[:]) - 3][1]) / temp[len(temp[:]) - 5][0]
                    D2 = abs(temp[len(temp[:]) - 2][0] - temp[len(temp[:]) - 2][1]) / temp[len(temp[:]) - 5][0]
                    D1 = abs(temp[len(temp[:]) - 1][0] - temp[len(temp[:]) - 1][1]) / temp[len(temp[:]) - 5][0]

                    if D3 > 0.03 and D3 > 0.03 and D3 > 0.03:
                        x_lower = 0
                        writer.writerow(
                            ["Big_wave_3D", stock, x, x_lower, OP_td] + temp[len(temp[:]) - 1] + [0])


                except TimeoutException:
                    print("Loading took too much time!")
                    TOE = TOE + 1
                except NoSuchElementException:
                    print("No Such Element Exception!")
                    NSE = NSE + 1

toc = time.perf_counter()
print(TOE)
print(NSE)
print(f"Downloaded the tutorial in {(toc - tic) / 60:0.4f} mins")
