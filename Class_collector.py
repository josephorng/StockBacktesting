from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import random
from datetime import date
from ToolBox import filter_q
from ToolBox import write2text
import time


# setup the webdriver
PATH = "C:\Program Files (x86)\chromedriver.exe"

options = webdriver.ChromeOptions()
options.add_argument("headless")
driver = webdriver.Chrome(PATH, options=options)
total = 0
for j in range(28):
    print(j)
    driver.get("https://www.cnyes.com/twstock/stock_astock.aspx#")
    time.sleep(2)
    type_ = driver.find_element_by_xpath('//*[@id="kinditem_0"]/ul/li[' + str(j+1) + ']/a')
    type_.click()
    time.sleep(2)
    num_length = len(driver.find_elements_by_xpath('//*[@id="form1"]/div[3]/div[2]/div/table/tbody/tr')) - 1
    name = driver.find_element_by_xpath('//*[@id="form1"]/div[3]/div[1]/p').text
    num = []
    print(num_length)
    for i in range(num_length):
        num_ = driver.find_element_by_xpath('//*[@id="form1"]/div[3]/div[2]/div/table/tbody/tr[' + str(i+2) + ']/td[2]/a').text
        num.append(num_)
        print(num_)
    name = name + '.txt'
    write2text(name, num)
    total = total + num_length
print(total)