import os.path
import time
import csv
import win32api
from ToolBox import text2list


def score_p(temp_list, index, day, p):
    if temp_list[index][0] != 0:
        score_def = (temp_list[index + day - 1][p] + temp_list[index + day][p] + temp_list[index + day + 1][p] -
                     temp_list[index][0] * 3) / (3 * temp_list[index][0]) * 100
        return score_def
    else:
        return 0


def signal_type(i_, temp_):
    """
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
    """
    vol = temp_[i_][12]
    if vol > 2000:
        CP_yd_ = temp_[i_ - 1][0]
        CP_td_ = temp_[i_][0]
        OP_td_ = temp_[i_][1]
        avr_5_yd_ = temp_[i_ - 1][2]
        avr_20_yd_ = temp_[i_ - 1][3]
        avr_60_yd_ = temp_[i_ - 1][17]
        avr_20_td_ = temp_[i_][3]
        avr_60_td_ = temp_[i_][17]
        slope_5_yd_ = temp_[i_ - 1][6]
        HP5 = score_p(temp_, i_, 5, 8)
        LP5 = score_p(temp_, i_, 5, 9)
        HP10 = score_p(temp_, i_, 10, 8)
        LP10 = score_p(temp_, i_, 10, 9)
        HP20 = score_p(temp_, i_, 20, 8)
        LP20 = score_p(temp_, i_, 20, 9)
        HP30 = score_p(temp_, i_, 30, 8)
        LP30 = score_p(temp_, i_, 30, 9)
        HP60 = score_p(temp_, i_, 60, 8)
        LP60 = score_p(temp_, i_, 60, 9)

        # slope_20_yd_ = temp_[i_ - 1][7]

        a = temp_[i_][27]  # last last high
        b = temp_[i_][25]  # last high
        avr_5_td_ = temp_[i_][2]  # avr5_td
        d = temp_[i_][24]  # last low
        e = temp_[i_][26]  # last last low
        body_ = temp_[i_][28]

        year = temp[i_][14]
        month = temp[i_][15]
        date = temp[i_][16]
        CP_td = temp[i_][0]
        avr_60_yd = temp[i_ - 1][17]
        avr_20_yd = temp[i_ - 1][3]
        avr_5_yd = temp[i_ - 1][2]
        slope_60 = temp[i_ - 1][20]
        slope_20 = temp[i_ - 1][7]
        slope_5 = temp[i_ - 1][6]

        last_low = temp[i_][24]
        last_high = temp[i_][25]
        last_last_low = temp[i_][26]
        last_last_high = temp[i_][27]

        td_body = temp[i_][28]
        # yd_body = temp[i_ - 1][28]
        # yyd_body = temp[i_ - 2][28]

        score_5D = score_p(temp, i_, 5, 0)
        score_10D = score_p(temp, i_, 10, 0)
        score_20D = score_p(temp, i_, 20, 0)
        score_30D = score_p(temp, i_, 30, 0)
        score_60D = score_p(temp, i_, 60, 0)

        last_ = ''
        align_t_ = ''
        align_y_ = ''

        if score_5D < 61 and (score_10D + 100) / (score_5D + 100) < 259 / 161 \
                and (score_20D + 100) / (score_10D + 100) < 672 / 259 \
                and (score_30D + 100) / (score_20D + 100) < 1744 / 672 \
                and (score_60D + 100) / (score_30D + 100) < 30448 / 1744:

            if avr_5_td_ >= avr_20_td_ >= avr_60_td_:
                align_t_ = '5↘20↘60'
            elif avr_5_td_ >= avr_60_td_ >= avr_20_td_:
                align_t_ = '5↘60↘20'
            elif avr_60_td_ >= avr_5_td_ >= avr_20_td_:
                align_t_ = '60↘5↘20'
            elif avr_60_td_ >= avr_20_td_ >= avr_5_td_:
                align_t_ = '60↘20↘5'
            elif avr_20_td_ >= avr_60_td_ >= avr_5_td_:
                align_t_ = '20↘60↘5'
            elif avr_20_td_ >= avr_5_td_ >= avr_60_td_:
                align_t_ = '20↘5↘60'

            if avr_5_yd_ >= avr_20_yd_ >= avr_60_yd_:
                align_y_ = '5↘20↘60'
            elif avr_5_yd_ >= avr_60_yd_ >= avr_20_yd_:
                align_y_ = '5↘60↘20'
            elif avr_60_yd_ >= avr_5_yd_ >= avr_20_yd_:
                align_y_ = '60↘5↘20'
            elif avr_60_yd_ >= avr_20_yd_ >= avr_5_yd_:
                align_y_ = '60↘20↘5'
            elif avr_20_yd_ >= avr_60_yd_ >= avr_5_yd_:
                align_y_ = '20↘60↘5'
            elif avr_20_yd_ >= avr_5_yd_ >= avr_60_yd_:
                align_y_ = '20↘5↘60'

            if a >= b >= avr_5_td_ >= d >= e:
                last_ = 'abcde'
            elif a >= b >= avr_5_td_ >= e >= d:
                last_ = 'abced'
            elif a >= b >= d >= avr_5_td_ >= e:
                last_ = 'abdce'
            elif a >= b >= d >= e >= avr_5_td_:
                last_ = 'abdec'
            elif a >= b >= e >= avr_5_td_ >= d:
                last_ = 'abecd'
            elif a >= b >= e >= d >= avr_5_td_:
                last_ = 'abedc'
            elif a >= avr_5_td_ >= b >= d >= e:
                last_ = 'acbde'
            elif a >= avr_5_td_ >= b >= e >= d:
                last_ = 'acbed'
            elif a >= avr_5_td_ >= d >= b >= e:
                last_ = 'acdbe'
            elif a >= avr_5_td_ >= d >= e >= b:
                last_ = 'acdeb'
            elif a >= avr_5_td_ >= e >= b >= d:
                last_ = 'acebd'
            elif a >= avr_5_td_ >= e >= d >= b:
                last_ = 'acedb'
            elif a >= d >= b >= avr_5_td_ >= e:
                last_ = 'adbce'
            elif a >= d >= b >= e >= avr_5_td_:
                last_ = 'adbec'
            elif a >= d >= avr_5_td_ >= b >= e:
                last_ = 'adcbe'
            elif a >= d >= avr_5_td_ >= e >= b:
                last_ = 'adceb'
            elif a >= d >= e >= b >= avr_5_td_:
                last_ = 'adebc'
            elif a >= d >= e >= avr_5_td_ >= b:
                last_ = 'adecb'
            elif a >= e >= b >= avr_5_td_ >= d:
                last_ = 'aebcd'
            elif a >= e >= b >= d >= avr_5_td_:
                last_ = 'aebdc'
            elif a >= e >= avr_5_td_ >= b >= d:
                last_ = 'aecbd'
            elif a >= e >= avr_5_td_ >= d >= b:
                last_ = 'aecdb'
            elif a >= e >= d >= b >= avr_5_td_:
                last_ = 'aedbc'
            elif a >= e >= d >= avr_5_td_ >= b:
                last_ = 'aedcb'
            elif b >= a >= avr_5_td_ >= d >= e:
                last_ = 'bacde'
            elif b >= a >= avr_5_td_ >= e >= d:
                last_ = 'baced'
            elif b >= a >= d >= avr_5_td_ >= e:
                last_ = 'badce'
            elif b >= a >= d >= e >= avr_5_td_:
                last_ = 'badec'
            elif b >= a >= e >= avr_5_td_ >= d:
                last_ = 'baecd'
            elif b >= a >= e >= d >= avr_5_td_:
                last_ = 'baedc'
            elif b >= avr_5_td_ >= a >= d >= e:
                last_ = 'bcade'
            elif b >= avr_5_td_ >= a >= e >= d:
                last_ = 'bcaed'
            elif b >= avr_5_td_ >= d >= a >= e:
                last_ = 'bcdae'
            elif b >= avr_5_td_ >= d >= e >= a:
                last_ = 'bcdea'
            elif b >= avr_5_td_ >= e >= a >= d:
                last_ = 'bcead'
            elif b >= avr_5_td_ >= e >= d >= a:
                last_ = 'bceda'
            elif b >= d >= a >= avr_5_td_ >= e:
                last_ = 'bdace'
            elif b >= d >= a >= e >= avr_5_td_:
                last_ = 'bdaec'
            elif b >= d >= avr_5_td_ >= a >= e:
                last_ = 'bdcae'
            elif b >= d >= avr_5_td_ >= e >= a:
                last_ = 'bdcea'
            elif b >= d >= e >= a >= avr_5_td_:
                last_ = 'bdeac'
            elif b >= d >= e >= avr_5_td_ >= a:
                last_ = 'bdeca'
            elif b >= e >= a >= avr_5_td_ >= d:
                last_ = 'beacd'
            elif b >= e >= a >= d >= avr_5_td_:
                last_ = 'beadc'
            elif b >= e >= avr_5_td_ >= a >= d:
                last_ = 'becad'
            elif b >= e >= avr_5_td_ >= d >= a:
                last_ = 'becda'
            elif b >= e >= d >= a >= avr_5_td_:
                last_ = 'bedac'
            elif b >= e >= d >= avr_5_td_ >= a:
                last_ = 'bedca'
            elif avr_5_td_ >= a >= b >= d >= e:
                last_ = 'cabde'
            elif avr_5_td_ >= a >= b >= e >= d:
                last_ = 'cabed'
            elif avr_5_td_ >= a >= d >= b >= e:
                last_ = 'cadbe'
            elif avr_5_td_ >= a >= d >= e >= b:
                last_ = 'cadeb'
            elif avr_5_td_ >= a >= e >= b >= d:
                last_ = 'caebd'
            elif avr_5_td_ >= a >= e >= d >= b:
                last_ = 'caedb'
            elif avr_5_td_ >= b >= a >= d >= e:
                last_ = 'cbade'
            elif avr_5_td_ >= b >= a >= e >= d:
                last_ = 'cbaed'
            elif avr_5_td_ >= b >= d >= a >= e:
                last_ = 'cbdae'
            elif avr_5_td_ >= b >= d >= e >= a:
                last_ = 'cbdea'
            elif avr_5_td_ >= b >= e >= a >= d:
                last_ = 'cbead'
            elif avr_5_td_ >= b >= e >= d >= a:
                last_ = 'cbeda'
            elif avr_5_td_ >= d >= a >= b >= e:
                last_ = 'cdabe'
            elif avr_5_td_ >= d >= a >= e >= b:
                last_ = 'cdaeb'
            elif avr_5_td_ >= d >= b >= a >= e:
                last_ = 'cdbae'
            elif avr_5_td_ >= d >= b >= e >= a:
                last_ = 'cdbea'
            elif avr_5_td_ >= d >= e >= a >= b:
                last_ = 'cdeab'
            elif avr_5_td_ >= d >= e >= b >= a:
                last_ = 'cdeba'
            elif avr_5_td_ >= e >= a >= b >= d:
                last_ = 'ceabd'
            elif avr_5_td_ >= e >= a >= d >= b:
                last_ = 'ceadb'
            elif avr_5_td_ >= e >= b >= a >= d:
                last_ = 'cebad'
            elif avr_5_td_ >= e >= b >= d >= a:
                last_ = 'cebda'
            elif avr_5_td_ >= e >= d >= a >= b:
                last_ = 'cedab'
            elif avr_5_td_ >= e >= d >= b >= a:
                last_ = 'cedba'
            elif d >= a >= b >= avr_5_td_ >= e:
                last_ = 'dabce'
            elif d >= a >= b >= e >= avr_5_td_:
                last_ = 'dabec'
            elif d >= a >= avr_5_td_ >= b >= e:
                last_ = 'dacbe'
            elif d >= a >= avr_5_td_ >= e >= b:
                last_ = 'daceb'
            elif d >= a >= e >= b >= avr_5_td_:
                last_ = 'daebc'
            elif d >= a >= e >= avr_5_td_ >= b:
                last_ = 'daecb'
            elif d >= b >= a >= avr_5_td_ >= e:
                last_ = 'dbace'
            elif d >= b >= a >= e >= avr_5_td_:
                last_ = 'dbaec'
            elif d >= b >= avr_5_td_ >= a >= e:
                last_ = 'dbcae'
            elif d >= b >= avr_5_td_ >= e >= a:
                last_ = 'dbcea'
            elif d >= b >= e >= a >= avr_5_td_:
                last_ = 'dbeac'
            elif d >= b >= e >= avr_5_td_ >= a:
                last_ = 'dbeca'
            elif d >= avr_5_td_ >= a >= b >= e:
                last_ = 'dcabe'
            elif d >= avr_5_td_ >= a >= e >= b:
                last_ = 'dcaeb'
            elif d >= avr_5_td_ >= b >= a >= e:
                last_ = 'dcbae'
            elif d >= avr_5_td_ >= b >= e >= a:
                last_ = 'dcbea'
            elif d >= avr_5_td_ >= e >= a >= b:
                last_ = 'dceab'
            elif d >= avr_5_td_ >= e >= b >= a:
                last_ = 'dceba'
            elif d >= e >= a >= b >= avr_5_td_:
                last_ = 'deabc'
            elif d >= e >= a >= avr_5_td_ >= b:
                last_ = 'deacb'
            elif d >= e >= b >= a >= avr_5_td_:
                last_ = 'debac'
            elif d >= e >= b >= avr_5_td_ >= a:
                last_ = 'debca'
            elif d >= e >= avr_5_td_ >= a >= b:
                last_ = 'decab'
            elif d >= e >= avr_5_td_ >= b >= a:
                last_ = 'decba'
            elif e >= a >= b >= avr_5_td_ >= d:
                last_ = 'eabcd'
            elif e >= a >= b >= d >= avr_5_td_:
                last_ = 'eabdc'
            elif e >= a >= avr_5_td_ >= b >= d:
                last_ = 'eacbd'
            elif e >= a >= avr_5_td_ >= d >= b:
                last_ = 'eacdb'
            elif e >= a >= d >= b >= avr_5_td_:
                last_ = 'eadbc'
            elif e >= a >= d >= avr_5_td_ >= b:
                last_ = 'eadcb'
            elif e >= b >= a >= avr_5_td_ >= d:
                last_ = 'ebacd'
            elif e >= b >= a >= d >= avr_5_td_:
                last_ = 'ebadc'
            elif e >= b >= avr_5_td_ >= a >= d:
                last_ = 'ebcad'
            elif e >= b >= avr_5_td_ >= d >= a:
                last_ = 'ebcda'
            elif e >= b >= d >= a >= avr_5_td_:
                last_ = 'ebdac'
            elif e >= b >= d >= avr_5_td_ >= a:
                last_ = 'ebdca'
            elif e >= avr_5_td_ >= a >= b >= d:
                last_ = 'ecabd'
            elif e >= avr_5_td_ >= a >= d >= b:
                last_ = 'ecadb'
            elif e >= avr_5_td_ >= b >= a >= d:
                last_ = 'ecbad'
            elif e >= avr_5_td_ >= b >= d >= a:
                last_ = 'ecbda'
            elif e >= avr_5_td_ >= d >= a >= b:
                last_ = 'ecdab'
            elif e >= avr_5_td_ >= d >= b >= a:
                last_ = 'ecdba'
            elif e >= d >= a >= b >= avr_5_td_:
                last_ = 'edabc'
            elif e >= d >= a >= avr_5_td_ >= b:
                last_ = 'edacb'
            elif e >= d >= b >= a >= avr_5_td_:
                last_ = 'edbac'
            elif e >= d >= b >= avr_5_td_ >= a:
                last_ = 'edbca'
            elif e >= d >= avr_5_td_ >= a >= b:
                last_ = 'edcab'
            elif e >= d >= avr_5_td_ >= b >= a:
                last_ = 'edcba'

            if slope_5_yd_ >= 0:
                slope_ = 'slp↗'
            else:
                slope_ = 'slp↘'

            if CP_yd_ < avr_5_yd_ and CP_yd_ < avr_20_yd_ and CP_td_ > avr_5_td_ \
                    and CP_td_ > avr_20_td_ and body_ > 0:
                name_ = 'Body2+'
            elif CP_yd_ < avr_5_yd_ and CP_td_ - avr_5_td_ > abs(OP_td_ - avr_5_td_) and body_ > 0:
                name_ = 'Body+'
            elif CP_yd_ > avr_5_yd_ and CP_yd_ > avr_20_yd_ and CP_td_ < avr_5_td_ \
                    and CP_td_ < avr_20_td_ and body_ < 0:
                name_ = 'Body2-'
            elif CP_yd_ > avr_5_yd_ and avr_5_td_ - CP_td_ > abs(OP_td_ - avr_5_td_) and body_ < 0:
                name_ = 'Body-'
            elif body_ == 3:
                name_ = 'None3+'
            elif 0 <= body_ < 3:
                name_ = 'None+'
            elif body_ == -3:
                name_ = 'None3-'
            elif 0 > body_ > -3:
                name_ = 'None-'

            return [True, name_, last_, slope_, align_t_, align_y_, stock,
                    year, month, date, CP_td, avr_5_td_,
                    last_low, last_high, last_last_low, last_last_high,
                    avr_5_yd, avr_20_yd, avr_60_yd,
                    slope_5, slope_20, slope_60, td_body,
                    HP5, HP10, HP20, HP30, HP60,
                    LP5, LP10, LP20, LP30, LP60,
                    score_5D, score_10D, score_20D, score_30D, score_60D]
        else:
            return [False]
    else:
        return [False]


