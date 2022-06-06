import csv
from ToolBox import text2list
import numpy
import os.path
import time
import win32api

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
23 前一日收盤價
24 上一個五日線低點
25 上一個五日線高點
26 上上一個五日線低點
27 上上一個五日線高點
28 本體比例 = (收盤0 - 開盤1)/前一天收盤
29 上影線 = 上影線長度8/前一天收盤
30 下影線 = 下影線長度9/前一天收盤
'''

tic = time.perf_counter()

stock_list = text2list('ALL.txt')

for stock in stock_list:
    #if not os.path.isfile('./stock_data/DATA_' + stock + '.csv'):
    if os.path.isfile('./stock_data/RAW/' + stock + '.csv'):
        print(stock)
        data = []

        with open('./stock_data/RAW/' + stock + '.csv') as csv_file:
            rows = csv.reader(csv_file, delimiter=',')
            data = list(rows)

        def clear_dash(i, temp_, data_, col_input, col_output):
            temp_j = i
            while data_[temp_j][col_input] == '--':
                #print(i)
                if data_[temp_j - 1][col_input] != '--':
                    temp_[i][col_output] = float(data_[temp_j - 1][col_input].replace(',', ''))
                temp_j = temp_j - 1
            if data[i][col_input] != '--':
                temp_[i][col_output] = float(data_[i][col_input].replace(',', ''))
            return temp_

        temp = [[0]*31 for i in range(len(data))]
        for i in range(len(data)):
            temp = clear_dash(i, temp, data, 6, 0)
            temp = clear_dash(i, temp, data, 3, 1)
            temp = clear_dash(i, temp, data, 4, 8)
            temp = clear_dash(i, temp, data, 5, 9)

            temp[i][2] = 0
            temp[i][3] = 0
            temp[i][4] = 0
            temp[i][5] = 0
            temp[i][6] = 0
            temp[i][7] = 0
            temp[i][10] = 0
            temp[i][11] = 0
            temp[i][12] = float(data[i][1].replace(',', ''))/1000
            temp[i][13] = float(data[i][8].replace(',', ''))


            # temp_date = data[len(data[:]) - 1][0]
            list_date = data[i][0].split('/')

            temp[i][14] = list_date[0]
            temp[i][15] = list_date[1]
            temp[i][16] = list_date[2]

            temp[i][23] = 0
            temp[i][28] = 0
            temp[i][29] = 0
            temp[i][30] = 0

            body_rate = 0
            up_line_rate = 0
            down_line_rate = 0
            # print(temp[i][0])
            # print(temp[i][1])
            # print(temp[i][8])
            # print(temp[i][9])
            if i != 0 and temp[i - 1][0] != 0:
                body_rate = (temp[i][0] - temp[i][1]) / temp[i - 1][0] * 100
                if body_rate < 0:
                    up_line_rate = (temp[i][8] - temp[i][1]) / temp[i - 1][0] * 100
                    down_line_rate = (temp[i][9] - temp[i][0]) / temp[i - 1][0] * 100
                else:
                    up_line_rate = (temp[i][8] - temp[i][0]) / temp[i - 1][0] * 100
                    down_line_rate = (temp[i][9] - temp[i][1]) / temp[i - 1][0] * 100
            # print(body_rate)

            temp[i][28] = 0
            temp[i][29] = 0
            temp[i][30] = 0

            # body line
            if 1 > body_rate >= 0:
                temp[i][28] = 1
            elif 5 > body_rate >= 1:
                temp[i][28] = 2
            elif body_rate >= 5:
                temp[i][28] = 3
            elif -1 <= body_rate < 0:
                temp[i][28] = -1
            elif -5 <= body_rate < -1:
                temp[i][28] = -2
            elif body_rate < -5:
                temp[i][28] = -3
            # upper line
            if 1 > up_line_rate >= 0:
                temp[i][29] = 1
            elif 3 > up_line_rate >= 1:
                temp[i][29] = 2
            elif up_line_rate >= 3:
                temp[i][29] = 3
            # lower line
            if -1 < down_line_rate <= 0:
                temp[i][30] = -1
            elif -3 < down_line_rate <= -1:
                temp[i][30] = -2
            elif down_line_rate <= -3:
                temp[i][30] = -3
            # print('lower = ' + str(temp[i][30]))
            # print('upper = ' + str(temp[i][29]))
            # print('body = ' + str(temp[i][28]))

            if i != 0:
                temp[i][23] = temp[i-1][0]

            temp[i][24] = 0
            temp[i][25] = 0

        def average(day_num, data_, temp_, output_column):
            for i_ in range(len(data_[:])):
                if i_ < day_num:
                    sum_temp = 0
                    for j_ in range(0, i_ + 1):
                        sum_temp = sum_temp + temp_[j_][0]
                    average_ = sum_temp / (i_ + 1)
                    temp_[i_][output_column] = round(average_, 4)
                else:
                    sum_temp = 0
                    for j_ in range(i_ - day_num + 1, i_ + 1):
                        sum_temp = sum_temp + temp_[j_][0]
                    average_ = sum_temp / day_num
                    temp_[i_][output_column] = round(average_, 4)
            return temp_


        temp = average(5, data, temp, 2)
        temp = average(20, data, temp, 3)
        temp = average(60, data, temp, 17)
        temp = average(100, data, temp, 18)
        temp = average(300, data, temp, 19)

        # 趨勢
        def slope(arr, col_input, col_compare, col_output, day):
            for i in range(len(arr[:])):
                if i > day:
                    if arr[i - day][col_compare] != 0:
                        slope_ = (arr[i][col_input] - arr[i - day][col_compare]) / arr[i - day][col_compare]
                        slope_ = round(slope_, 6)
                    else:
                        slope_ = 0
                    arr[i][col_output] = slope_
            return arr

        #print(temp)
        temp = slope(temp, 0, 0, 4, 1)
        temp = slope(temp, 1, 1, 5, 1)
        temp = slope(temp, 2, 2, 6, 1)
        temp = slope(temp, 3, 3, 7, 1)
        temp = slope(temp, 8, 0, 10, 1)
        temp = slope(temp, 9, 0, 11, 1)
        temp = slope(temp, 17, 17, 20, 1)
        temp = slope(temp, 18, 18, 21, 1)
        temp = slope(temp, 19, 19, 22, 1)
        #print(temp)

        def slope_zero(arr, col_input, col_high, col_low, col_prev_high, col_prev_low):
            high = arr[0][col_input]
            low = arr[0][col_input]
            high_prev = arr[0][col_input]
            low_prev = arr[0][col_input]
            gap = 3

            for i in range(gap, len(arr[:])-gap):
                flag = (arr[i][col_input] - arr[i-gap][col_input]) * (arr[i + gap][col_input] - arr[i][col_input]) * 100
                if flag < 0:
                    if (arr[i][col_input] - arr[i-gap][col_input]) > 0:
                        high_prev = high
                        high = arr[i][col_input]
                    elif (arr[i][col_input] - arr[i-gap][col_input]) < 0:
                        low_prev = low
                        low = arr[i][col_input]
                arr[i][col_high] = high
                arr[i][col_low] = low
                arr[i][col_prev_high] = high_prev
                arr[i][col_prev_low] = low_prev

            for i in range(gap):
                arr[i][col_high] = arr[0][col_input]
                arr[i][col_low] = arr[0][col_input]
                arr[i][col_prev_high] = arr[0][col_input]
                arr[i][col_prev_low] = arr[0][col_input]
                arr[len(arr[:]) - i - 1][col_high] = high
                arr[len(arr[:]) - i - 1][col_low] = low
                arr[len(arr[:]) - i - 1][col_prev_high] = high_prev
                arr[len(arr[:]) - i - 1][col_prev_low] = low_prev
            return arr

        temp = slope_zero(temp, 2, 25, 24, 27, 26)

        with open('./stock_data/DATA/DATA_' + stock + '.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for i in range(len(temp[:])):
                writer.writerow(temp[i])

toc = time.perf_counter()
print(f"Downloaded the tutorial in {(toc - tic) / 60:0.4f} mins")

win32api.MessageBox(0, 'Finished', 'Reminder', 0x00001000)
