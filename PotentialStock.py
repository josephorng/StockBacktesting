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



# setup the webdriver
PATH = "C:\Program Files (x86)\chromedriver.exe"

options = webdriver.ChromeOptions()
options.add_argument("headless")
driver = webdriver.Chrome(PATH, options=options)

driver.get("https://www.cnyes.com/twstock/a_technical6.aspx")

num_5 = len(driver.find_elements_by_xpath("//*[@id='ctl00_ContentPlaceHolder1_UpdatePanel1']/div[1]/div/table[1]/tbody/tr")) - 2
list_5 = []
for i in range(num_5):
    cost = driver.find_element_by_xpath("//*[@id='ctl00_ContentPlaceHolder1_UpdatePanel1']/div[1]/div/table[1]/tbody/tr[" + str(i+3) + "]/td[3]").text
    cost = float(cost)
    if cost > 20 and cost < 200:
        temp = driver.find_element_by_xpath("//*[@id='ctl00_ContentPlaceHolder1_UpdatePanel1']/div[1]/div/table[1]/tbody/tr[" + str(i+3) + "]/td[1]").text
        list_5.append(temp)
print(list_5)

num_20 = len(driver.find_elements_by_xpath("//*[@id='ctl00_ContentPlaceHolder1_UpdatePanel1']/div[1]/div/table[3]/tbody/tr")) - 2
list_20 = []
for i in range(num_20):
    cost = driver.find_element_by_xpath("//*[@id='ctl00_ContentPlaceHolder1_UpdatePanel1']/div[1]/div/table[3]/tbody/tr[" + str(i+3) + "]/td[3]").text
    cost = float(cost)
    if cost > 20 and cost < 200:
        temp = driver.find_element_by_xpath("//*[@id='ctl00_ContentPlaceHolder1_UpdatePanel1']/div[1]/div/table[3]/tbody/tr[" + str(i+3) + "]/td[1]").text
        list_20.append(temp)
print(list_20)

num_60 = len(driver.find_elements_by_xpath("//*[@id='ctl00_ContentPlaceHolder1_UpdatePanel1']/div[1]/div/table[5]/tbody/tr")) - 2
list_60 = []
for i in range(num_60):
    cost = driver.find_element_by_xpath("//*[@id='ctl00_ContentPlaceHolder1_UpdatePanel1']/div[1]/div/table[5]/tbody/tr[" + str(i+3) + "]/td[3]").text
    cost = float(cost)
    if cost > 20 and cost < 200:
        temp = driver.find_element_by_xpath("//*[@id='ctl00_ContentPlaceHolder1_UpdatePanel1']/div[1]/div/table[5]/tbody/tr[" + str(i+3) + "]/td[1]").text
        list_60.append(temp)
print(list_60)


list_5 = filter_q(list_5, driver)
print(list_5)
list_20 = filter_q(list_20, driver)
print(list_20)
list_60 = filter_q(list_60, driver)
print(list_60)

write2text("5_upward.txt", list_5)
write2text("20_upward.txt", list_20)
write2text("60_upward.txt", list_60)
