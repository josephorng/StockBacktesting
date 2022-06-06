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

# setup the webdriver
PATH = "C:\Program Files (x86)\chromedriver.exe"

options = webdriver.ChromeOptions()
options.add_argument("headless")
driver = webdriver.Chrome(PATH, options=options)

stock_list = text2list('ALL.txt')
input_list = ['Stock', 'Date', '1000 People', '1000 %', '800 People', '800 %', '600 People', '600 %', '400 People',
              '400 %', 'Total People', 'Total %']
TOE = 0
NSE = 0
file_date = year + '_' + month + '_' + day
Negative_list = []
for stock in stock_list:
    if not os.path.isfile('./stock_data/MAIN/MAIN_' + stock + '.csv'):
        with open('./stock_data/MAIN/MAIN_' + stock + '.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(input_list)
            delay = 1  # seconds
            try:
                driver.get("https://www.tdcc.com.tw/portal/zh/smWeb/qryStock")
                time.sleep(1)
                myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="StockNo"]')))
                myElem.send_keys(stock)
                length = len(driver.find_elements_by_xpath('//*[@id="form1"]/table/tbody/tr[1]/td[2]/select/option'))
                print(length)
                for i in range(1, length+1):
                    print(i)
                    i = length - i + 1
                    date_option = WebDriverWait(driver, delay).until(EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="form1"]/table/tbody/tr[1]/td[2]/select')))
                    date_option = driver.find_element_by_xpath('//*[@id="form1"]/table/tbody/tr[1]/td[2]/select')
                    date_option.click()
                    date = driver.find_element_by_xpath('//*[@id="form1"]/table/tbody/tr[1]/td[2]/select/option[' + str(i) + ']')
                    date.click()
                    dt = date.text
                    myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="StockNo"]')))
                    myElem.send_keys(Keys.RETURN)
                    time.sleep(1)
                    peo_1000 = float(driver.find_element_by_xpath('//*[@id="body"]/div/main/div[6]/div/table/tbody/tr[15]/td[3]').text.replace(',', ''))
                    per_1000 = float(driver.find_element_by_xpath('//*[@id="body"]/div/main/div[6]/div/table/tbody/tr[15]/td[5]').text.replace(',', ''))
                    peo_800 = float(driver.find_element_by_xpath('//*[@id="body"]/div/main/div[6]/div/table/tbody/tr[14]/td[3]').text.replace(',', ''))
                    per_800 = float(driver.find_element_by_xpath('//*[@id="body"]/div/main/div[6]/div/table/tbody/tr[14]/td[5]').text.replace(',', ''))
                    peo_600 = float(driver.find_element_by_xpath('//*[@id="body"]/div/main/div[6]/div/table/tbody/tr[13]/td[3]').text.replace(',', ''))
                    per_600 = float(driver.find_element_by_xpath('//*[@id="body"]/div/main/div[6]/div/table/tbody/tr[13]/td[5]').text.replace(',', ''))
                    peo_400 = float(driver.find_element_by_xpath('//*[@id="body"]/div/main/div[6]/div/table/tbody/tr[12]/td[3]').text.replace(',', ''))
                    per_400 = float(driver.find_element_by_xpath('//*[@id="body"]/div/main/div[6]/div/table/tbody/tr[12]/td[5]').text.replace(',', ''))
                    total_peo = peo_400 + peo_600 + peo_800 + peo_1000
                    total_per = round(per_400 + per_600 + per_800 + per_1000, 2)
                    writer.writerow([stock, dt, peo_1000, per_1000, peo_800, per_800, peo_600, per_600, peo_400, per_400, total_peo, total_per])
                    print([stock, dt, peo_1000, per_1000, peo_800, per_800, peo_600, per_600, peo_400, per_400, total_peo, total_per])

            except TimeoutException:
                print("Loading took too much time!")
                TOE = TOE + 1
            except NoSuchElementException:
                print("No Such Element Exception!")
                NSE = NSE + 1
    elif os.path.isfile('./stock_data/MAIN/MAIN_' + stock + '.csv'):
        temp = []
        with open('./stock_data/MAIN/MAIN_' + stock + '.csv') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                temp.append(row)
        with open('./stock_data/MAIN/MAIN_' + stock + '.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            delay = 1  # seconds
            try:
                driver.get("https://www.tdcc.com.tw/portal/zh/smWeb/qryStock")
                time.sleep(1)
                myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="StockNo"]')))
                myElem.send_keys(stock)
                length = len(driver.find_elements_by_xpath('//*[@id="form1"]/table/tbody/tr[1]/td[2]/select/option'))
                print(length)
                for i in range(1, length+1):
                    print(i)
                    i = length - i + 1
                    date_option = WebDriverWait(driver, delay).until(EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="form1"]/table/tbody/tr[1]/td[2]/select')))
                    date_option = driver.find_element_by_xpath('//*[@id="form1"]/table/tbody/tr[1]/td[2]/select')
                    date_option.click()
                    date = driver.find_element_by_xpath(
                        '//*[@id="form1"]/table/tbody/tr[1]/td[2]/select/option[' + str(i) + ']')

                    dt = date.text
                    flag = True
                    for j in range(1, len(temp[:])):
                        if date.text == str(temp[j][1]):
                            flag = False
                    if flag is True:
                        date.click()
                        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located(
                            (By.XPATH, '//*[@id="StockNo"]')))
                        myElem.send_keys(Keys.RETURN)
                        time.sleep(1)
                        peo_1000 = float(driver.find_element_by_xpath('//*[@id="body"]/div/main/div[6]/div/table/tbody/tr[15]/td[3]').text.replace(',', ''))
                        per_1000 = float(driver.find_element_by_xpath('//*[@id="body"]/div/main/div[6]/div/table/tbody/tr[15]/td[5]').text.replace(',', ''))
                        peo_800 = float(driver.find_element_by_xpath('//*[@id="body"]/div/main/div[6]/div/table/tbody/tr[14]/td[3]').text.replace(',', ''))
                        per_800 = float(driver.find_element_by_xpath('//*[@id="body"]/div/main/div[6]/div/table/tbody/tr[14]/td[5]').text.replace(',', ''))
                        peo_600 = float(driver.find_element_by_xpath('//*[@id="body"]/div/main/div[6]/div/table/tbody/tr[13]/td[3]').text.replace(',', ''))
                        per_600 = float(driver.find_element_by_xpath('//*[@id="body"]/div/main/div[6]/div/table/tbody/tr[13]/td[5]').text.replace(',', ''))
                        peo_400 = float(driver.find_element_by_xpath('//*[@id="body"]/div/main/div[6]/div/table/tbody/tr[12]/td[3]').text.replace(',', ''))
                        per_400 = float(driver.find_element_by_xpath('//*[@id="body"]/div/main/div[6]/div/table/tbody/tr[12]/td[5]').text.replace(',', ''))
                        total_peo = peo_400 + peo_600 + peo_800 + peo_1000
                        total_per = round(per_400 + per_600 + per_800 + per_1000, 2)
                        writer.writerow([stock, dt, peo_1000, per_1000, peo_800, per_800, peo_600, per_600, peo_400, per_400, total_peo, total_per])
                        print([stock, dt, peo_1000, per_1000, peo_800, per_800, peo_600, per_600, peo_400, per_400, total_peo, total_per])

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
