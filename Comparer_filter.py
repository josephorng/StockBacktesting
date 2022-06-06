import csv
from ToolBox import text2list
import numpy
import os.path
import time


#stock = '2330'

stock_list = text2list('ALL.txt')

total_num = 0
happen = 0
earn = 0
lose = 0
wait_day = 3
sum_rate = 0
earn_rate = 0
lose_rate = 0
sum_hold_day = 0

for stock in stock_list:
    if os.path.isfile('./stock_data/DATA_' + stock + '.csv'):
        temp = []
        print('--------------------------------------------------------------')
        print(stock)
        with open(stock + '_DATA.csv') as csvfile:
            reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC) # change contents to floats
            # each row is a list
            for row in reader:
                temp.append(row)
        total_num = total_num + len(temp[:])
        #print(temp)
        for i in range(len(temp[:]) - wait_day):
            if temp[i][3] > temp[i][2] and temp[i + 1][2] > temp[i + 1][3] and i > curr_day:  # and temp[i][7] >= 0: # and temp[i][0] > temp[i][1] and temp[i][0] > temp[i][2] and temp[i][6] > 0 and temp[i][7] > -0.01:
                happen = happen + 1
                buy_day = i+1
                hold_day = 0
                rate = (temp[buy_day][0] - temp[buy_day-1][0]) / temp[buy_day-1][0]
                #print(rate)
                print('Buyday' + str(buy_day))
                curr_day = buy_day + hold_day
                while rate > -0.005 and curr_day <= len(temp[:]):
                    hold_day = hold_day + 1
                    prev_day = buy_day + hold_day - 1
                    curr_day = buy_day + hold_day
                    #time.sleep(0.005)
                    print(i)
                    #print(curr_day)
                    print(temp[curr_day][0])
                    rate = (temp[curr_day][0] - temp[prev_day][0]) / temp[prev_day][0]

                final_rate = (temp[buy_day+hold_day][0] - temp[buy_day][0]) / temp[buy_day][0]
                sum_rate = sum_rate + final_rate
                sum_hold_day = sum_hold_day + hold_day
                if final_rate >= 0:
                    earn = earn + 1
                    earn_rate = earn_rate + final_rate
                else:
                    lose = lose + 1
                    lose_rate = lose_rate + final_rate

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
'''
happen_rate = happen / total_num
win_rate = earn / happen
avr_earn_rate = sum_rate / happen
win_earn_rate = earn_rate/earn
lose_earn_rate = lose_rate/lose
avr_hold_day = sum_hold_day / happen

print('鳥嘴' + str(wait_day) + '天')
print('發生次數: ' + str(happen))
print('獲利次數: ' + str(earn))
print('發生機率: ' + str(round(100 * happen_rate, 2)) + '%')
print('勝率: ' + str(round(100 * win_rate, 2)) + '%')
print('期待值: ' + str(round(100 * avr_earn_rate, 2)) + '%')
print('獲利時的平均獲利: ' + str(round(100 * win_earn_rate, 2)) + '%')
print('損失時的平均獲利: ' + str(round(100 * lose_earn_rate, 2)) + '%')
print('平均持有天數: ' + str(round(avr_hold_day, 2)) + '天')


