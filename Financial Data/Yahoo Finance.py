# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10 14:12:48 2019

@author: Darius Choi
"""

import yfinance as yf #Require the installation of yfinance package (pip install yfinance --upgrade --no-cache-dir)
import datetime
import pandas as pd

tickers = ["^FTSE"] #Can choose a list of tickers
start = datetime.datetime(2018,12,31) 
end = datetime.datetime(2019,10,15)
data = yf.download(tickers, start=start, end=end)

pd.set_option('display.float_format', lambda x: '%.4f' % x) #Convert scientific numbers into floating numbers
data = data[["Adj Close", "Volume"]] #Identify the columns we need. Adjusted Close and Volumne in this case
tsvfile = data.to_csv(r"C:\Documents\HKU\Courses\FINA 4350 Text Analytics and NPL\Project\Python related\fina_data-ftse1001.csv", sep="\t")

#%%

import yfinance as yf 
import datetime
import pandas as pd

tickers = ["^FTSE"]
start = datetime.datetime(2018,12,31) 
end = datetime.datetime(2019,10,15)
data = yf.download(tickers, start=start, end=end)
pd.set_option('display.float_format', lambda x: '%.4f' % x)
data = data[["Adj Close", "Volume"]] 



