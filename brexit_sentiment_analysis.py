"""
This file is created for analysing the results generated by machine learning
model.
author: leodai
"""

#%% Init
import os
import sys 
import datetime
import pandas as pd
import numpy as np

from textblob import TextBlob

from plotnine import *
from plotnine.data import mpg

sys.path.append(os.getcwd())
import _LocalVariable
from projectpackage.data_preprocessing import DataValidation, DataCleansing
#%% Load Data
DB_PATH = _LocalVariable._DATA_DIRECTORY + "\\prediction_result-combined.pkl"

data = pd.read_pickle(DB_PATH)

#%% Data Preprocessing
def check_date(date):
    
    if DataValidation.check_standard_date_format(date):
        return True
    ## if not
    else:
        ## check if it's in the pre-defined nonstandard format
        if DataValidation.check_nonstandard_date_format(date):
            # change to standard format
            date = DataCleansing.get_standard_date(date)
            return True
        else:
            return False


dateformat_check = data['Date'].apply(check_date)
false_count = (dateformat_check == False).sum()

if false_count == 0:
    data.loc[:,'Date'] = data['Date'].apply(DataCleansing.get_standard_date)
    data.loc[:,'Date'] = pd.to_datetime(data['Date'])
#%% Analyse brexit mentions
END_DATE = datetime.datetime.fromisoformat('2019-10-15')

brexit_mention_df = data['Date'].value_counts()
brexit_mention_df = brexit_mention_df.reset_index()
brexit_mention_df.columns = ['Date', 'total_count']
brexit_mention_df = brexit_mention_df.sort_values(by=['Date'])
brexit_mention_df = brexit_mention_df.reset_index(drop=True)

DATE_FILTER = brexit_mention_df['Date'] <= END_DATE
brexit_mention_df = brexit_mention_df.loc[DATE_FILTER, :]

brexit_mention_df['brexit_count'] = 0


# count number of brexit related news
OBS_NO = len(data.index)

for i in range(OBS_NO):
    date = data.at[i,'Date']
    brexit = data.at[i,'brexit']
    index = brexit_mention_df.index[brexit_mention_df['Date'] == date]

    if brexit == 1:
        brexit_mention_df.loc[index,'brexit_count'] += 1




brexit_mention_df['brexit_proportion'] = brexit_mention_df['brexit_count']/\
                                         brexit_mention_df['total_count']



plot1 = (ggplot(brexit_mention_df)
        + aes(x='Date', y='brexit_proportion')
        + geom_line()
        )

#%% Analyse Sentiment
brexit_data = data[data['brexit'] == 1]
brexit_data = brexit_data.reset_index(drop=True)

brexit_data['polarity'] = None

BREXIT_DATA_NO = len(brexit_data.index)

for i in range(BREXIT_DATA_NO):
    text = brexit_data.at[i,'combined_text']

    s = TextBlob(text).sentiment
    brexit_data.at[i,'polarity'] = s.polarity

brexit_data.loc[:,'polarity'] = pd.to_numeric(brexit_data.loc[:,'polarity'])
print("mean:" + str(brexit_data.loc[:,'polarity'].mean()))
print("sd:" + str(brexit_data.loc[:,'polarity'].std()))


brexit_analysis_df = brexit_mention_df.copy()
brexit_analysis_df['sentiment'] = 0

for i in range(BREXIT_DATA_NO):
    date = brexit_data.at[i,'Date']
    polarity = brexit_data.at[i,'polarity']
    
    index = brexit_analysis_df.index[brexit_analysis_df['Date'] == date]
    brexit_analysis_df.loc[index, 'sentiment'] += polarity

brexit_analysis_df['sentiment'] = brexit_analysis_df['sentiment']/\
                                  brexit_analysis_df['brexit_count']
                                  


plot2 = (ggplot(brexit_analysis_df)
        + aes(x='Date')
        + geom_line(aes(y='sentiment'))
        )

print(plot1)
print(plot2)

os.chdir(_LocalVariable._DATA_DIRECTORY)

CSV_NAME = "processed_data.csv"
PKL_NAME = "processed_data.pkl"

#brexit_analysis_df.to_csv(CSV_NAME)
#brexit_analysis_df.to_pickle(PKL_NAME)
