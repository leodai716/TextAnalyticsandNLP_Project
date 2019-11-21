# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 21:21:26 2019

@author: LeoDai
"""

#%% Init
import pandas as pd
from plotnine import *
from plotnine.data import mpg
import _LocalVariable

#%% Load data
FILE_PATH = _LocalVariable._DATA_DIRECTORY + "\\prediction_result-gardian.pkl"
data = pd.read_pickle(FILE_PATH)

#%% creat day count matrix
# create empty dataframe with dates
from projectpackage.data_preprocessing import DataCleansing
data['Date'] = data['Date'].apply(DataCleansing.get_standard_date)
data['Date'] = pd.to_datetime(data['Date'])
start_date = data['Date'].iloc[0]
end_date = data['Date'].iloc[-1]

date_range = pd.date_range(start_date, end_date).tolist()

brexit_related_day_count = pd.DataFrame(index=range(len(date_range)))
brexit_related_day_count['date'] = date_range

brexit_related_day_count['count'] = 0

for i in range(len(data.index)):
    date = data['Date'][i]
    brexit = data['brexit'][i]
    if brexit == 1:
        brexit_related_day_count.loc[brexit_related_day_count['date'] == date\
                                     ,'count'] += 1




plot = (ggplot(brexit_related_day_count)
        + aes(x='date', y='count')
        + geom_line()
        )

print(plot)
