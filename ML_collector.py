import csv
from ToolBox import text2list
import os.path
import math


price_upper = 20000
price_lower = 0

stock_list = text2list('ALL.txt')
wait_day = 10
SD = [0] * wait_day
avr_earn_rate = [0] * wait_day
DATA = [[0] * 30 for i in range(wait_day)]

'''
0 收盤價
1 開盤價
2 5日均價
3 20日均價
4 收盤價近1日趨勢
5 開盤價近1日趨勢
6 5日均價近1日趨勢
7 20日均價近1日趨勢
8 最高價
9 最低價
10 最高價近1日趨勢
11 最低價近1日趨勢
12 成交股數
13 成交筆數
14 日期 (年)
15 日期 (月)
16 日期 (日)
17 60日均價
18 100日均價
19 300日均價
20 60日均價趨勢
21 100日均價趨勢
22 300日均價趨勢
在i+1天買入 


0 收盤價/前一日收盤價
1 開盤價/前一日收盤價
2 最高價/前一日收盤價
3 最低價/前一日收盤價
4 5日均價/前一日收盤價
5 20日均價/前一日收盤價
6 60日均價/前一日收盤價
7 100日均價/前一日收盤價
8 300日均價/前一日收盤價

9 開盤價近1日趨勢
10 最高價近1日趨勢
11 最低價近1日趨勢
12 5日均價近1日趨勢
13 20日均價近1日趨勢
14 60日均價趨勢
15 100日均價趨勢
16 300日均價趨勢

17 日期 (年)
18 日期 (月)
19 日期 (日)
20 前一天收盤價
21 前一天開盤價
22 前一天五日價
23 當天收盤價
24 當天開盤價
25 當天五日價

26 下一天漲跌幅
27 下二天漲跌幅
'''

j = 0
test = []
train = []
for stock in stock_list:
    if os.path.isfile('./stock_ML/' + stock + '_ML.csv'):
        temp = []
        print(stock)
        with open('./stock_ML/' + stock + '_ML.csv') as csvfile:
            reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)  # change contents to floats
            # each row is a list
            for row in reader:
                temp.append(row)
        for i in range(len(temp[:])):
            j = j + 1
            if temp[i][17] > 103 and temp[i][22] > 0.5 * (temp[i][20] + temp[i][21]) and (temp[i][23] - temp[i][25]) > abs(temp[i][25] - temp[i][24]):
                if j % 10 <= 7:
                    data = []
                    data = temp[i]
                    train.append(data)
                else:
                    data = []
                    data = temp[i]
                    print(data)
                    test.append(data)

with open('./stock_ML/ML_train.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for k in range(len(train[:])):
        writer.writerow(train[k])

with open('./stock_ML/ML_test.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for k in range(len(test[:])):
        writer.writerow(test[k])

print(len(train[:]))
print(len(test[:]))
