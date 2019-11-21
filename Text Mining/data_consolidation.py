'''
This file is created for consolidating data and saving as tsv and pickle
for other stages of processing
'''
#%% Init
import os
import sys
import pandas as pd

MAIN_SCRIPT_PATH = os.getcwd()
sys.path.append(MAIN_SCRIPT_PATH)
sys.path.append("../")
import _LocalVariable

#%% Load Data
os.chdir(_LocalVariable._DATA_DIRECTORY)
#tsv
data_i_path = "raw_data-opinion-independent.tsv"
data_g_path = "raw_data-opinion-guadian.tsv"
data_f_path = "raw_data-opinion-financialtimes.tsv"

data_i = pd.read_csv(data_i_path, sep='\t')
data_i['news_paper'] = 'independent'
data_g = pd.read_csv(data_g_path, sep='\t', engine='python')
data_g['news_paper'] = 'guradian'
data_f = pd.read_csv(data_f_path, sep='\t', engine='python')
data_f['news_paper'] = 'financial times'

#pickel
data_t_path = "raw_data-opinion-telegraph.pkl"
data_e_path = "raw_data-opinion-express.pkl"

data_t = pd.read_pickle(data_t_path)
data_t['news_paper'] = 'telegraph'

data_e = pd.read_pickle(data_e_path)
data_e['news_paper'] = 'express'

data_list = [data_g, data_i, data_t, data_e, data_f]

#%% Merge

data = pd.concat(data_list)

drop_list = []
for i in range(len(data.index)):
    title_nan = pd.isnull(data.iat[i,1])
    text_nan = pd.isnull(data.iat[i,2])
    if title_nan or text_nan:
        drop_list.append(i)
        
os.chdir(_LocalVariable._DATA_DIRECTORY)
DATA_PATH = "raw_data-opinion-combined.pkl"
pd.to_pickle(data, DATA_PATH)
