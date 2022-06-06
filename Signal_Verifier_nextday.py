from datetime import datetime
import os.path
import time
import csv
import win32api
from ToolBox import text2list


def signal_type(name_, last_, slope_, align_t_, align_y_, i_, temp_):
    CP_yd_ = temp_[i_ - 1][0]
    CP_td_ = temp_[i_][0]
    OP_td_ = temp_[i_][1]
    avr_5_yd_ = temp_[i_ - 1][2]
    avr_20_yd_ = temp_[i_ - 1][3]
    avr_60_yd_ = temp_[i_ - 1][17]
    avr_5_td_ = temp_[i_][2]
    avr_20_td_ = temp_[i_][3]
    avr_60_td_ = temp_[i_][17]
    slope_5_yd_ = temp_[i_ - 1][6]
    slope_20_yd_ = temp_[i_ - 1][7]
    last_low_ = temp_[i_][24]
    last_high_ = temp_[i_][25]
    last_last_low_ = temp_[i_][26]
    last_last_high_ = temp_[i_][27]
    vol = temp_[i_][12]
    body_ = temp_[i_][28]
    y_flag = False
    t_flag = False
    last_flag = False
    s_flag = False

    if align_t_ == '5↘20↘60' and avr_5_td_ > avr_20_td_ > avr_60_td_:
        y_flag = True
    elif align_t_ == '5↘60↘20' and avr_5_td_ > avr_60_td_ > avr_20_td_:
        y_flag = True
    elif align_t_ == '60↘5↘20' and avr_60_td_ > avr_5_td_ > avr_20_td_:
        y_flag = True
    elif align_t_ == '60↘20↘5' and avr_60_td_ > avr_20_td_ > avr_5_td_:
        y_flag = True
    elif align_t_ == '20↘60↘5' and avr_20_td_ > avr_60_td_ > avr_5_td_:
        y_flag = True
    elif align_t_ == '20↘5↘60' and avr_20_td_ > avr_5_td_ > avr_60_td_:
        y_flag = True
    elif align_t_ == '0':
        y_flag = True
    else:
        y_flag = False

    if align_y_ == '5↘20↘60' and avr_5_yd_ > avr_20_yd_ > avr_60_yd_:
        t_flag = True
    elif align_y_ == '5↘60↘20' and avr_5_yd_ > avr_60_yd_ > avr_20_yd_:
        t_flag = True
    elif align_y_ == '60↘5↘20' and avr_60_yd_ > avr_5_yd_ > avr_20_yd_:
        t_flag = True
    elif align_y_ == '60↘20↘5' and avr_60_yd_ > avr_20_yd_ > avr_5_yd_:
        t_flag = True
    elif align_y_ == '20↘60↘5' and avr_20_yd_ > avr_60_yd_ > avr_5_yd_:
        t_flag = True
    elif align_y_ == '20↘5↘60' and avr_20_yd_ > avr_5_yd_ > avr_60_yd_:
        t_flag = True
    elif align_y_ == '0':
        t_flag = True
    else:
        t_flag = False

    if last_ == 'LastLow' and avr_5_yd_ > last_low_:
        last_flag = True
    elif last_ == 'Last2High' and avr_5_yd_ > last_last_high_:
        last_flag = True
    elif last_ == 'LastHigh' and avr_5_yd_ < last_high_:
        last_flag = True
    elif last_ == 'Last2low' and avr_5_yd_ < last_last_low_:
        last_flag = True
    elif last_ == 'LastNone':
        last_flag = True
    else:
        last_flag = False

    if slope_ == 'slp↗' and slope_5_yd_ > 0:
        s_flag = True
    elif slope_ == 'slp↘' and slope_5_yd_ < 0:
        s_flag = True
    elif slope_ == 'slp↕':
        s_flag = True
    else:
        s_flag = False

    if y_flag is True and t_flag is True and last_flag is True and s_flag is True:
        if name_ == 'Body+' and CP_yd_ < avr_5_yd_ and CP_td_ - avr_5_td_ > abs(OP_td_ - avr_5_td_) and vol > 2000 \
                and body_ > 0:
            return True
        elif name_ == 'Body2+' and CP_yd_ < avr_5_yd_ and CP_yd_ < avr_20_yd_ and CP_td_ > avr_5_td_ \
                and CP_td_ > avr_20_td_ and vol > 2000 and body_ > 0:
            return True
        elif name_ == 'Body3+' and CP_yd_ < avr_5_yd_ and CP_yd_ < avr_20_yd_ and CP_yd_ < avr_60_yd_ \
                and CP_td_ > avr_5_td_ and CP_td_ > avr_20_td_ and CP_td_ > avr_60_td_ and vol > 2000 and body_ > 0:
            return True
        elif name_ == 'Body-' and CP_yd_ > avr_5_yd_ and avr_5_td_ - CP_td_ > abs(OP_td_ - avr_5_td_) and vol > 2000 \
                and body_ < 0:
            return True
        elif name_ == 'Body2-' and CP_yd_ > avr_5_yd_ and CP_yd_ > avr_20_yd_ and CP_td_ < avr_5_td_ \
                and CP_td_ < avr_20_td_ and vol > 2000 and body_ < 0:
            return True
        elif name_ == 'Body3-' and CP_yd_ > avr_5_yd_ and CP_yd_ > avr_20_yd_ and CP_yd_ > avr_60_yd_ \
                and CP_td_ < avr_5_td_ and CP_td_ < avr_20_td_ and CP_td_ < avr_60_td_ and vol > 2000 and body_ < 0:
            return True
        elif name_ == 'None' and vol > 2000 and body_ > 0:
            return True
    else:
        return False


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
day_combination = ['5', '20', '60']
align_list = ['5↘20↘60', '5↘60↘20', '60↘5↘20', '60↘20↘5', '20↘60↘5', '20↘5↘60']
last_list = ['LastLow', 'Last2High', 'LastHigh', 'Last2low']
name_list = ['Body+', 'Body-', 'None']
slope_list = ['slp↗', 'slp↘']
stock_list = text2list('test.txt')
total_list = []

