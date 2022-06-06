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

driver.get("https://histock.tw/member/mystocks.aspx?id=3")

Group = '5'
Name = '5_upward.txt'

login_email = driver.find_element_by_xpath("//*[@id='email']")
login_email.send_keys('josephorng@hotmail.com')
login_email = driver.find_element_by_xpath("//*[@id='password']")
login_email.send_keys('aa123456')
login_btn = driver.find_element_by_xpath("//*[@id='bLogin']")
login_btn.click()
stock_btn1 = driver.find_element_by_xpath("//*[@id='f']/div[3]/div/div[2]/nav[1]/ul/li[3]/a")
stock_btn1.click()
stock_btn2 = driver.find_element_by_xpath("//*[@id='form1']/div[5]/div/div[1]/nav/ul/li[" + Group + "]/a")
stock_btn2.click()

stock_file = open(Name, "r")
stock_list = stock_file.read().splitlines()
print(stock_list)
stock_file.close()

i = 0

for num in stock_list:
    input_num = driver.find_element_by_xpath("//*[@id='CPHB1_tbxStock']")
    input_num.send_keys(str(num))
    input_num.send_keys(Keys.ENTER)
    input_enter = driver.find_element_by_xpath("//*[@id='CPHB1_btnGo']")
    input_enter.click()
    driver.implicitly_wait(2000)
    i = i+1
    print(i)


