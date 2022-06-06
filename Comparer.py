import csv
from ToolBox import text2list
import os.path
import math


name_list = ['鳥嘴', '鳥嘴_向上', '鳥嘴_向下', '鳥嘴_平緩',
             '半身以上', '半身以上向上', '半身以上向下', '半身以上平緩',
             '半身_以下犯上', '半身_以下犯上_向上', '半身_以下犯上_向下', '半身_以下犯上_平緩',
             '半身_超半', '半身_超半_向上', '半身_超半_向下', '半身_超半_平緩'
             '大行情', '60_100', '20_下半身']
name_list = ['反鳥嘴']

tactic_list = ['Kill_D2', 'Kill_D3', 'Kill_D23', 'none', '5 lower than 20']
tactic_list = ['none']

price_upper = 20000
price_lower = 0

for N in name_list:
    for T in tactic_list:
        stock_list = text2list('ALL.txt')
        wait_day = 10
        SD = [0] * wait_day
        avr_earn_rate = [0] * wait_day
        DATA = [[0] * 30 for i in range(wait_day)]

        for day in range(wait_day):
            day = wait_day - day - 1
            total_num = 0
            happen = 0
            earn = 0
            lose = 0
            sum_rate = 0
            earn_rate = 0
            lose_rate = 0
            sell_price = 0
            buy_price = 0
            rate_square = 0
            turn_down = 0
            turn_up = 0
            turn_down_low = 0
            turn_up_low = 0
            downward = [0] * 4
            upward = [0] * 4
            count_2 = 0
            count_3 = 0
            p_count_2 = 0
            p_count_3 = 0
            buy_day = 1
            buy_gap = 1

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
            test_name = N


            def tactic(num, i_, temp_):
                rate_buy_day = (temp_[i_+1][0] - temp_[i_][0]) / temp_[i_][0]
                if price_upper > temp_[i_ + buy_day][0] > price_lower:
                    if num == 'Kill_D1' and temp_[i_ + 2][0] > temp_[i_ + 1][0]:
                        return True
                    elif num == 'Kill_D2' and temp_[i_ + 3][0] > temp_[i_ + 1][0]:
                        return True
                    elif num == 'Kill_D3' and temp_[i_ + 4][0] > temp_[i_ + 1][0]:
                        return True
                    elif num == 'Kill_D4' and temp_[i_ + 5][0] > temp_[i_ + 1][0]:
                        return True
                    elif num == 'Kill_D5' and temp_[i_ + 6][0] > temp_[i_ + 1][0]:
                        return True
                    elif num == 'Kill_D6' and temp_[i_ + 7][0] > temp_[i_ + 1][0]:
                        return True
                    elif num == 'Kill_D2_rate3' and temp_[i_ + 3][0] > temp_[i_ + 1][0] and rate_buy_day > 0.03:
                        return True
                    elif num == 'Kill_D12' and temp_[i_ + 2][0] > temp_[i_ + 1][0] and temp_[i_ + 3][0] > temp_[i_ + 1][0]:
                        return True
                    elif num == '5 lower than 20' and temp_[i_][2] < temp_[i_][3]:
                        return True
                    elif num == 'none':
                        return True
                    else:
                        return False
                else:
                    return False


            def exp_(name, i_, curr_day_, temp_, tactic_name):
                # 鳥嘴
                upper = 0.01
                lower = -0.01
                slope_num = 6
                if name == '鳥嘴' and i_ > curr_day_ and temp_[i_][3] > temp_[i_][2] and temp_[i_ + 1][2] > temp_[i_ + 1][3] and tactic(tactic_name, i_, temp_):
                    # 前一天 20日價 > 5日價
                    # 買當天 5日價 > 20日價
                    return True
                if name == '反鳥嘴' and i_ > curr_day_ and temp_[i_][3] < temp_[i_][2] and temp_[i_ + 1][2] < temp_[i_ + 1][3] and tactic(tactic_name, i_, temp_):
                    # 前一天 20日價 > 5日價
                    # 買當天 5日價 > 20日價
                    return True
                elif name == '鳥嘴_向上' and i_ > curr_day_ and temp_[i_][3] > temp_[i_][2] and temp_[i_ + 1][2] > temp_[i_ + 1][3] and \
                        temp_[i_][slope_num] > upper and tactic(tactic_name, i_, temp_):
                    return True
                elif name == '鳥嘴_向下' and i_ > curr_day_ and temp_[i_][3] > temp_[i_][2] and temp_[i_ + 1][2] > temp_[i_ + 1][3] and \
                        temp_[i_][slope_num] <= lower and tactic(tactic_name, i_, temp_):
                    return True
                elif name == '鳥嘴_平緩' and i_ > curr_day_ and temp_[i_][3] > temp_[i_][2] and temp_[i_ + 1][2] > temp_[i_ + 1][3] and \
                        upper >= temp_[i_][slope_num] > lower and tactic(tactic_name, i_, temp_):
                    return True
                elif name == '半身' and i_ > curr_day_ and temp_[i_][2] > 0.5 * (temp_[i_][0] + temp_[i_][1]) and \
                        (temp_[i_ + 1][0] - temp_[i_ + 1][2]) >= abs(temp_[i_ + 1][2] - temp_[i_ + 1][1]) and tactic(tactic_name, i_, temp_):
                    # 前一天 五日價 > 0.5 (收盤價 & 開盤價)
                    # 買當天 (收盤價 - 五日價) >= abs(開盤價 - 五日價)
                    return True
                elif name == '反半身' and i_ > curr_day_ and temp_[i_][2] < 0.5 * (temp_[i_][0] + temp_[i_][1]) and \
                        (temp_[i_ + 1][2] - temp_[i_ + 1][0]) >= abs(temp_[i_ + 1][1] - temp_[i_ + 1][2]) and tactic(tactic_name, i_, temp_):
                    # 前一天 五日價 < 0.5 (收盤價 & 開盤價)
                    # 買當天 (收盤價 - 五日價) >= abs(開盤價 - 五日價)
                    return True
                elif name == '純半身' and i_ > curr_day_ and (temp_[i_ + 1][0] - temp_[i_ + 1][2]) >= abs(temp_[i_ + 1][2] - temp_[i_ + 1][1]) and tactic(tactic_name, i_, temp_):
                    # 買當天 (收盤價 - 五日價) >= abs(開盤價 - 五日價)
                    return True
                elif name == '5_下半身_向上' and i_ > curr_day_ and temp_[i_][2] > temp_[i_][0] and temp_[i_][2] > temp_[i_][1] and \
                        (temp_[i_ + 1][0] - temp_[i_ + 1][2]) >= abs(temp_[i_ + 1][2] - temp_[i_ + 1][1]) and temp_[i_][slope_num] > upper and tactic(tactic_name, i_, temp_):
                    return True
                elif name == '5_下半身_向下' and i_ > curr_day_ and temp_[i_][2] > temp_[i_][0] and temp_[i_][2] > temp_[i_][1] and \
                        (temp_[i_ + 1][0] - temp_[i_ + 1][2]) >= abs(temp_[i_ + 1][2] - temp_[i_ + 1][1]) and temp_[i_][slope_num] <= lower and tactic(tactic_name, i_, temp_):
                    return True
                elif name == '5_下半身_平緩' and i_ > curr_day_ and temp_[i_][2] > temp_[i_][0] and temp_[i_][2] > temp_[i_][1] and \
                        (temp_[i_ + 1][0] - temp_[i_ + 1][2]) >= abs(temp_[i_ + 1][2] - temp_[i_ + 1][1]) and upper >= temp_[i_][slope_num] > lower and tactic(tactic_name, i_, temp_):
                    return True
                elif name == '20_下半身' and i_ > curr_day_ and temp_[i_][3] > temp_[i_][0] and temp_[i_][3] > temp_[i_][1] and \
                        (temp_[i_ + 1][0] - temp_[i_ + 1][3]) >= abs(temp_[i_ + 1][3] - temp_[i_ + 1][1]) and tactic(tactic_name, i_, temp_):
                    # 前一天 20日價 > 收盤價 & 開盤價
                    # 買當天 (收盤價 - 20日價) >= abs(開盤價 - 20日價)
                    return True
                elif name == '大行情' and i_ > curr_day_ and not temp_[i_][2] > temp_[i_][3] > temp_[i_][17] > temp_[i_][18] > temp_[i_][19] and \
                        temp_[i_+buy_day][2] > temp_[i_+buy_day][3] > temp_[i_+buy_day][17] > temp_[i_+buy_day][18] > temp_[i_+buy_day][19] and \
                        tactic(tactic_name, i_, temp_):
                    return True
                elif name == '60_100' and i_ > curr_day_ and temp_[i_][18] > temp_[i_][17] and temp_[i_+1][18] < temp_[i_+1][17] and tactic(tactic_name, i_, temp_):
                    return True
                elif name == 'Underdog_CP' and temp[i_-6][0] > temp[i_-5][0] > temp[i_-4][0] > temp[i_-3][0] > temp[i_-2][0] > temp[i_-1][0]:# tactic(tactic_name, i_, temp_):
                    return True
                elif name == '漲停' and temp[i_][4] > 0.09:  # tactic(tactic_name, i_, temp_):
                    return True
                else:
                    return False


            for stock in stock_list:
                if os.path.isfile('./stock_data/DATA_' + stock + '.csv'):
                    temp = []
                    # print(stock)
                    with open('./stock_data/DATA_' + stock + '.csv') as csvfile:
                        reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)  # change contents to floats
                        # each row is a list
                        for row in reader:
                            temp.append(row)
                    total_num = total_num + len(temp[:])
                    # print(temp)
                    curr_day = 0

                    # day = 0 ~ (wait_day-1)

                    for i in range(len(temp[:]) - wait_day - 3):
                        if exp_(test_name, i, curr_day, temp, T):
                            curr_day = i + wait_day
                            happen = happen + 1
                            rate = (temp[i + day + buy_day + buy_gap][sell_price] - temp[i + buy_day][buy_price]) / temp[i + buy_day][buy_price]
                            sum_rate = sum_rate + rate
                            rate_square = rate_square + rate ** 2
                            next_rate = (temp[i + day + buy_day + buy_gap + 1][sell_price] - temp[i + buy_day][buy_price]) / temp[i + buy_day][buy_price]
                            if rate >= 0:
                                earn = earn + 1
                                earn_rate = earn_rate + rate
                                #if next_rate < 0:
                                    #turn_down = turn_down + 1
                            else:
                                lose = lose + 1
                                lose_rate = lose_rate + rate
                                #if next_rate >= 0:
                                    #turn_up = turn_up + 1
                            if rate < 0:
                                rate_ = (temp[i + day + buy_day + buy_gap + 1][sell_price] - temp[i + buy_day][buy_price]) / temp[i + buy_day][buy_price]
                                if rate_ < 0:
                                    count_2 = count_2 + 1
                                rate_ = (temp[i + day + buy_day + buy_gap + 2][sell_price] - temp[i + buy_day][buy_price]) / temp[i + buy_day][buy_price]
                                if rate_ < 0:
                                    count_3 = count_3 + 1
                            if rate >= 0:
                                rate_ = (temp[i + day + buy_day + buy_gap + 1][sell_price] - temp[i + buy_day][buy_price]) / temp[i + buy_day][buy_price]
                                if rate_ >= 0:
                                    p_count_2 = p_count_2 + 1
                                rate_ = (temp[i + day + buy_day + buy_gap + 2][sell_price] - temp[i + buy_day][buy_price]) / temp[i + buy_day][buy_price]
                                if rate_ >= 0:
                                    p_count_3 = p_count_3 + 1

            happen_rate = happen / total_num
            win_rate = earn / happen
            avr_earn_rate[day] = sum_rate / happen
            if earn != 0:
                win_earn_rate = earn_rate / earn
                positive_2_rate = p_count_2 / earn
                positive_3_rate = p_count_3 / earn
            else:
                win_earn_rate = 0
                positive_2_rate = 0
                positive_3_rate = 0

            if lose != 0:
                negative_2_rate = count_2 / lose
                negative_3_rate = count_3 / lose
                lose_earn_rate = lose_rate / lose
            else:
                negative_2_rate = 0
                negative_3_rate = 0
                lose_earn_rate = 0

            SD[day] = round(math.sqrt(rate_square / happen - avr_earn_rate[day] ** 2), 4)

            area = [0, 0, 0, 0, 0]

            # 檢查是否為常態分佈
            for stock in stock_list:
                if os.path.isfile('./stock_data/DATA_' + stock + '.csv'):
                    temp = []
                    with open('./stock_data/DATA_' + stock + '.csv') as csvfile:
                        reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)  # change contents to floats
                        # each row is a list
                        for row in reader:
                            temp.append(row)
                    total_num = total_num + len(temp[:])
                    curr_day = 0

                    for i in range(len(temp[:]) - wait_day - 3):
                        if exp_(test_name, i, curr_day, temp, T):
                            curr_day = i + wait_day
                            rate = (temp[i + day + buy_day + buy_gap][sell_price] - temp[i + buy_day][buy_price]) / temp[i + buy_day][buy_price]
                            next_rate = (temp[i + day + buy_day + buy_gap + 1][sell_price] - temp[i + buy_day][buy_price]) / temp[i + buy_day][buy_price]
                            if rate >= (SD[day] + avr_earn_rate[day]):
                                area[0] = area[0] + 1
                                if day != (wait_day - 1) and next_rate < (SD[day + 1] + avr_earn_rate[day + 1]):
                                    downward[0] = downward[0] + 1
                            elif rate >= avr_earn_rate[day]:
                                area[1] = area[1] + 1
                                if day != (wait_day - 1) and next_rate < avr_earn_rate[day + 1]:
                                    downward[1] = downward[1] + 1
                                if day != (wait_day - 1) and next_rate > (SD[day + 1] + avr_earn_rate[day + 1]):
                                    upward[0] = upward[0] + 1
                            elif avr_earn_rate[day] > rate >= 0:
                                area[2] = area[2] + 1
                                if day != (wait_day - 1) and next_rate < 0:
                                    downward[2] = downward[2] + 1
                                if day != (wait_day - 1) and next_rate > avr_earn_rate[day + 1]:
                                    upward[1] = upward[1] + 1
                            elif 0 > rate >= (avr_earn_rate[day] - SD[day]):
                                area[3] = area[3] + 1
                                if day != (wait_day - 1) and next_rate < (avr_earn_rate[day + 1] - SD[day + 1]):
                                    downward[3] = downward[3] + 1
                                if day != (wait_day - 1) and next_rate > 0:
                                    upward[2] = upward[2] + 1
                            else:
                                area[4] = area[4] + 1
                                if day != (wait_day - 1) and next_rate > (avr_earn_rate[day + 1] - SD[day + 1]):
                                    upward[3] = upward[3] + 1
            # 數據輸出
            downward_rate = [0] * 4
            upward_rate = [0] * 4
            for i in range(4):
                if area[i] != 0:
                    downward_rate[i] = round(100 * downward[i] / happen, 2)#area[i], 2)
                else:
                    downward_rate[i] = 0
            for i in range(4):
                if area[i + 1] != 0:
                    upward_rate[i] = round(100 * upward[i] / happen, 2)#area[i + 1], 2)
                else:
                    upward_rate[i] = 0

            print('\n' + test_name + T + str(day + 1) + '天')
            DATA[day][0] = day + 1
            print('發生次數: ' + str(happen))
            DATA[day][1] = happen
            print('獲利次數: ' + str(earn))
            DATA[day][2] = earn
            print('發生機率: ' + str(round(100 * happen_rate, 2)) + '%')
            DATA[day][3] = round(100 * happen_rate, 2)
            print('勝率: ' + str(round(100 * win_rate, 2)) + '%')
            DATA[day][4] = round(100 * win_rate, 2)
            print('期待值: ' + str(round(100 * avr_earn_rate[day], 2)) + '%')
            DATA[day][5] = round(100 * avr_earn_rate[day], 2)
            print('獲利時的平均獲利: ' + str(round(100 * win_earn_rate, 2)) + '%')
            DATA[day][6] = round(100 * win_earn_rate, 2)
            print('損失時的平均獲利: ' + str(round(100 * lose_earn_rate, 2)) + '%')
            DATA[day][7] = round(100 * lose_earn_rate, 2)
            print('標準差: ' + str(100 * SD[day]) + '%')
            DATA[day][8] = 100 * SD[day]

            DATA[day][9] = round(100 * positive_3_rate, 2)
            DATA[day][10] = round(100 * positive_2_rate, 2)

            DATA[day][11] = round(100 * area[0] / happen, 2)  # 0區
            DATA[day][12] = downward_rate[0]
            DATA[day][13] = round(100 * (SD[day] + avr_earn_rate[day]), 2)
            DATA[day][14] = upward_rate[0]
            DATA[day][15] = round(100 * area[1] / happen, 2)
            DATA[day][16] = downward_rate[1]
            DATA[day][17] = round(100 * avr_earn_rate[day], 2)
            DATA[day][18] = upward_rate[1]
            DATA[day][19] = round(100 * area[2] / happen, 2)
            DATA[day][20] = downward_rate[2]
            DATA[day][21] = 0
            DATA[day][22] = upward_rate[2]
            DATA[day][23] = round(100 * area[3] / happen, 2)
            DATA[day][24] = downward_rate[3]
            DATA[day][25] = round(100 * (avr_earn_rate[day] - SD[day]), 2)
            DATA[day][26] = upward_rate[3]
            DATA[day][27] = round(100 * area[4] / happen, 2)
            DATA[day][28] = round(100 * negative_2_rate, 2)
            DATA[day][29] = round(100 * negative_3_rate, 2)

        i = 0
        while os.path.isfile('Compare_DATA_' + test_name + '_' + T + '_' + str(price_upper) + '_' + str(price_lower) + '_' + str(i) + '.csv'):
            i = i+1

        with open('Compare_DATA_' + test_name + '_' + T + '_' + str(price_upper) + '_' + str(price_lower) + '_' + str(i) + '.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for i in range(len(DATA[:])):
                writer.writerow(DATA[i])
