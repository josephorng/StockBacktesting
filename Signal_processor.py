import os.path
import time
import csv
import win32api
from ToolBox import text2list

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

first_line = ['name', 'total', 'last', 'align_y', 'align_t', 'slope',
              '5 score', '10 score', '20 score', '30 score', '60 score',
              '5 win rate', '10 win rate', '20 win rate', '30 win rate', '60 win rate',
              '5 HP', '10 HP', '20 HP', '30 HP', '60 HP',
              '5 LP', '10 LP', '20 LP', '30 LP', '60 LP']
total_list = []
for name in name_list:
    for align_y in align_list:
        for align_t in align_list:
            for last in last_list:
                for slope in slope_list:
                    path = folder + str(name) + '_' + str(last) + '_Y' + str(align_y) + '_T' + str(align_t) + '_' + str(slope)
                    if os.path.isfile(path + '.csv'):
                        # temp = []
                        print(path)
                        with open(path + '.csv') as csv_file:
                            rows = csv.reader(csv_file, delimiter=',')
                            temp = list(rows)
                        total = 0
                        sc5 = 0
                        sc10 = 0
                        sc20 = 0
                        sc30 = 0
                        sc60 = 0
                        wr5 = 0
                        wr10 = 0
                        wr20 = 0
                        wr30 = 0
                        wr60 = 0
                        HP5 = 0
                        HP10 = 0
                        HP20 = 0
                        HP30 = 0
                        HP60 = 0
                        LP5 = 0
                        LP10 = 0
                        LP20 = 0
                        LP30 = 0
                        LP60 = 0
                        for i in range(1, len(temp[:])):
                            if float(temp[i][-5]) > 0:
                                wr5 += 1
                            if float(temp[i][-4]) > 0:
                                wr10 += 1
                            if float(temp[i][-3]) > 0:
                                wr20 += 1
                            if float(temp[i][-2]) > 0:
                                wr30 += 1
                            if float(temp[i][-1]) > 0:
                                wr60 += 1
                            total = total + 1
                            sc5 = sc5 + float(temp[i][-5])
                            sc10 = sc10 + float(temp[i][-4])
                            sc20 = sc20 + float(temp[i][-3])
                            sc30 = sc30 + float(temp[i][-2])
                            sc60 = sc60 + float(temp[i][-1])
                            HP5 = HP5 + float(temp[i][-15])
                            HP10 = HP10 + float(temp[i][-14])
                            HP20 = HP20 + float(temp[i][-13])
                            HP30 = HP30 + float(temp[i][-12])
                            HP60 = HP60 + float(temp[i][-11])
                            LP5 = LP5 + float(temp[i][-10])
                            LP10 = LP10 + float(temp[i][-9])
                            LP20 = LP20 + float(temp[i][-8])
                            LP30 = LP30 + float(temp[i][-7])
                            LP60 = LP60 + float(temp[i][-6])
                        if total > 20:
                            line = [name, total, last, align_y.replace('↘', '>'), align_t.replace('↘', '>'),
                                    slope.replace('↗', '>0').replace('↘', '<0'),
                                    sc5/total, sc10/total, sc20/total, sc30/total, sc60/total,
                                    wr5/total, wr10/total, wr20/total, wr30/total, wr60/total,
                                    HP5/total, HP10/total, HP20/total, HP30/total, HP60/total,
                                    LP5/total, LP10/total, LP20/total, LP30/total, LP60/total]
                            total_list.append(line)
                            print(line)
i = 0
while os.path.isfile(folder + 'Total_list_' + str(i) + '.csv'):
    i = i + 1
with open(folder + 'Total_list_' + str(i) + '.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(first_line)
    writer.writerows(total_list)

toc = time.perf_counter()
print(f"Downloaded the tutorial in {(toc - tic) / 60:0.4f} mins")

win32api.MessageBox(0, 'Finished', 'Reminder', 0x00001000)
