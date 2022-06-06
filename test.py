import shioaji as sj
import pandas as pd
import time
from datetime import datetime
import csv
import os.path


def quote_callback(topic: str, quote: dict):
    now_ = datetime.now()  # current date and time
    y = now_.strftime("%Y")
    m = now_.strftime("%m")
    d = now_.strftime("%d")
    file_date_ = y + '_' + m + '_' + d
    topic = topic.split('/')
    print(topic)
    print(quote)  # ['Close']
    global j
    with open('./' + file_date_ + '_' + str(i) + '.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([topic[3], quote['Close']])
        j = j + 1


# initiate
api = sj.Shioaji()
api.login(
    person_id='A129288927',
    passwd='NYC8213',
    contracts_cb=lambda security_type: print(f"{repr(security_type)} fetch done.")
)
ticks = api.ticks(api.Contracts.Stocks["2330"], "2021-08-02")
print(ticks.close[0])
df = pd.DataFrame({**ticks})
df.ts = pd.to_datetime(df.ts)
print(df)
'''
def quote_callback(topic: str, quote: dict):
    now_ = datetime.now()  # current date and time
    y = now_.strftime("%Y")
    m = now_.strftime("%m")
    d = now_.strftime("%d")
    file_date_ = y + '_' + m + '_' + d
    topic = topic.split('/')
    print(topic)
    print(quote)  # ['Close']
    global j
    with open('./' + file_date_ + '_' + str(i) + '.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([topic[3], quote['Close']])
        j = j + 1

    #print(f"Topic: {topic}, Quote: {quote}")


api.quote.subscribe(api.Contracts.Stocks['2330'], quote_type='tick')
j = 0
while j == 0:
    time.sleep(0.5)

contract_0050 = api.Contracts.Stocks["0050"]
print(contract_0050)'''

'''
kbars = api.kbars(contract_0050, start="2020-09-18", end="2020-09-18")
print(kbars[open])
kbars_df = pd.DataFrame({**kbars})
kbars_df.ts = pd.to_datetime(kbars_df.ts)
kbars_df.head()'''
