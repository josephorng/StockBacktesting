import csv
from ToolBox import text2list
import os.path
import math

seven_list = []
nine_list = []
seven_p = 0
seven_n = 0
nine_p = 0
nine_n = 0
stock_list = text2list('110.txt')
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
'''
total_number = 0
for stock in stock_list:
    if os.path.isfile('./stock_data/DATA_' + stock + '.csv'):
        temp = []
        # print(stock)
        with open('./stock_data/DATA_' + stock + '.csv') as csvfile:
            reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)  # change contents to floats
            # each row is a list
            for row in reader:
                temp.append(row)

        total_number = total_number + len(temp[:])

        i = 1
        count = 0
        while i != (len(temp[:])-2):
            i = i + 1
            write_flag = False
            order = 'up'
            if temp[i][0] >= temp[i-1][0]:
                count += 1
                if temp[i + 1][0] < temp[i][0]:
                    write_flag = True
                    print(count)
                    seven_p += 1
            elif temp[i][0] < temp[i-1][0]:
                count -= 1
                if temp[i + 1][0] >= temp[i][0]:
                    write_flag = True
                    print(count)
                    seven_n += 1
            if write_flag:
                if temp[i][2] >= temp[i][3]:
                    order = 'up'
                else:
                    order = 'down'
                seven_list.append(
                    [count, int(stock), temp[i][14], temp[i][15], temp[i][16], temp[i][0], order, temp[i][12]])
                write_flag = False
                count = 0
        i = 1
        count = 0
        while i != (len(temp[:])-2):
            i = i + 1
            write_flag = False
            order = 'up'
            if temp[i][0] >= temp[i][2]:
                count += 1
                if temp[i + 1][0] < temp[i + 1][2]:
                    write_flag = True
                    print(count)
                    nine_p += 1
            elif temp[i][0] < temp[i][2]:
                count -= 1
                if temp[i + 1][0] >= temp[i + 1][2]:
                    write_flag = True
                    print(count)
                    nine_n += 1
            if write_flag:
                if temp[i][2] > temp[i][3]:
                    order = 'up'
                else:
                    order = 'down'
                nine_list.append(
                    [count, int(stock), temp[i][14], temp[i][15], temp[i][16], temp[i][0], order, temp[i][12]])
                write_flag = False
                count = 0

top = ['Day', 'Stock', 'year', 'month', 'date', 'CP', 'Slope', 'Q', 'Next', 'Next_2', 'Sequence', total_number]
with open('nine_list.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    total = len(nine_list[:])-2
    writer.writerow(top + ['Positive'] + [seven_p] + ['Negative'] + [seven_n] + [total])
    for i in range(len(nine_list) - 2):
        writer.writerow(nine_list[i][:] + [nine_list[i+1][0]] + [nine_list[i+2][0]] + [i])

with open('seven_list.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    total = len(seven_list[:])-2
    writer.writerow(top + ['Positive'] + [nine_p] + ['Negative'] + [nine_n] + [total])
    for i in range(len(seven_list) - 2):
        writer.writerow(seven_list[i][:] + [seven_list[i+1][0]] + [seven_list[i+2][0]] + [i])

