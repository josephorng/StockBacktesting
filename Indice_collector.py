from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os.path
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
date_yd = year + '/' + month + '/27'
print(date_yd)

PATH = "C:\Program Files (x86)\chromedriver.exe"

options = webdriver.ChromeOptions()
options.add_argument("headless")
driver = webdriver.Chrome(PATH, options=options)

if not os.path.isfile('./stock_data/RAW/Indices.csv'):
    driver.get("https://www.twse.com.tw/zh/page/trading/indices/MI_5MINS_HIST.html")
    list_o = []
    year_button = driver.find_element_by_xpath("//*[@id='d1']/select[1]")
    year_button.click()
    search = driver.find_element_by_xpath('//*[@id="main-form"]/div/div/form/a')

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
            search.click()
            time.sleep(3)
            # 一定要有時間
            num_Row = len(driver.find_elements_by_xpath("//*[@id='report-table']/tbody/tr"))
            num_Col = 5
            for m in range(num_Row):
                object_ = []
                for n in range(num_Col):
                    object_.append(driver.find_element_by_xpath("//*[@id='report-table']/tbody/tr[" + str(m+1) + "]/td[" + str(n+1) + "]").text)
                list_o.append(object_)
    with open('./stock_data/Indices.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # 日期	開盤指數	最高指數	最低指數	收盤指數
        writer.writerows(list_o)

else:
    with open('./stock_data/RAW/Indices.csv') as csv_file:
        rows = csv.reader(csv_file, delimiter=',')
        data = list(rows)

    temp_date = data[len(data[:])-1][0]
    print(temp_date)

    if temp_date != date_yd:
        list_date = temp_date.split('/')
        for x in range(len(list_date)):
            list_date[x] = int(list_date[x])
        try:
            driver.get("https://www.twse.com.tw/zh/page/trading/indices/MI_5MINS_HIST.html")
            time.sleep(1.5)
            search = driver.find_element_by_xpath('//*[@id="main-form"]/div/div/form/a')

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
                    "//*[@id='d1']/select[1]/option[" + str(num_Y - (i - 88)) + "]")
                Year.click()
                print(Year.text)
                month_limit = 0
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
                            for n in range(5):
                                object_ = driver.find_element_by_xpath(
                                    "//*[@id='report-table']/tbody/tr[" + str(m + 1) + "]/td[" + str(n + 1) + "]").text
                                temp_list.append(object_)
                            temp_data = [[0] * 5 for y in range(len(temp_data[:]))]
                            temp_data[0:len(data)-1] = data
                            temp_data[len(data[:])] = temp_list
                            data = temp_data
                            #print(temp_data[len(temp_data)-5:len(temp_data)])
                        if object_date == temp_date:
                            start_update = 1
        except TimeoutException:
            print("Loading took too much time!")
        except NoSuchElementException:
            print("No Such Element Exception!")

        with open('./stock_data/RAW/Indices.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(data)

toc = time.perf_counter()
print(f"Downloaded the tutorial in {(toc - tic) / 60:0.4f} mins")