Big = []
with open('./stock_data/DATA/DATA_Indices.csv') as csvfile:
    reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)  # change contents to floats
    # each row is a list
    for row in reader:
        Big.append(row)


def Big_finder(year_, month_, date_, Big_):
    for i_ in range(len(Big_)):
        if year_ == Big_[i_][14] and month_ == Big_[i_][15] and date_ == Big_[i_][16]:
            return i_


length = len(align_list) * len(align_list) * len(last_list) * len(name_list) * len(slope_list)
print(str(length) + ' research list\n')
for name in name_list:
    for last in last_list:
        for align_y in align_list:
            for align_t in align_list:
                for slope in slope_list:
                    total = 0
                    total_score_5 = 0
                    total_score_10 = 0
                    total_score_20 = 0
                    total_score_30 = 0
                    write_up_list = []
                    write_down_list = []
                    total_list_name = str(name) + '_' + str(last) + '_Y' + str(align_y) + '_T' + str(align_t) + '_' + str(slope)
                    print(str(name) + '_' + str(last) + '_Y' + str(align_y) + '_T' + str(align_t) + '_' + str(slope))
                    for stock in stock_list:
                        if os.path.isfile('./stock_data/DATA/DATA_' + stock + '.csv'):
                            #print(stock)
                            temp = []
                            with open('./stock_data/DATA/DATA_' + stock + '.csv') as csvfile:
                                reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)  # change contents to floats
                                # each row is a list
                                for row in reader:
                                    temp.append(row)
                            for j in range(301, len(temp[:])-31):
                                if signal_type(name, last, slope, align_t, align_y, j, temp):

                                    def score(temp_list, index, day):
                                        score_def = (temp_list[index + day - 1][0] + temp_list[index + day][0] + temp_list[index + day + 1][0] - temp_list[index][0] * 3) / (3 * temp_list[index][0]) * 100
                                        return score_def

                                    score_5D = score(temp, j, 5)
                                    score_10D = score(temp, j, 10)
                                    score_20D = score(temp, j, 20)
                                    score_30D = score(temp, j, 30)

                                    #if score_5D < 61 and score_10D < 159 and score_20D < 572 and score_30D < 1644:
                                    if score_5D < 61 and (score_10D+100) / (score_5D+100) < 259 / 161 \
                                            and (score_20D+100) / (score_10D+100) < 672 / 259 and (score_30D+100) / (score_20D+100) < 1744 / 672:
                                        total_score_5 = total_score_5 + score_5D
                                        total_score_10 = total_score_10 + score_10D
                                        total_score_20 = total_score_20 + score_20D
                                        total_score_30 = total_score_30 + score_30D

                                        year = temp[j][14]
                                        month = temp[j][15]
                                        date = temp[j][16]
                                        CP_td = temp[j][0]
                                        OP_td = temp[j][1]
                                        avr_60_yd = temp[j - 1][17]
                                        avr_20_yd = temp[j - 1][3]
                                        avr_5_yd = temp[j - 1][2]
                                        slope_60 = temp[j - 1][20]
                                        slope_20 = temp[j - 1][7]
                                        slope_5 = temp[j - 1][6]

                                        last_low = temp[j][24]
                                        last_high = temp[j][25]
                                        last_last_low = temp[j][26]
                                        last_last_high = temp[j][27]

                                        td_body = temp[j][28]
                                        td_uline = temp[j][29]
                                        td_lline = temp[j][30]
                                        yd_body = temp[j-1][28]
                                        yd_uline = temp[j-1][29]
                                        yd_lline = temp[j-1][30]
                                        yyd_body = temp[j-2][28]
                                        yyd_uline = temp[j-2][29]
                                        yyd_lline = temp[j-2][30]

                                        Big_date = Big_finder(temp[j][14], temp[j][15], temp[j][16], Big)
                                        Big_CP_slope = Big[Big_date][4]
                                        Big_5D_slope = Big[Big_date][6]
                                        Big_CP = Big[Big_date][0]

                                        write_list = [stock, year, month, date, CP_td, Big_CP,
                                                      last_low, last_high, last_last_low, last_last_high,
                                                      avr_5_yd, avr_20_yd, avr_60_yd,
                                                      slope_5, slope_20, slope_60,
                                                      yyd_body, yd_body, td_body,
                                                      Big_CP_slope, Big_5D_slope,
                                                      score_5D, score_10D, score_20D, score_30D]

                                        if score_5D <= 0:
                                            write_down_list.append(write_list)
                                        elif score_5D > 0:
                                            write_up_list.append(write_list)

                                        total = total + 1

                    if total >= 40:
                        print('Total = ' + str(total))
                        print('5D_score = ' + str(total_score_5 / total))
                        print('10D_score = ' + str(total_score_10 / total))
                        print('20D_score = ' + str(total_score_20 / total))
                        print('30D_score = ' + str(total_score_30 / total) + '\n')
                        total_list.append([name, total, last, align_y, align_t, total_score_5 / total,
                                           total_score_10 / total, total_score_20 / total, total_score_30 / total])
                        first_row = ['stock', 'Year', 'Month', 'Date', 'CP_td', 'Big CP',
                                     'LLow', 'LHigh', 'LLLow', 'LLHigh',
                                     'avr_5D_yd', 'avr_20D_yd', 'avr_60D_yd',
                                     'slp_5D_yd', 'slp_20D_yd', 'slp_60D_yd',
                                     'YYD_body', 'YD_body', 'TD_body',
                                     'Big CP slope', 'Big 5D slope',
                                     '5D score', '10D score', '20D score', '30D score']
                        i = 0
                        while os.path.isfile('./Comparison/Signal_verifier_150/' + str(name) + '_' + str(last) + '_Y' + str(
                                align_y) + '_T' + str(align_t) + '_' + str(slope) + '_↗_' + str(i) + '.csv'):
                            i = i + 1
                        with open('./Comparison/Signal_verifier_150/' + str(name) + '_' + str(last) + '_Y' + str(
                                align_y) + '_T' + str(align_t) + '_' + str(slope) + '_↗_' + str(i) + '.csv', 'w', newline='') as csvfile:
                            writer = csv.writer(csvfile)
                            writer.writerow(first_row)
                            writer.writerows(write_up_list)

                        i = 0
                        while os.path.isfile('./Comparison/Signal_verifier_150/' + str(name) + '_' + str(last) + '_Y' + str(
                                align_y) + '_T' + str(align_t) + '_' + str(slope) + '_↘_' + str(i) + '.csv'):
                            i = i + 1
                        with open('./Comparison/Signal_verifier_150/' + str(name) + '_' + str(last) + '_Y' + str(
                                align_y) + '_T' + str(align_t) + '_' + str(slope) + '_↘_' + str(i) + '.csv', 'w', newline='') as csvfile:
                            writer = csv.writer(csvfile)
                            writer.writerow(first_row)
                            writer.writerows(write_down_list)

                    else:
                        print('No data. \n')
i = 0
while os.path.isfile('./Comparison/Signal_verifier_150/Total_list+_' + str(i) + '.csv'):
    i = i + 1
with open('./Comparison/Signal_verifier_150/Total_list+_' + str(i) + '.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(
        ['name', 'total', '> last', 'align_y', 'align_t', '5 score', '10 score', '20 score', '30 score'])
    writer.writerows(total_list)

toc = time.perf_counter()
print(f"Downloaded the tutorial in {(toc - tic) / 60:0.4f} mins")

win32api.MessageBox(0, 'Finished', 'Reminder', 0x00001000)
