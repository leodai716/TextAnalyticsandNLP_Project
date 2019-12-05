# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 00:33:18 2019

@author: Mars Leung

Objective: to perform descriptive and cross-correlation analysis on statistics collected
"""
import os
import time
import numpy as np
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import _LocalVariable

os.chdir(_LocalVariable._DATA_DIRECTORY)
START_TIME = time.time()
PKL_DIR = r"processed_data.pkl"
ERI_DIR = r"fian-data_exchange_rate.csv"
FTSE_DIR = "fina_data-ftse100.csv"

def load_financial_data(data_dir):
    # To load data from .csv files, set Date column as index column, and forward-fill na entries
    loaded_df = pd.read_csv(data_dir)
    loaded_df.loc[:,"Date"] = pd.to_datetime(loaded_df.loc[:,"Date"])
    loaded_df.set_index("Date", inplace = True)
    loaded_df = loaded_df.resample("D").pad()
    return loaded_df

def normalized_cross_correlate(s1, s2):
    # I shamelessly copy from here: https://stackoverflow.com/questions/53436231/normalized-cross-correlation-in-python
    s1 = (s1 - np.mean(s1)) / (np.std(s1) * len(s1))
    s2 = (s2 - np.mean(s2)) / (np.std(s2))
    return np.correlate(s1, s2, 'full')

def plot_cross_correlation(cc_series, color = "b", scope = None):
    # scope is a tuple input that limits the x range shown in the plot
    # Default value of scope is none => show full range of x 
    max_lag_period = int((len(cc_series) - 1)/2)                                # maximum amount of days the sentiment can possibly lag
    period_array = list(range(-max_lag_period, max_lag_period + 1))             # x-axis of the plot
    
    plt.figure(figsize=(12,6))
    plt.plot(period_array, cc_series, color)
    
    plt.ylabel("Correlation coefficient") 
    plt.xlabel("Number of days the sentiment score lags the dependent variable")
    
    if scope is not None:    
        plt.xlim(scope)     # default show all x-range if the user does not input a scope
    
def get_max_correlation(cc_series):
    max_cc = max(cc_series, key = abs)                                          # find the absolute maximum correlation
    max_cc_index_list = [i for i, j in enumerate(cc_series) if j == max_cc]     # a list in case there are two absolute maxima
    max_lag_period = int((len(cc_series) - 1)/2)                                # maximum amount of days the sentiment can possibly lag
    max_cc_lag_period_list = [max_cc_index - max_lag_period for max_cc_index in max_cc_index_list]   # now in term of how many days the sentiment lags the market
    if len(max_cc_lag_period_list) > 1:
        return max_cc, max_cc_lag_period_list
    else:
        return max_cc, max_cc_lag_period_list[0]    # just simply return the number of day if the list only has one element
    
# Load sentimental data from PKL_DIR
with open(PKL_DIR, "rb") as f:
    df = pickle.load(f)
df.set_index("Date", inplace = True)

# Load Sterling ERI data from ERI_DIR, then merge that to df
eri_df = load_financial_data(ERI_DIR)
df = df.merge(eri_df, how = "left", left_index = True, right_index = True)

# Load FTSE 1000 Adjusted Close from FTSE_DIR, then merge that to df
ftse_df = load_financial_data(FTSE_DIR)
df = df.merge(ftse_df, how = "left", left_index = True, right_index = True)

# Forward-fill all the na entries
df = df.fillna(method = "ffill")

# Descriptive statistics
print("------------------------------Data description------------------------------")
df.plot(y = "sentiment",
        color = "r", 
        figsize=(12,6),
        title = "Sentiment Score over Time")
plt.show()

df.plot(y = "ERI_sterling",
        color = "b",
        figsize=(12,6),
        title = "Sterling Effective Exchange Rate Index over Time")
plt.show()

df.plot(y = "Adj Close",
        color = "g",
        figsize=(12,6),
        title = "FTSE1000 Adjusted Close over Time")
plt.show()
print("\nDescriptive statistics:\n")
print(df[["sentiment", "ERI_sterling", "Adj Close"]].describe())

# Cross-correlation analysis
print("\n--------Cross Correlation between sentiment score and Sterling ERI--------")

# Plotting sentiment vs ERI
df.plot(y = "sentiment",
        color = "r",
        figsize=(12,6),
        secondary_y = False,
        title = "Sentiment Score and Sterling Effective Exchange Rate Index over Time").set_ylabel('Sentimental Score')
df["ERI_sterling"].plot(color = "b", secondary_y = True).set_ylabel('Sterling Effective Exchange Rate Index')
plt.show()

# Cross Correlation: sentiment vs ERI
cc_eri = normalized_cross_correlate(df["sentiment"], df["ERI_sterling"])
plot_cross_correlation(cc_eri, color = "b")
plt.title("Normalized Cross Correlation between Sentimental Score and Sterling Effective Exchange Rate Index")
plt.show()

# Find the point where the correlation is the largest 
max_cc_eri, max_cc_eri_lag_period = get_max_correlation(cc_eri)
print("\nThe correlation coefficient is maximized absolutely at", round(max_cc_eri, 2),
      "when the sentiment score lags the Sterling Effective Exchange Rate Index by", 
      max_cc_eri_lag_period, "days.",
      "\n(When the number of days is negative, it means that the sentiment is instead leading.)")

print("\n---Cross Correlation between sentiment score and FTSE1000 Adjusted Close---")

# Plotting sentiment vs FTSE
df.plot(y = "sentiment",
        color = "r",
        figsize=(12,6),
        secondary_y = False,
        title = "Sentiment Score and FTSE1000 Adjusted Close over Time").set_ylabel('Sentimental Score')
df["Adj Close"].plot(color = "g", secondary_y = True).set_ylabel('FTSE1000 Adjusted Close')
plt.show()

# Cross Correlation: sentiment vs FTSE
cc_ftse = normalized_cross_correlate(df["sentiment"], df["Adj Close"])
plot_cross_correlation(cc_ftse, color = "g")
plt.title("Normalized Cross Correlation between Sentimental Score and FTSE1000 Adjusted Close")
plt.show()

# Find the point where the correlation is the largest 
max_cc_ftse, max_cc_ftse_lag_period = get_max_correlation(cc_ftse)
print("\nThe correlation coefficient is maximized absolutely at", round(max_cc_ftse, 2), 
      "when the sentiment score lags the Sterling Effective Exchange Rate Index by", 
      max_cc_ftse_lag_period, "days.",
      "\n(When the number of days is negative, it means that the sentiment is instead leading.)")

# Print time used
print("\n(Time used =", time.time() - START_TIME, "seconds.)")