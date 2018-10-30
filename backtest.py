#! /usr/bin/env python
# coding: utf-8

import os

import numpy as np
import scipy as sp
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.finance as mpf

from tqdm import trange
from sys import getsizeof

SDAY = 5
LDAY = 11
SIGDAY = 4

def load_data(dirpath):
    data = pd.DataFrame()
    for yyyy in trange(2016, 2019):
        for mm in range(1, 13):
            yyyymm = 100 * yyyy + mm
            if 201601 <= yyyymm < 201807:
                filedir = dirpath + str(yyyymm)
                filelist = os.listdir(filedir)
                filelist.sort()
                for filename in filelist:
                    tmp = pd.read_csv(filedir + '/' + filename, encoding='shift-jis')
                    data = pd.concat([data, tmp])
    return data
                    
def convert_to_5min(data):
    data.columns = ['datetime', 'bidopen', 'bidhigh', 'bidlow', 'bidclose', 'askopen', 'askhigh', 'asklow', 'askclose']
    data = data[::5]
    data.datetime = pd.to_datetime(data.datetime)
    data.index = data.datetime.tolist()
    del data['datetime']
    data["bidclose"] = data["bidopen"].shift(-1)
    data["askclose"] = data["askopen"].shift(-1)
    return data

def compute_indicators(data):
    data['sema'] = data.bidclose.ewm(alpha=2/(SDAY + 1)).mean()
    data['lema'] = data.bidclose.ewm(alpha=2/(LDAY + 1)).mean()
    data['macd'] = data.sema - data.lema
    data['signal'] = data.macd.rolling(SIGDAY).mean()

    data['indicator'] = np.sign(data.macd - data.signal)
    data['tradeflag'] = (data.indicator - data.indicator.shift(1))/2 # -1:BID, 1:ASK
    
    return data
    
def entry_and_set(data):
    entrydata = data[abs(data["tradeflag"]) == 1]

    entrydata["entryrate"] = entrydata[entrydata["tradeflag"] == -1]["bidopen"]
    entrydata["entryrate"] = entrydata["entryrate"].fillna(entrydata["askopen"])
    entrydata["setrate"] = entrydata["askopen"].where(entrydata["tradeflag"] == 1).shift(-1)
    entrydata["setrate"] = entrydata["setrate"].fillna(entrydata["bidopen"].shift(-1))

    entrydata["pips"] = (entrydata["setrate"] - entrydata["entryrate"]) * entrydata["tradeflag"]
    
    return entrydata

def main():
    data = load_data('./data/USDJPY_1601_1806/')
    data = convert_to_5min(data)
    data = compute_indicators(data)
    entrydata = entry_and_set(data)
    
    data["pips"] = entrydata["pips"] 
    print("SUM of pips:", data["pips"].sum())
    
    start = '20160101'
    end   = '20180701'
    data["pips"].cumsum().plot()
    plt.ylabel("pips")
    plt.xlabel("time")
    plt.show()
    
if __name__ == "__main__":
    main()
