# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 03:22:17 2019

@author: LeoDai
"""

#%% Init
import pandas as pd
import pickle
import os
import sys
import _LocalVariable

sys.path.append(".")
start_time = time.time()
#%% Load data and trained model
DATA_PATH = _LocalVariable._DATA_DIRECTORY + "\\raw_data-opinion-gardian.tsv"
data = pd.read_csv(DATA_PATH, sep='\t', engine='python')

os.chdir(_LocalVariable._OBJECT_DIRECTORY)

file_list = os.listdir()
for item in file_list:
    object_name = item[:-4]
    f = open(item, 'rb')
    vars()[object_name] = pickle.load(f)

os.chdir(_LocalVariable._WORKING_DIRECTORY)
#%% Data Transformation
from projectpackage.data_preprocessing import TextProcessing

data['combined_text'] = data['title'] + " " + data['text']
data['combined_text'] = data['combined_text'].apply(lambda x: x.lower())
data['combined_text'] = data['combined_text'].apply(TextProcessing.combine_specialwords)

#%% Tokenization
from projectpackage.data_preprocessing import DataTransformation

data['tokens'] = data['combined_text'].apply(DataTransformation.get_tokens)
#%% Data transformation (text to numbers)
from projectpackage.data_preprocessing import DataTransformation

data['bow_vector'] = data['tokens'].apply(\
    lambda x: DataTransformation.get_bow_vector(x, word_index_map))

DTM = DataTransformation.get_DTM_predict(data, word_index_map)

#%% Prediction 
prediction = model_ab.predict(DTM)
prediction = pd.DataFrame(prediction)
prediction.columns = ['brexit']

data_predicted = pd.concat([data.reset_index(drop=True), prediction], axis=1)

#%% save the prediction result
os.chdir(_LocalVariable._DATA_DIRECTORY)
FILENAME = "prediction_result-gardian.pkl"
pd.to_pickle(data_predicted, FILENAME)

print("--- %s seconds ---" % (time.time() - start_time))