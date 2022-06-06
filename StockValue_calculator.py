from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import random
from datetime import date
from ToolBox import write2csv
from ToolBox import text2list
import os.path
from os import path
import time
from datetime import datetime
import csv

tic = time.perf_counter()
now = datetime.now() # current date and time

year = now.strftime("%Y")
year = str(int(year)-1911)
month = now.strftime("%m")
day = now.strftime("%d")

date_ = year + '/' + month + '/' + day
date_yd = year + '/' + month + '/19'
#print(date_)
print(date_yd)

stock_list = text2list('ALL.txt')
PATH = "C:\Program Files (x86)\chromedriver.exe"

options = webdriver.ChromeOptions()
options.add_argument("headless")
driver = webdriver.Chrome(PATH, options=options)

driver.get("https://stock.wespai.com/p/21965")
length = driver.find_elements_by_xpath('//*[@id="example"]/tbody/tr')

with open('./stock_data/ALL_value.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['stock', 'CP', 'num', 'value'])
    for i in range(1, len(length)+1):
        stock = driver.find_element_by_xpath('//*[@id="example"]/tbody/tr[' + str(i) + ']/td[1]').text
        print(stock)
        for j in range(len(stock_list)):
            if stock == stock_list[j]:
                CP = driver.find_element_by_xpath('//*[@id="example"]/tbody/tr[' + str(i) + ']/td[3]').text
                num = driver.find_element_by_xpath('//*[@id="example"]/tbody/tr[' + str(i) + ']/td[4]').text
                value = float(CP) * float(num)
                writer.writerow([stock, CP, num, value])
