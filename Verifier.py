from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
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

Class = []
with open('./stock_data/stock_class.csv') as csvfile:
    reader = csv.reader(csvfile)
    # each row is a list
    for row in reader:
        Class.append(row)


def search_class(num, c):
    for i_ in range(31):
        for j_ in range(len(c[i_][:])):
            if num == c[i_][j_]:
                return c[i_][1]

tic = time.perf_counter()
now = datetime.now() # current date and time

year = now.strftime("%Y")
year = str(int(year)-1911)
month = now.strftime("%m")
day = now.strftime("%d")
file_date = year + '_' + month + '_' + day
stock_list = []
stock_CP = []

TOE = 0
NSE = 0
print(file_date)
with open('./Practice/Question.csv') as csvfile:
    reader = csv.reader(csvfile)  # change contents to floats
    # each row is a list
    for row in reader:
        stock_list.append(row)

print(stock_list)
# setup the webdriver
PATH = "C:\Program Files (x86)\chromedriver.exe"

options = webdriver.ChromeOptions()
options.add_argument("headless")
driver = webdriver.Chrome(PATH, options=options)

i = 0
while os.path.isfile('./Practice/Ans_' + file_date + '_' + str(i) + '.csv'):
    i = i+1
with open('./Practice/Ans_' + file_date + '_' + str(i) + '.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for i in range(len(stock_list)):
        stock = str(stock_list[i]).replace('[', '')
        stock = stock.replace(']', '')
        stock = stock.replace("'", '')
        
        print(stock)
        driver.get("https://invest.cnyes.com/twstock/TWS/" + stock + "/overview")
        delay = 3  # seconds
        try:
            myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="_profile-TWS:' + stock + ':STOCK"]/div[1]/div[3]/div[1]/div/span')))
            print("Page is ready!")
            CP_td = float(driver.find_element_by_xpath(
                '//*[@id="_profile-TWS:' + stock + ':STOCK"]/div[1]/div[3]/div[1]/div/span').text.replace('--',
                                                                                                        '0').replace(
                ',', ''))
            print(stock)
            print('今日收盤價' + str(CP_td))
            #class_name = search_class(stock, Class)
            
            rate = driver.find_element_by_xpath('//*[@id="_profile-TWS:' + stock + ':STOCK"]/div[1]/div[3]/div[2]/div[2]/span').text
            range = driver.find_element_by_xpath('//*[@id="_profile-TWS:' + stock + ':STOCK"]/div[2]/div[2]/div[2]/div[2]').text
            Q = driver.find_element_by_xpath('//*[@id="_profile-TWS:' + stock + ':STOCK"]/div[2]/div[2]/div[1]/div[2]').text
            writer.writerow([stock] + [rate] + [range] + [CP_td] + [Q])
        except TimeoutException:
            print("Loading took too much time!")
            TOE = TOE + 1
        except NoSuchElementException:
            print("No Such Element Exception!")
            NSE = NSE + 1
        except StaleElementReferenceException:
            print("Stale Element Reference Exception!")




toc = time.perf_counter()
print('TOE' + str(TOE))
print('NSE' + str(NSE))
print(f"Downloaded the tutorial in {(toc - tic) / 60:0.4f} mins")

win32api.MessageBox(0, 'Finished', 'Reminder', 0x00001000)
