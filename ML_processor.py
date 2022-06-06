import csv
from ToolBox import text2list
import os.path
import math


stock_list = text2list('ALL.txt')

for stock in stock_list:
    if os.path.isfile('./stock_data/DATA_' + stock + '.csv'):
        temp = []
        print(stock)
        with open('./stock_data/DATA_' + stock + '.csv') as csvfile:
            reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)  # change contents to floats
            # each row is a list
            for row in reader:
                temp.append(row)
        data_output = []
        with open('./stock_ML/' + stock + '_ML.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            #writer.writerow(["Class", 'stock', 'CP_upper', 'CP_lower', 'OP_td'] + input_list)
            for i in range(200, len(temp[:])-2):
                data_output = []

                data_output.append(round((temp[i][0] - temp[i][23]) / temp[i][23], 4) * 10)
                data_output.append(round((temp[i][1] - temp[i][23]) / temp[i][23], 4) * 10)
                data_output.append(round((temp[i][8] - temp[i][23]) / temp[i][23], 4) * 10)
                data_output.append(round((temp[i][9] - temp[i][23]) / temp[i][23], 4) * 10)
                data_output.append(round((temp[i][2] - temp[i][23]) / temp[i][23], 4) * 10)
                data_output.append(round((temp[i][3] - temp[i][23]) / temp[i][23], 4) * 10)
                data_output.append(round((temp[i][17] - temp[i][23]) / temp[i][23], 4) * 10)
                data_output.append(round((temp[i][18] - temp[i][23]) / temp[i][23], 4) * 10)
                data_output.append(round((temp[i][19] - temp[i][23]) / temp[i][23], 4) * 10)

                #data_output.append(temp[i][4])
                data_output.append(temp[i][5] * 10)
                data_output.append(temp[i][10] * 10)
                data_output.append(temp[i][11] * 10)
                data_output.append(temp[i][6] * 10)
                data_output.append(temp[i][7] * 10)
                data_output.append(temp[i][20] * 10)
                data_output.append(temp[i][21] * 10)
                data_output.append(temp[i][22] * 10)

                data_output.append(temp[i][14]) #Year
                data_output.append(temp[i][15]) #Month
                data_output.append(temp[i][16]) #Date

                data_output.append(temp[i - 1][0])
                data_output.append(temp[i - 1][1])
                data_output.append(temp[i - 1][2])
                data_output.append(temp[i][0])
                data_output.append(temp[i][1])
                data_output.append(temp[i][2])

                data_output.append((temp[i + 1][0]-temp[i][0]) / temp[i][0] * 10)
                data_output.append((temp[i + 2][0] - temp[i][0]) / temp[i][0] * 10)

                writer.writerow(data_output)

'''
輸入 --> 輸出
0 收盤價 ---------------- 收盤價/前一日收盤價 (1)
1 開盤價 ---------------- 開盤價/前一日收盤價 (2)
2 5日均價 --------------- 5日均價/前一日收盤價 (5)
3 20日均價 -------------- 20日均價/前一日收盤價 (6)
4 收盤價近1日趨勢  (1)
5 開盤價近1日趨勢 (1)
6 5日均價近1日趨勢 (1)
7 20日均價近1日趨勢 (1)
8 最高價 ---------------- 最高價/前一日收盤價 (3)
9 最低價 ---------------- 最低價/前一日收盤價 (4)
10 最高價近1日趨勢 (1)
11 最低價近1日趨勢 (1)
12 成交股數 ------------- 不錄用
13 成交筆數 ------------- 不錄用
14 日期 (年) ------------ 不錄用
15 日期 (月) ------------ 不錄用
16 日期 (日) ------------ 不錄用
17 60日均價 ------------- 60日均價/前一日收盤價 (1)
18 100日均價 ------------ 100日均價/前一日收盤價 (1)
19 300日均價 ------------ 300日均價/前一日收盤價 (1)
20 60日均價趨勢  (1)
21 100日均價趨勢 (1)
22 300日均價趨勢 (1)
23 前一日收盤價

1 收盤價/前一日收盤價
2 開盤價/前一日收盤價
3 最高價/前一日收盤價
4 最低價/前一日收盤價
5 5日均價/前一日收盤價
6 20日均價/前一日收盤價
7 60日均價/前一日收盤價
8 100日均價/前一日收盤價
9 300日均價/前一日收盤價

10 開盤價近1日趨勢
11 最高價近1日趨勢
12 最低價近1日趨勢
13 5日均價近1日趨勢
14 20日均價近1日趨勢
15 60日均價趨勢
16 100日均價趨勢
17 300日均價趨勢

18 日期 (年)
19 日期 (月)
20 日期 (日)
21 前一天收盤價
22 前一天開盤價
23 前一天五日價
24 當天收盤價
25 當天開盤價
26 當天五日價

27 下一天漲跌幅
28 下二天漲跌幅
'''