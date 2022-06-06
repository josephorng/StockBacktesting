from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import random
from datetime import datetime
from ToolBox import write2csv
from ToolBox import text2list
import os.path
from os import path
import time
import re
from ToolBox import write2text

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

for stock_num in stock_list:
    print(stock_num)
    driver.get("https://www.twse.com.tw/zh/page/trading/exchange/STOCK_DAY.html")

    search = driver.find_element_by_xpath("//*[@id='main-form']/div/div/form/input")
    search.send_keys(stock_num)

    OP = []
    CP = []

    year_button = driver.find_element_by_xpath("//*[@id='d1']/select[1]")
    year_button.click()
    Year = driver.find_element_by_xpath("//*[@id='d1']/select[1]/option[1]")
    Year.click()
    month_button = driver.find_element_by_xpath("//*[@id='d1']/select[2]")
    month_button.click()
    Month = driver.find_element_by_xpath("//*[@id='d1']/select[2]/option[" + str(int(month)-1) + "]")
    Month.click()
    print(Year.text + '-' + Month.text)
    search.send_keys(Keys.RETURN)
    time.sleep(3)
    #一定要有時間
    num_Row = len(driver.find_elements_by_xpath("//*[@id='report-table']/tbody/tr"))
    num_Col = 9

    for m in range(num_Row):
        CP.append(float(driver.find_element_by_xpath("//*[@id='report-table']/tbody/tr[" + str(m+1) + "]/td[7]").text.replace(',', '')))
        OP.append(float(driver.find_element_by_xpath("//*[@id='report-table']/tbody/tr[" + str(m+1) + "]/td[4]").text.replace(',', '')))

    Month = driver.find_element_by_xpath("//*[@id='d1']/select[2]/option[" + month + "]")
    Month.click()
    search.send_keys(Keys.RETURN)
    time.sleep(3)
    num_Row = len(driver.find_elements_by_xpath("//*[@id='report-table']/tbody/tr"))
    for m in range(num_Row):
        CP.append(float(driver.find_element_by_xpath("//*[@id='report-table']/tbody/tr[" + str(m+1) + "]/td[7]").text.replace(',', '')))
        OP.append(float(driver.find_element_by_xpath("//*[@id='report-table']/tbody/tr[" + str(m + 1) + "]/td[4]").text.replace(',','')))

    print(stock_num)

    driver.get("https://invest.cnyes.com/twstock/tws/" + stock_num)
    time.sleep(0.5)
    OP.append(float(driver.find_element_by_xpath('//*[@id="_profile-TWS:' + stock_num + ':STOCK"]/div[2]/div[2]/div[5]/div[2]').text.replace(',', '')))
    CP.append(float(driver.find_element_by_xpath('//*[@id="_profile-TWS:' + stock_num + ':STOCK"]/div[2]/div[2]/div[6]/div[2]').text.replace(',', '')))

    '''
    driver.get("https://www.cnyes.com/twstock/Technical.aspx?code=" + stock_num)
    Five = float(driver.find_element_by_xpath('//*[@id="main3"]/div[5]/div[3]/table[1]/tbody/tr[2]/td[4]').text.replace(',', ''))
    Twenty = float(driver.find_element_by_xpath('//*[@id="main3"]/div[5]/div[3]/table[1]/tbody/tr[2]/td[6]').text.replace(',', ''))
    '''

    avg_20_td = sum(CP[len(CP)-20:len(CP)]) / 20
    avg_5_td = sum(CP[len(CP)-5:len(CP)]) / 5
    avg_20_yd = sum(CP[len(CP) - 21:len(CP)-1]) / 20
    avg_5_yd = sum(CP[len(CP) - 6:len(CP)-1]) / 5
    slope_20 = (avg_20_td - avg_20_yd) / avg_20_yd
    slope_5 = (avg_5_td - avg_5_yd) / avg_5_yd

    # 鳥嘴
    # 前一天 20日價 > 5日價
    # 買當天 5日價 > 20日價

    # 半身_以上
    # 前一天 五日價 > 收盤價
    # 買當天 收盤價 > 開盤價 > 五日價

    # 半身_以下犯上
    # 前一天 五日價 > 收盤價 & 開盤價
    # 買當天 收盤價 > 開盤價 > 五日價

    if avg_5_yd > CP[len(CP)-2] and avg_5_yd > OP[len(OP)-2] and CP[len(CP)-1] > OP[len(OP)-1] > avg_5_td:
        body_down_up.append(stock_num)

    # 半身_超半
    # 前一天 五日價 > 收盤價 & 開盤價
    # 買當天 abs(收盤價 - 五日價) >= abs(開盤價 - 五日價)


    print(OP)
    print(CP)
    print(avg_20_td)
    print(avg_5_td)


write2text(year + month + day, body_down_up)

