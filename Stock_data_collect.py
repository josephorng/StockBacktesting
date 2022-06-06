from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import random

# setup the webdriver
PATH = "C:\Program Files (x86)\chromedriver.exe"

options = webdriver.ChromeOptions()
options.add_argument("headless")
driver = webdriver.Chrome(PATH, options=options)

driver.get("https://www.twse.com.tw/zh/page/trading/exchange/STOCK_DAY.html")

search = driver.find_element_by_xpath("//*[@id='main-form']/div/div/form/input")
search.send_keys('0050')

for Y in range(5):
    for M in range(12):
        year_button = driver.find_element_by_xpath("//*[@id='d1']/select[1]")
        year_button.click()
        year = driver.find_element_by_xpath("//*[@id='d1']/select[1]/option[" + str(Y+2) + "]")
        year.click()

        month_button = driver.find_element_by_xpath("//*[@id='d1']/select[2]")
        month_button.click()
        month = driver.find_element_by_xpath("//*[@id='d1']/select[2]/option[" + str(M+1) + "]")
        month.click()


        search.send_keys(Keys.RETURN)

        download = driver.find_element_by_xpath("//*[@id='reports']/div[1]/a[2]")

        driver.implicitly_wait(2000)

        download.click()

        driver.implicitly_wait(2000)


