# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 01:30:58 2019

@author: marzl
"""
import os
import sys
import datetime
import numpy as np
import pandas as pd
import pickle
import matplotlib.pyplot as plt

sys.path.append(os.getcwd())
import _LocalVariable

# input data directories
os.chdir(_LocalVariable._DATA_DIRECTORY)
PKL_DIR = r"processed_data.pkl"
ERI_DIR = r"fian-data_exchange_rate.csv"
FTSE_DIR = "fina_data-ftse100.csv"


# open .pkl, containing sentimental data

with open(PKL_DIR, "rb") as f:
    df = pickle.load(f)

# parameters for the bollinger bands
N = 20  # number of days in calculating moving average & SD
K = 1   # width of the bands

# construct b-bands of the sentimental score
df["20_day_ma"] = df["sentiment"].rolling(window=N).mean()
df["20_day_sd"] = df["sentiment"].rolling(window=N).std()
df["upper_band"] = df["20_day_ma"] + df["20_day_sd"] * K
df["lower_band"] = df["20_day_ma"] - df["20_day_sd"] * K

# intrepret any breaching of the b-bands as a buy/sell signal:
# signal = 1 => buy; signal < 1 => sell
df["buy_signal"] = np.where(df["sentiment"] > df["upper_band"], -1, 0)
df["sell_signal"] = np.where(df["sentiment"] < df["lower_band"], 1, 0)
df["signal"] = df["buy_signal"] + df["sell_signal"]

# read effective exchange rate index from .csv input
eri = pd.read_csv(ERI_DIR)
# Change to datetime dtype
eri.loc[:,"Date"] = pd.to_datetime(eri.loc[:,"Date"])

template_df = df
# merging the 2 dataframes
df = template_df.merge(eri, how="left")
# first forward fill the NaN (as there are time gaps in financial data),
# then drop all the remaining rows with NaN (the first 19 days where constructing the b-bands is impossible)
df = df.ffill().dropna()

# cash flow by day
df["cash_flow"] = - df["signal"] * df["ERI_sterling"]
# cash balance = the cumulative sum of daily CFs, assuming cash balance on day 1 = 0
df["cash_balance"] = df["cash_flow"].cumsum()
# treating each transaction as trading "one unit" of commodity
df["pound_inventory"] = df["signal"].cumsum()
# value of the pound inventory
df["pound_balance"] = df["pound_inventory"] * df["ERI_sterling"]
# wealth = cash_balance + pound_balance
df["wealth"] = df["cash_balance"] + df["pound_balance"]

# data visualization
# plotting the b-bands
df.plot(y = ["sentiment", "20_day_ma", "upper_band", "lower_band"],
        x = "Date",
        figsize=(12,6), 
        title = "Sentimental Bollinger Bands")
plt.show()

#plotting the wealth over time
df.plot(y = "wealth",
        x = "Date",
        figsize=(12,6), 
        title = "Wealth over time")
plt.show()



#%% FTSE
ftse = pd.read_csv(FTSE_DIR)
ftse.loc[:,'Date'] = ftse.loc[:,'Date'].apply(datetime.datetime.fromisoformat)
df2 = template_df.merge(ftse, how="left")
df2 = df2.ffill().dropna()
# cash flow by day
df2["cash_flow"] = - df2["signal"] * df2["Adj Close"]
# cash balance = the cumulative sum of daily CFs, assuming cash balance on day 1 = 0
df2["cash_balance"] = df2["cash_flow"].cumsum()
# treating each transaction as trading "one unit" of commodity
df2["pound_inventory"] = df2["signal"].cumsum()
# value of the pound inventory
df2["pound_balance"] = df2["pound_inventory"] * df2["Adj Close"]
# wealth = cash_balance + pound_balance
df2["wealth"] = df2["cash_balance"] + df2["pound_balance"]

# data visualization
# plotting the b-bands
df2.plot(y = ["sentiment", "20_day_ma", "upper_band", "lower_band"],
        x = "Date",
        figsize=(12,6), 
        title = "Sentimental Bollinger Bands")
plt.show()

#plotting the wealth over time
df2.plot(y = "wealth",
        x = "Date",
        figsize=(12,6), 
        title = "Wealth over time")
plt.show()
