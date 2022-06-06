from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
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
date_yd = year + '/' + month + '/02'
print(date_yd)

stock_list = text2list('ALL.txt')
PATH = "C:\Program Files (x86)\chromedriver.exe"

options = webdriver.ChromeOptions()
options.add_argument("headless")
driver = webdriver.Chrome(PATH, options=options)

for stock_num in stock_list:
    if not os.path.isfile('./stock_data/RAW/' + stock_num + '.csv'):
        print(stock_num)

        driver.get("https://www.twse.com.tw/zh/page/trading/exchange/STOCK_DAY.html")

        search = driver.find_element_by_xpath("//*[@id='main-form']/div/div/form/input")
        search.send_keys(stock_num)

        list_o = []
        year_button = driver.find_element_by_xpath("//*[@id='d1']/select[1]")
        year_button.click()

        num_Y = len(driver.find_elements_by_xpath("//*[@id='d1']/select[1]/option"))
        for i in range(num_Y):
            year_button.click()
            Year = driver.find_element_by_xpath("//*[@id='d1']/select[1]/option[" + str(num_Y-i) + "]")
            Year.click()
            num_M = len(driver.find_elements_by_xpath("//*[@id='d1']/select[2]/option"))
            print(Year.text)
            for j in range(num_M):
                month_button = driver.find_element_by_xpath("//*[@id='d1']/select[2]")
                month_button.click()
                Month = driver.find_element_by_xpath("//*[@id='d1']/select[2]/option[" + str(j+1) + "]")
                Month.click()
                print(Month.text)
                search.send_keys(Keys.RETURN)
                time.sleep(3)
                #一定要有時間
                num_Row = len(driver.find_elements_by_xpath("//*[@id='report-table']/tbody/tr"))
                num_Col = 9
                for m in range(num_Row):
                    for n in range(num_Col):
                        object = driver.find_element_by_xpath("//*[@id='report-table']/tbody/tr[" + str(m+1) + "]/td[" + str(n+1) + "]").text
                        list_o.append(object)

        path = './stock_data/' + stock_num + '.csv'
        write2csv(path, list_o, 9)

    else:
        print(stock_num)
        with open('./stock_data/RAW/' + stock_num + '.csv') as csv_file:
            rows = csv.reader(csv_file, delimiter=',')
            data = list(rows)

        temp_date = data[len(data[:])-1][0]
        print(temp_date)

        if temp_date != date_yd:
            list_date = temp_date.split('/')
            for x in range(len(list_date)):
                list_date[x] = int(list_date[x])
            try:
                driver.get("https://www.twse.com.tw/zh/page/trading/exchange/STOCK_DAY.html")
                time.sleep(1.5)
                search = driver.find_element_by_xpath("//*[@id='main-form']/div/div/form/input")
                search.send_keys(stock_num)
                delay = 1.5
                myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located(
                    (By.XPATH, "//*[@id='d1']/select[1]")))

                year_button = driver.find_element_by_xpath("//*[@id='d1']/select[1]")
                year_button.click()
                num_Y = len(driver.find_elements_by_xpath("//*[@id='d1']/select[1]/option"))

                start_update = 0

                for i in range(list_date[0], int(year)+1):
                    year_button.click()
                    Year = driver.find_element_by_xpath(
                        "//*[@id='d1']/select[1]/option[" + str(num_Y - (i - 99)) + "]")
                    #print(num_Y - (i - 99))
                    Year.click()
                    print(Year.text)
                    month_limit = 0
                    #print(i)
                    if int(year) == list_date[0]:
                        month_limit = int(month) + 1
                        month_start = list_date[1]
                    elif int(year) != list_date[0]:
                        if int(year) == i:
                            month_limit = int(month) + 1
                            month_start = 1
                        elif i == list_date[0]:
                            month_limit = 13
                            month_start = list_date[1]
                        elif int(year) > i > list_date[0]:
                            month_limit = 13
                            month_start = 1

                    for j in range(month_start, month_limit):
                        month_button = driver.find_element_by_xpath("//*[@id='d1']/select[2]")
                        month_button.click()
                        Month = driver.find_element_by_xpath("//*[@id='d1']/select[2]/option[" + str(j) + "]")
                        Month.click()
                        print(Month.text)
                        search.send_keys(Keys.RETURN)
                        time.sleep(3)
                        num_Row = len(driver.find_elements_by_xpath("//*[@id='report-table']/tbody/tr"))
                        for m in range(num_Row):
                            object_date = driver.find_element_by_xpath(
                                "//*[@id='report-table']/tbody/tr[" + str(m + 1) + "]/td[" + str(1) + "]").text
                            temp_data = data
                            if start_update == 1:
                                temp_list = []
                                for n in range(9):
                                    object = driver.find_element_by_xpath(
                                        "//*[@id='report-table']/tbody/tr[" + str(m + 1) + "]/td[" + str(n + 1) + "]").text
                                    temp_list.append(object)
                                temp_data = [[0] * 9 for y in range(len(temp_data[:]))]
                                temp_data[0:len(data)-1] = data
                                temp_data[len(data[:])] = temp_list
                                data = temp_data
                            if object_date == temp_date:
                                start_update = 1
            except TimeoutException:
                print("Loading took too much time!")
            except NoSuchElementException:
                print("No Such Element Exception!")

            with open('./stock_data/RAW/' + stock_num + '.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                for i in range(len(data[:])):
                    writer.writerow(data[i])

toc = time.perf_counter()
print(f"Downloaded the tutorial in {(toc - tic) / 60:0.4f} mins")
