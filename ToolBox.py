import csv


def text2list(name):
    stock_file = open(name, "r")
    stock_list = stock_file.read().splitlines()
    print(stock_list)
    stock_file.close()
    return stock_list


def write2text(name, list):
    fp = open(name, "a")
    fp.truncate(0)
    for element in list:
        fp.write(element + "\n")


def write2csv(path, list_, col_num):
    # 開啟輸出的 CSV 檔案
    with open(path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        print(len(list_) / col_num)
        for i in range(int(len(list_) / col_num)):
            writer.writerow(list_[i * col_num:i * col_num + col_num])


#def csv2list(name, list, col_num):

def filter_q(list, driver):
    i = -1
    record = []
    new_list = []
    for num in list:
        i = i+1
        driver.get("https://invest.cnyes.com/twstock/TWS/" + num)
        Q = driver.find_element_by_xpath("//*[@id='_profile-TWS:" + num + ":STOCK']/div[2]/div[2]/div[1]/div[2]").text
        print(Q)
        if Q.find('K') != -1:
            temp = float(Q.replace("K", ""))
            print(temp)
            if temp > 2:
                record.append(i)
    for j in record:
        new_list.append(list[j])
    return new_list