tic = time.perf_counter()
align_list = ['5↘20↘60', '5↘60↘20', '60↘5↘20', '60↘20↘5', '20↘60↘5', '20↘5↘60']
last_list = ['abcde',
             'abced',
             'abdce',
             'abdec',
             'abecd',
             'abedc',
             'acbde',
             'acbed',
             'acdbe',
             'acdeb',
             'acebd',
             'acedb',
             'adbce',
             'adbec',
             'adcbe',
             'adceb',
             'adebc',
             'adecb',
             'aebcd',
             'aebdc',
             'aecbd',
             'aecdb',
             'aedbc',
             'aedcb',
             'bacde',
             'baced',
             'badce',
             'badec',
             'baecd',
             'baedc',
             'bcade',
             'bcaed',
             'bcdae',
             'bcdea',
             'bcead',
             'bceda',
             'bdace',
             'bdaec',
             'bdcae',
             'bdcea',
             'bdeac',
             'bdeca',
             'beacd',
             'beadc',
             'becad',
             'becda',
             'bedac',
             'bedca',
             'cabde',
             'cabed',
             'cadbe',
             'cadeb',
             'caebd',
             'caedb',
             'cbade',
             'cbaed',
             'cbdae',
             'cbdea',
             'cbead',
             'cbeda',
             'cdabe',
             'cdaeb',
             'cdbae',
             'cdbea',
             'cdeab',
             'cdeba',
             'ceabd',
             'ceadb',
             'cebad',
             'cebda',
             'cedab',
             'cedba',
             'dabce',
             'dabec',
             'dacbe',
             'daceb',
             'daebc',
             'daecb',
             'dbace',
             'dbaec',
             'dbcae',
             'dbcea',
             'dbeac',
             'dbeca',
             'dcabe',
             'dcaeb',
             'dcbae',
             'dcbea',
             'dceab',
             'dceba',
             'deabc',
             'deacb',
             'debac',
             'debca',
             'decab',
             'decba',
             'eabcd',
             'eabdc',
             'eacbd',
             'eacdb',
             'eadbc',
             'eadcb',
             'ebacd',
             'ebadc',
             'ebcad',
             'ebcda',
             'ebdac',
             'ebdca',
             'ecabd',
             'ecadb',
             'ecbad',
             'ecbda',
             'ecdab',
             'ecdba',
             'edabc',
             'edacb',
             'edbac',
             'edbca',
             'edcab',
             'edcba']
