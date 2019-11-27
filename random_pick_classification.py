"""
This is scripted for randomly picking 60 brexit related observations
and asking users to classify whether they are
1. No Deal Brexit
2. Soft Brexit
3. Revoke Brexit
4. Unable to be classified

@author: LeoDai
"""
#%% Init
import os
import sys
import random
import pandas as pd
import numpy as np

SCRIPT_DIRECTORY = os.getcwd()
sys.path.append(SCRIPT_DIRECTORY)
import _LocalVariable


#%% User Inputs
DATA_DIRECTORY = _LocalVariable._DATA_DIRECTORY
#%% Load Data
DATA_PATH = DATA_DIRECTORY + "\\prediction_result-combined.pkl"
data = pd.read_pickle(DATA_PATH)

brexit_data = data.loc[data['brexit'] == 1, :].copy()
brexit_data = brexit_data.reset_index(drop=True)
#%% Choosing data set to work with

NEWS_PAPER_DICT = {0:'guardian', 1:'independent', 2:'telegraph', 3:'express', 4:'financial times'}
DISPLAY_TEXT_1 = "Please input the news paper you want to work with: \n\
0:'guardian', 1:'independent', 2:'telegraph', 3:'express', 4:'financial times'\n"
news_paper_no = input(DISPLAY_TEXT_1)
news_paper_no = int(news_paper_no)


news_paper_choosed = NEWS_PAPER_DICT[news_paper_no]
news_paper_data = brexit_data.loc[brexit_data['news_paper'] == news_paper_choosed, :]
news_paper_data = news_paper_data.reset_index(drop=True)

#%% Randomly pick 60 observations and ask for user input

# generate observations for input
total_number_of_observation = len(news_paper_data.index)
pick_number = min([60, total_number_of_observation])

random_pick_list = random.sample(range(total_number_of_observation), pick_number)

random_pick_data = news_paper_data.loc[random_pick_list,:].copy()
random_pick_data = random_pick_data.reset_index(drop=True)


# ask for inputs
random_pick_data['brexit_classification'] = np.nan

DISPLAY_TEXT_2 =\
'''
Please classify the following to
1. No Deal Brexi
2. Soft Brexit
3. Revoke Brexit or General Election
4. Unable to be classified \n
Please input the numerical value
There will be 60 items in total
Thank you \n
'''
print(DISPLAY_TEXT_2)

NON_ERROR_LIST = ['1', '2', '3', '4']

for i in range(len(random_pick_data.index)):
    text = str(i) + ". " + random_pick_data.loc[i,'combined_text']
    print(text + "\n")
    while True:
        brexit_classification = input()
        if brexit_classification in NON_ERROR_LIST:
            break
        else:
            print('Wrong input, please type 1, 2, 3, or 4')
    random_pick_data.loc[i,'brexit_classification'] = brexit_classification



#%% Saving files
news_paper_choosed = news_paper_choosed.replace(' ', '_')
file_name = 'classification_data-' + news_paper_choosed + '.pkl'
file_path = DATA_DIRECTORY + "\\" + file_name
pd.to_pickle(random_pick_data, file_path)

#%% Coda
DISPLAY_TEXT_3 =\
'''
Thank you, 
please go to your data directory 
find the .pkl file 
and send it to Leo.
Shall Glory Be To Hong Kong
'''
print(DISPLAY_TEXT_3)
