from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from datetime import datetime
from ToolBox import write2csv
from ToolBox import text2list
import os.path
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
    14 日期 (年)
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
    28 本體比例 = (收盤0 - 開盤1)/前一天收盤
    29 上影線 = 上影線長度8/前一天收盤
    30 下影線 = 下影線長度9/前一天收盤
    """

    avr_5_td_ = 0
    avr_20_td_ = 0
    avr_60_td_ = 0
    for i_ in range(4):
        avr_5_td_ = avr_5_td_ + temp_[-i_ - 1][0] / 5
    avr_5_td_ = avr_5_td_ + CP_td_ / 5
    for i_ in range(19):
        avr_20_td_ = avr_20_td_ + temp_[-i_ - 1][0] / 20
    avr_20_td_ = avr_20_td_ + CP_td_ / 20
    for i_ in range(59):
        avr_60_td_ = avr_60_td_ + temp_[-i_ - 1][0] / 60
    avr_60_td_ = avr_60_td_ + CP_td_ / 60

    avr_5_yd_ = temp_[-1][2]
    avr_20_yd_ = temp_[-1][3]
    avr_60_yd_ = temp_[-1][17]

    CP_yd_ = temp_[-1][0]

    slope_5_yd_ = temp_[-1][6]

    a = temp_[-1][27]  # last last high
    b = temp_[-1][25]  # last high
    d = temp_[-1][24]  # last low
    e = temp_[-1][26]  # last last low

    last_ = ''
    align_t_ = ''
    align_y_ = ''

    body_rate = (CP_td_ - OP_td_)/CP_yd_*100
    if 1 > body_rate >= 0:
        body_ = 1
    elif 5 > body_rate >= 1:
        body_ = 2
    elif body_rate >= 5:
        body_ = 3
    elif -1 <= body_rate < 0:
        body_ = -1
    elif -5 <= body_rate < -1:
        body_ = -2
    elif body_rate < -5:
        body_ = -3

    if avr_5_td_ >= avr_20_td_ >= avr_60_td_:
        align_t_ = '5>20>60'
    elif avr_5_td_ >= avr_60_td_ >= avr_20_td_:
        align_t_ = '5>60>20'
    elif avr_60_td_ >= avr_5_td_ >= avr_20_td_:
        align_t_ = '60>5>20'
    elif avr_60_td_ >= avr_20_td_ >= avr_5_td_:
        align_t_ = '60>20>5'
    elif avr_20_td_ >= avr_60_td_ >= avr_5_td_:
        align_t_ = '20>60>5'
    elif avr_20_td_ >= avr_5_td_ >= avr_60_td_:
        align_t_ = '20>5>60'

    if avr_5_yd_ >= avr_20_yd_ >= avr_60_yd_:
        align_y_ = '5>20>60'
    elif avr_5_yd_ >= avr_60_yd_ >= avr_20_yd_:
        align_y_ = '5>60>20'
    elif avr_60_yd_ >= avr_5_yd_ >= avr_20_yd_:
        align_y_ = '60>5>20'
    elif avr_60_yd_ >= avr_20_yd_ >= avr_5_yd_:
        align_y_ = '60>20>5'
    elif avr_20_yd_ >= avr_60_yd_ >= avr_5_yd_:
        align_y_ = '20>60>5'
    elif avr_20_yd_ >= avr_5_yd_ >= avr_60_yd_:
        align_y_ = '20>5>60'

    if a >= b >= avr_5_td_ >= d >= e:
        last_ = 'abcde'
    elif a >= b >= avr_5_td_ >= e >= d:
        last_ = 'abced'
    elif a >= b >= d >= avr_5_td_ >= e:
        last_ = 'abdce'
    elif a >= b >= d >= e >= avr_5_td_:
        last_ = 'abdec'
    elif a >= b >= e >= avr_5_td_ >= d:
        last_ = 'abecd'
    elif a >= b >= e >= d >= avr_5_td_:
        last_ = 'abedc'
    elif a >= avr_5_td_ >= b >= d >= e:
        last_ = 'acbde'
    elif a >= avr_5_td_ >= b >= e >= d:
        last_ = 'acbed'
    elif a >= avr_5_td_ >= d >= b >= e:
        last_ = 'acdbe'
    elif a >= avr_5_td_ >= d >= e >= b:
        last_ = 'acdeb'
    elif a >= avr_5_td_ >= e >= b >= d:
        last_ = 'acebd'
    elif a >= avr_5_td_ >= e >= d >= b:
        last_ = 'acedb'
    elif a >= d >= b >= avr_5_td_ >= e:
        last_ = 'adbce'
    elif a >= d >= b >= e >= avr_5_td_:
        last_ = 'adbec'
    elif a >= d >= avr_5_td_ >= b >= e:
        last_ = 'adcbe'
    elif a >= d >= avr_5_td_ >= e >= b:
        last_ = 'adceb'
    elif a >= d >= e >= b >= avr_5_td_:
        last_ = 'adebc'
    elif a >= d >= e >= avr_5_td_ >= b:
        last_ = 'adecb'
    elif a >= e >= b >= avr_5_td_ >= d:
        last_ = 'aebcd'
    elif a >= e >= b >= d >= avr_5_td_:
        last_ = 'aebdc'
    elif a >= e >= avr_5_td_ >= b >= d:
        last_ = 'aecbd'
    elif a >= e >= avr_5_td_ >= d >= b:
        last_ = 'aecdb'
    elif a >= e >= d >= b >= avr_5_td_:
        last_ = 'aedbc'
    elif a >= e >= d >= avr_5_td_ >= b:
        last_ = 'aedcb'
    elif b >= a >= avr_5_td_ >= d >= e:
        last_ = 'bacde'
    elif b >= a >= avr_5_td_ >= e >= d:
        last_ = 'baced'
    elif b >= a >= d >= avr_5_td_ >= e:
        last_ = 'badce'
    elif b >= a >= d >= e >= avr_5_td_:
        last_ = 'badec'
    elif b >= a >= e >= avr_5_td_ >= d:
        last_ = 'baecd'
    elif b >= a >= e >= d >= avr_5_td_:
        last_ = 'baedc'
    elif b >= avr_5_td_ >= a >= d >= e:
        last_ = 'bcade'
    elif b >= avr_5_td_ >= a >= e >= d:
        last_ = 'bcaed'
    elif b >= avr_5_td_ >= d >= a >= e:
        last_ = 'bcdae'
    elif b >= avr_5_td_ >= d >= e >= a:
        last_ = 'bcdea'
    elif b >= avr_5_td_ >= e >= a >= d:
        last_ = 'bcead'
    elif b >= avr_5_td_ >= e >= d >= a:
        last_ = 'bceda'
    elif b >= d >= a >= avr_5_td_ >= e:
        last_ = 'bdace'
    elif b >= d >= a >= e >= avr_5_td_:
        last_ = 'bdaec'
    elif b >= d >= avr_5_td_ >= a >= e:
        last_ = 'bdcae'
    elif b >= d >= avr_5_td_ >= e >= a:
        last_ = 'bdcea'
    elif b >= d >= e >= a >= avr_5_td_:
        last_ = 'bdeac'
    elif b >= d >= e >= avr_5_td_ >= a:
        last_ = 'bdeca'
    elif b >= e >= a >= avr_5_td_ >= d:
        last_ = 'beacd'
    elif b >= e >= a >= d >= avr_5_td_:
        last_ = 'beadc'
    elif b >= e >= avr_5_td_ >= a >= d:
        last_ = 'becad'
    elif b >= e >= avr_5_td_ >= d >= a:
        last_ = 'becda'
    elif b >= e >= d >= a >= avr_5_td_:
        last_ = 'bedac'
    elif b >= e >= d >= avr_5_td_ >= a:
        last_ = 'bedca'
    elif avr_5_td_ >= a >= b >= d >= e:
        last_ = 'cabde'
    elif avr_5_td_ >= a >= b >= e >= d:
        last_ = 'cabed'
    elif avr_5_td_ >= a >= d >= b >= e:
        last_ = 'cadbe'
    elif avr_5_td_ >= a >= d >= e >= b:
        last_ = 'cadeb'
    elif avr_5_td_ >= a >= e >= b >= d:
        last_ = 'caebd'
    elif avr_5_td_ >= a >= e >= d >= b:
        last_ = 'caedb'
    elif avr_5_td_ >= b >= a >= d >= e:
        last_ = 'cbade'
    elif avr_5_td_ >= b >= a >= e >= d:
        last_ = 'cbaed'
    elif avr_5_td_ >= b >= d >= a >= e:
        last_ = 'cbdae'
    elif avr_5_td_ >= b >= d >= e >= a:
        last_ = 'cbdea'
    elif avr_5_td_ >= b >= e >= a >= d:
        last_ = 'cbead'
    elif avr_5_td_ >= b >= e >= d >= a:
        last_ = 'cbeda'
    elif avr_5_td_ >= d >= a >= b >= e:
        last_ = 'cdabe'
    elif avr_5_td_ >= d >= a >= e >= b:
        last_ = 'cdaeb'
    elif avr_5_td_ >= d >= b >= a >= e:
        last_ = 'cdbae'
    elif avr_5_td_ >= d >= b >= e >= a:
        last_ = 'cdbea'
    elif avr_5_td_ >= d >= e >= a >= b:
        last_ = 'cdeab'
    elif avr_5_td_ >= d >= e >= b >= a:
        last_ = 'cdeba'
    elif avr_5_td_ >= e >= a >= b >= d:
        last_ = 'ceabd'
    elif avr_5_td_ >= e >= a >= d >= b:
        last_ = 'ceadb'
    elif avr_5_td_ >= e >= b >= a >= d:
        last_ = 'cebad'
    elif avr_5_td_ >= e >= b >= d >= a:
        last_ = 'cebda'
    elif avr_5_td_ >= e >= d >= a >= b:
        last_ = 'cedab'
    elif avr_5_td_ >= e >= d >= b >= a:
        last_ = 'cedba'
    elif d >= a >= b >= avr_5_td_ >= e:
        last_ = 'dabce'
    elif d >= a >= b >= e >= avr_5_td_:
        last_ = 'dabec'
    elif d >= a >= avr_5_td_ >= b >= e:
        last_ = 'dacbe'
    elif d >= a >= avr_5_td_ >= e >= b:
        last_ = 'daceb'
    elif d >= a >= e >= b >= avr_5_td_:
        last_ = 'daebc'
    elif d >= a >= e >= avr_5_td_ >= b:
        last_ = 'daecb'
    elif d >= b >= a >= avr_5_td_ >= e:
        last_ = 'dbace'
    elif d >= b >= a >= e >= avr_5_td_:
        last_ = 'dbaec'
    elif d >= b >= avr_5_td_ >= a >= e:
        last_ = 'dbcae'
    elif d >= b >= avr_5_td_ >= e >= a:
        last_ = 'dbcea'
    elif d >= b >= e >= a >= avr_5_td_:
        last_ = 'dbeac'
    elif d >= b >= e >= avr_5_td_ >= a:
        last_ = 'dbeca'
    elif d >= avr_5_td_ >= a >= b >= e:
        last_ = 'dcabe'
    elif d >= avr_5_td_ >= a >= e >= b:
        last_ = 'dcaeb'
    elif d >= avr_5_td_ >= b >= a >= e:
        last_ = 'dcbae'
    elif d >= avr_5_td_ >= b >= e >= a:
        last_ = 'dcbea'
    elif d >= avr_5_td_ >= e >= a >= b:
        last_ = 'dceab'
    elif d >= avr_5_td_ >= e >= b >= a:
        last_ = 'dceba'
    elif d >= e >= a >= b >= avr_5_td_:
        last_ = 'deabc'
    elif d >= e >= a >= avr_5_td_ >= b:
        last_ = 'deacb'
    elif d >= e >= b >= a >= avr_5_td_:
        last_ = 'debac'
    elif d >= e >= b >= avr_5_td_ >= a:
        last_ = 'debca'
    elif d >= e >= avr_5_td_ >= a >= b:
        last_ = 'decab'
    elif d >= e >= avr_5_td_ >= b >= a:
        last_ = 'decba'
    elif e >= a >= b >= avr_5_td_ >= d:
        last_ = 'eabcd'
    elif e >= a >= b >= d >= avr_5_td_:
        last_ = 'eabdc'
    elif e >= a >= avr_5_td_ >= b >= d:
        last_ = 'eacbd'
    elif e >= a >= avr_5_td_ >= d >= b:
        last_ = 'eacdb'
    elif e >= a >= d >= b >= avr_5_td_:
        last_ = 'eadbc'
    elif e >= a >= d >= avr_5_td_ >= b:
        last_ = 'eadcb'
    elif e >= b >= a >= avr_5_td_ >= d:
        last_ = 'ebacd'
    elif e >= b >= a >= d >= avr_5_td_:
        last_ = 'ebadc'
    elif e >= b >= avr_5_td_ >= a >= d:
        last_ = 'ebcad'
    elif e >= b >= avr_5_td_ >= d >= a:
        last_ = 'ebcda'
    elif e >= b >= d >= a >= avr_5_td_:
        last_ = 'ebdac'
    elif e >= b >= d >= avr_5_td_ >= a:
        last_ = 'ebdca'
    elif e >= avr_5_td_ >= a >= b >= d:
        last_ = 'ecabd'
    elif e >= avr_5_td_ >= a >= d >= b:
        last_ = 'ecadb'
    elif e >= avr_5_td_ >= b >= a >= d:
        last_ = 'ecbad'
    elif e >= avr_5_td_ >= b >= d >= a:
        last_ = 'ecbda'
    elif e >= avr_5_td_ >= d >= a >= b:
        last_ = 'ecdab'
    elif e >= avr_5_td_ >= d >= b >= a:
        last_ = 'ecdba'
    elif e >= d >= a >= b >= avr_5_td_:
        last_ = 'edabc'
    elif e >= d >= a >= avr_5_td_ >= b:
        last_ = 'edacb'
    elif e >= d >= b >= a >= avr_5_td_:
        last_ = 'edbac'
    elif e >= d >= b >= avr_5_td_ >= a:
        last_ = 'edbca'
    elif e >= d >= avr_5_td_ >= a >= b:
        last_ = 'edcab'
    elif e >= d >= avr_5_td_ >= b >= a:
        last_ = 'edcba'

    if slope_5_yd_ >= 0:
        slope_ = 'slp>0'
    else:
        slope_ = 'slp<0'

    if CP_yd_ < avr_5_yd_ and CP_yd_ < avr_20_yd_ and CP_td_ > avr_5_td_ and CP_td_ > avr_20_td_ and body_ > 0:
        name_ = 'Body2+'
    elif CP_yd_ < avr_5_yd_ and CP_td_ - avr_5_td_ > abs(OP_td_ - avr_5_td_) and body_ > 0:
        name_ = 'Body+'
    elif CP_yd_ > avr_5_yd_ and CP_yd_ > avr_20_yd_ and CP_td_ < avr_5_td_ and CP_td_ < avr_20_td_ and body_ < 0:
        name_ = 'Body2-'
    elif CP_yd_ > avr_5_yd_ and avr_5_td_ - CP_td_ > abs(OP_td_ - avr_5_td_) and body_ < 0:
        name_ = 'Body-'
    elif body_ == 3:
        name_ = 'None3+'
    elif 0 <= body_ < 3:
        name_ = 'None+'
    elif body_ == -3:
        name_ = 'None3-'
    elif 0 > body_ > -3:
        name_ = 'None-'

    for j_ in range(1, len(total_indices_[:])):
        if total_indices_[j_][0] == name_ and total_indices_[j_][2] == last_ and total_indices_[j_][3] == align_y_ \
                and total_indices_[j_][4] == align_t_ and total_indices_[j_][5] == slope_:
            # print(total_indices_[j_][0], total_indices_[j_][1])
            return total_indices_[j_][:] + [avr_5_td_]
    return ['Empty']


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

input_list = ['stock', 'CP',
              'name', 'total', 'last', 'align_y', 'align_t', 'slope',
              '5 score', '10 score', '20 score', '30 score', '60 score',
              '5 win rate', '10 win rate', '20 win rate', '30 win rate', '60 win rate',
              '5 HP', '10 HP', '20 HP', '30 HP', '60 HP',
              '5 LP', '10 LP', '20 LP', '30 LP', '60 LP', 'avr5_td']

TOE = 0
NSE = 0
file_date = year + '_' + month + '_' + day
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
                    time.sleep(1)
                    myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="_profile-TWS:' + stock + ':STOCK"]/div[2]/div[2]/div[5]/div[2]')))
                    # print("Page is ready!")
                    OP_td = float(driver.find_element_by_xpath(
                        '//*[@id="_profile-TWS:' + stock + ':STOCK"]/div[2]/div[2]/div[5]/div[2]').text.replace('--',
                                                                                                                '0').replace(
                        ',', ''))
                    myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="_profile-TWS:' + stock + ':STOCK"]/div[1]/div[3]/div[1]/div/span')))
                    CP_td = float(driver.find_element_by_xpath(
                        '//*[@id="_profile-TWS:' + stock + ':STOCK"]/div[1]/div[3]/div[1]/div/span').text.replace('--',
                                                                                                                  '0').replace(
                        ',', ''))
                    signal = signal_type(temp, total_indices, CP_td, OP_td)
                    writer.writerow([stock, CP_td] + signal)
                    print([stock, CP_td] + signal)

                except TimeoutException:
                    print("Loading took too much time!")
                    TOE = TOE + 1
                except NoSuchElementException:
                    print("No Such Element Exception!")
                    NSE = NSE + 1
                except StaleElementReferenceException:
                    print('StaleElementReferenceException')

toc = time.perf_counter()
print('TOE' + str(TOE))
print('NSE' + str(NSE))
print(f"Downloaded the tutorial in {(toc - tic) / 60:0.4f} mins")

win32api.MessageBox(0, 'Finished', 'Reminder', 0x00001000)
