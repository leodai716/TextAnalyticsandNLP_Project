# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 01:30:58 2019

@author: marzl
"""
import numpy as np
import pandas as pd
import pickle
import matplotlib.pyplot as plt

# input data directories
PKL_DIR = r"processed_data.pkl"
ERI_DIR = r"ERI_16-19.csv"

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
df["buy_signal"] = np.where(df["sentiment"] > df["upper_band"], 1, 0)
df["sell_signal"] = np.where(df["sentiment"] < df["lower_band"], -1, 0)
df["signal"] = df["buy_signal"] + df["sell_signal"]

# read effective exchange rate index from .csv input
eri = pd.read_csv(ERI_DIR)
# Change to datetime dtype
eri.loc[:,"Date"] = pd.to_datetime(eri.loc[:,"Date"])

# merging the 2 dataframes
df = df.merge(eri, how="left")
# first forward fill the NaN (as there are time gaps in financial data),
# then drop all the remaining rows with NaN (the first 19 days where constructing the b-bands is impossible)
df = df.ffill().dropna()

# trade volumn by day
df["trade"] = df["signal"] * df["ERI_sterling"]
# wealth = the cumulative sum of daily trade volumns, assuming wealth on day 1 = 0
df["wealth"] = df["trade"].cumsum()

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
