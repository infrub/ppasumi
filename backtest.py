#! /usr/bin/env python
# coding: utf-8

"""
compute sum of pips for dataset
dataset format: ./data/USDJPY_1601_1806/yyyymm/USDJPY_yyyymmdd.csv
entry as bid or ask only when macd < or > signal
set the entry when next entry
output the sum of pips and graph of pips cumulation
"""

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
    data_df = pd.DataFrame()
    for yyyy in trange(2016, 2019):
        for mm in range(1, 13):
            yyyymm = 100 * yyyy + mm
            if 201601 <= yyyymm < 201807:
                filedir = dirpath + str(yyyymm)
                filelist = os.listdir(filedir)
                filelist.sort()
                for filename in filelist:
                    tmp = pd.read_csv(filedir + "/" + filename, encoding="shift-jis")
                    data_df = pd.concat([data_df, tmp])
    return data_df
                    
def convert_to_5min(data_df):
    data_df.columns = ["datetime", "bidopen", "bidhigh", "bidlow", "bidclose", "askopen", "askhigh", "asklow", "askclose"]
    data_df = data_df[::5]
    data_df.datetime = pd.to_datetime(data_df.datetime)
    data_df.index = data_df.datetime.tolist()
    del data_df["datetime"]
    data_df["bidclose"] = data_df.bidopen.shift(-1)
    data_df["askclose"] = data_df.askopen.shift(-1)

    return data_df

def compute_indicators(data_df):
    data_df["sema"] = data_df.bidclose.ewm(alpha=2/(SDAY + 1)).mean()
    data_df["lema"] = data_df.bidclose.ewm(alpha=2/(LDAY + 1)).mean()
    data_df["macd"] = data_df.sema - data_df.lema
    data_df["signal"] = data_df.macd.rolling(SIGDAY).mean()

    data_df["indicator"] = np.sign(data_df.macd - data_df.signal)
    data_df["tradeflag"] = (data_df.indicator - data_df.indicator.shift(1))/2 # -1:BID, 1:ASK
    del data_df["sema"]
    del data_df["lema"]

    return data_df
    
def make_entry_and_set_df(data_df):
    entrydata = data_df[abs(data_df.tradeflag) == 1]

    entrydata["entryrate"] = entrydata[entrydata["tradeflag"] == -1]["bidclose"]
    entrydata["entryrate"] = entrydata["entryrate"].fillna(entrydata["askclose"])
    entrydata["setrate"] = entrydata["askclose"].where(entrydata["tradeflag"] == 1).shift(-1)
    entrydata["setrate"] = entrydata["setrate"].fillna(entrydata["bidclose"].shift(-1))

    entrydata["pips"] = (entrydata.setrate - entrydata.entryrate) * entrydata.tradeflag
    
    return entrydata

def main():
    rawdata_df = load_data("./data/USDJPY_1601_1806/")
    data_df = convert_to_5min(rawdata_df)
    data_df = compute_indicators(data_df)
    entrydata = make_entry_and_set_df(data_df)
    
    data_df["pips"] = entrydata["pips"]
    print("SUM of pips:", data_df["pips"].sum())
    
    start = "20160101"
    end   = "20180701"
    data_df["pips"].cumsum().plot()
    plt.ylabel("pips")
    plt.xlabel("time")
    plt.show()
    
if __name__ == "__main__":
    main()
