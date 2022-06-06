from datetime import datetime
import os.path
import time
import csv
import win32api
from ToolBox import text2list

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


def calculator(vol_threshold, r_threshold, op_threshold, file_name):
    tic = time.perf_counter()
    stock_list = text2list('ALL_company.txt')
    folder = './Comparison/'

    write_all_list = []
    total = 0
    win = [0, 0, 0, 0]
    win_max = [0, 0, 0, 0]
    low_count = [0, 0, 0, 0]
    sum_low = 0
    sum_high = 0
    sum_cp = 0
    # Q_threshold = 0
    # R_threshold = 3
    # op_threshold = 0.01
    for stock in stock_list:
        if not os.path.isfile('./stock_data/DATA/DATA_' + stock + '.csv'):
            print('No data. \n')
            continue

        list_stock_dt = []
        with open('./stock_data/DATA/DATA_' + stock + '.csv') as csvfile:
            reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)  # change contents to floats
            # each row is a list
            for row in reader:
                list_stock_dt.append(row)
        for i_stock_dt in range(51, len(list_stock_dt[:])):
            year = list_stock_dt[i_stock_dt][14]
            month = list_stock_dt[i_stock_dt][15]
            date = list_stock_dt[i_stock_dt][16]
            CP_YD = float(list_stock_dt[i_stock_dt][23])
            CP = float(list_stock_dt[i_stock_dt][0])
            OP = float(list_stock_dt[i_stock_dt][1])
            HP = float(list_stock_dt[i_stock_dt][8])
            LP = float(list_stock_dt[i_stock_dt][9])
            Q = float(list_stock_dt[i_stock_dt][12])
            sum_q = 0
            day = 5
            for i in range(day):
                sum_q = sum_q + float(list_stock_dt[i_stock_dt - i - 1][12])
            aver = sum_q / day
            if aver != 0:
                r = Q / aver
            else:
                r = 0

            if not (r_threshold + 1 > r > r_threshold and vol_threshold[1] > Q > vol_threshold[0]):
                continue
            profit = 0
            profit_max = 0
            profit_low = 0
            b_count = False
            # if OP >= CP_YD:
            if CP_YD == 0:
                continue
            if op_threshold + 0.01 > (OP - CP_YD) / CP_YD > op_threshold:
                profit = (CP - OP) / OP * 100
                profit_max = (HP - OP) / OP * 100
                profit_low = (LP - OP) / OP * 100
                b_count = True
            # elif CP_YD >= OP:
            elif op_threshold + 0.01 > (CP_YD - OP) / CP_YD > op_threshold:
                profit = (OP - CP) / OP * 100
                profit_max = (OP - LP) / OP * 100
                profit_low = (OP - HP) / OP * 100
                b_count = True
            if b_count is False:
                continue
            write_list = [stock, year, month, date,
                          r, profit, profit_max, profit_low,
                          CP, OP, HP, LP, Q, sum_q]
            write_all_list.append(write_list)

            total = total + 1
            sum_low += profit_low
            sum_high += profit_max
            sum_cp += profit
            for i in range(4):
                if profit > i:
                    win[i] += 1
                if profit_max > i:
                    win_max[i] += 1
                if abs(profit_low) > i:
                    low_count[i] += 1
    if total == 0:
        return False
    # file_name = "Ultimatum_Summary_five_day"
    with open(folder + file_name + '.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        """writer.writerow(
            ["Q_threshold", "R_threshold","OP_threshold", "total", "avr_cp", "avr_high", "avr_low", "win1", "win2", "win3", "win4",
             "max1", "max2", "max3", "max4",
             "low1", "low2", "low3", "low4"])"""
        # writer.writerow([ total, sum_cp, sum_high, sum_low] + win + win_max + low_count)
        win_rate = [x / total for x in win]
        max_rate = [x / total for x in win_max]
        low_rate = [x / total for x in low_count]
        avr_high = sum_high / total
        avr_cp = sum_cp / total
        avr_low = sum_low / total
        writer.writerow(
            [vol_threshold[0], vol_threshold[1], r_threshold, op_threshold, total, avr_cp, avr_high,
             avr_low] + win_rate + max_rate + low_rate)

    toc = time.perf_counter()
    print(f"Downloaded the tutorial in {(toc - tic) / 60:0.4f} mins")

    """i = 0
    while os.path.isfile(folder + 'Ultimatum_R' + str(r_threshold) + "_Q" + str(vol_threshold) + "_" + str(i) + '.csv'):
        i = i + 1

    file_name = 'Ultimatum_R' + str(r_threshold) + "_Q" + str(vol_threshold) + "_OP" + str(op_threshold * 100)
    with open(folder + file_name + "_detail_" + str(i) + '.csv', 'w',
              newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(
            ["stock", "year", "month", "date",
             "Ratio", "profit", "profit_max", "profit_low",
             "CP", "OP", "HP", "LP", "Q", "sum_q"])
        writer.writerows(write_all_list)"""


folder_ = './Comparison/'
file_name_ = "Ultimatum_Summary_five_day"
with open(folder_ + file_name_ + '.csv', 'w', newline='') as csvfile:
    writer_ = csv.writer(csvfile)
    writer_.writerow(
        ["vol_threshold[0]", "vol_threshold[1]", "R_threshold", "OP_threshold", "total", "avr_cp", "avr_high",
         "avr_low", "win1", "win2", "win3", "win4",
         "max1", "max2", "max3", "max4",
         "low1", "low2", "low3", "low4"])

vol_threshold_list = [[0, 1000], [1000, 2000], [2000, 3000], [3000, 2000000]]
r_threshold_list = [1, 2, 3, 4, 5]
op_threshold_list = [0, 0.01, 0.02, 0.03, 0.04, 0.05]
for vol in vol_threshold_list:
    for r in r_threshold_list:
        for op in op_threshold_list:
            calculator(vol, r, op, file_name_)