name_list = ['None+', 'None-', 'None3+', 'None3-', 'Body+', 'Body2+', 'Body-', 'Body2-']
slope_list = ['slp↗', 'slp↘']
stock_list = text2list('ALL.txt')
total_list = []
folder = './Comparison/Signal_verifier_2000-/'
folder = './Comparison/Signal_verifier_2000+/'

length = len(align_list) * len(align_list) * len(last_list) * len(name_list) * len(slope_list) / 2
print(str(length) + ' research list\n')

total_number = 0
last_signal = []
for stock in stock_list:
    if os.path.isfile('./stock_data/DATA/DATA_' + stock + '.csv'):
        # print(stock)
        temp = []
        with open('./stock_data/DATA/DATA_' + stock + '.csv') as csvfile:
            reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)  # change contents to floats
            # each row is a list
            for row in reader:
                temp.append(row)
        total_number = total_number + len(temp[:]) - 122
        for j in range(61, len(temp[:]) - 61):
            ans = signal_type(j, temp)
            if ans[0] is True:
                first_row = ['stock', 'year', 'month', 'date', 'CP_td', 'avr_5_td',
                             'last_low', 'last_high', 'last_last_low', 'last_last_high',
                             'avr_5_yd', 'avr_20_yd', 'avr_60_yd',
                             'slope_5', 'slope_20', 'slope_60', 'td_body',
                             'HP5', 'HP10', 'HP20', 'HP30', 'HP60',
                             'LP5', 'LP10', 'LP20', 'LP30', 'LP60',
                             'score_5D', 'score_10D', 'score_20D', 'score_30D', 'score_60D']
                name = ans[1]
                last = ans[2]
                slope = ans[3]
                align_t = ans[4]
                align_y = ans[5]

                if last_signal != str(name) + '_' + str(last) + '_Y' + str(align_y) + '_T' + str(align_t) + '_' + str(slope):
                    last_signal = str(name) + '_' + str(last) + '_Y' + str(align_y) + '_T' + str(align_t) + '_' + str(slope)
                    path = folder + str(name) + '_' + str(last) + '_Y' + str(align_y) + '_T' + str(align_t) + '_' + str(slope)
                    print(path)
                    if os.path.isfile(path + '.csv'):
                        with open(path + '.csv', 'a', newline='') as csvfile:
                            writer = csv.writer(csvfile)
                            writer.writerow(ans[6:])
                    else:
                        with open(path + '.csv', 'a', newline='') as csvfile:
                            writer = csv.writer(csvfile)
                            writer.writerow(first_row)
                            writer.writerow(ans[6:])

toc = time.perf_counter()
print(f"Downloaded the tutorial in {(toc - tic) / 60:0.4f} mins")

win32api.MessageBox(0, 'Finished', 'Reminder', 0x00001000)
