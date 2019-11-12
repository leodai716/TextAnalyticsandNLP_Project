# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 13:21:54 2019

@author: LeoDai
"""

#%% Init
import pandas as pd
import numpy as np
import pickle
import os
import sys
import _LocalVariable
import multiprocessing
from projectpackage.data_preprocessing import TextProcessing
from projectpackage.data_preprocessing import DataTransformation
import time


sys.path.append(".")
cores_allocated = int(multiprocessing.cpu_count()/2)
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

#%% functions

def text_processing(df):
    df['combined_text'] = df['title'] + " " + df['text']
    df['combined_text'] = df['combined_text'].apply(lambda x: x.lower())
    df['combined_text'] = df['combined_text'].apply(TextProcessing.combine_specialwords)
    
    return df

def tokenization(df):
    df['tokens'] = df['combined_text'].apply(DataTransformation.get_tokens)
    return df

def data_transformation(df):
    print('Hello World')
    df['bow_vector'] = df['tokens'].apply(\
        lambda x: DataTransformation.get_bow_vector(x, word_index_map))
    print('Nice World')
    DTM = DataTransformation.get_DTM_predict(df, word_index_map)
    
    return DTM
#%% main
if __name__ == '__main__':
    start_time = start_time
    data = data
#    global chunks
    chunks = np.array_split(data, cores_allocated)
    
    with multiprocessing.Pool(processes=cores_allocated) as pool:
        data = pd.concat(pool.map(text_processing, chunks))
    print("--- %s seconds ---" % (time.time() - start_time))
    
    chunks = np.array_split(data, cores_allocated)

    with multiprocessing.Pool(processes=cores_allocated) as pool:
        data = pd.concat(pool.map(tokenization, chunks))
        
    print("--- %s seconds ---" % (time.time() - start_time))
    
    chunks = np.array_split(data, cores_allocated)
    with multiprocessing.Pool(processes=cores_allocated) as pool:
        DTM = pd.concat(pool.map(data_transformation, chunks))
    print("--- %s seconds ---" % (time.time() - start_time))
    
    #%% Prediction 
    prediction = model_ab.predict(DTM)
    prediction = pd.DataFrame(prediction)
    prediction.columns = ['brexit']
    
    data_predicted = pd.concat([data.reset_index(drop=True), prediction], axis=1)
    
    print("--- %s seconds ---" % (time.time() - start_time))
        
    #%% save the prediction result
    os.chdir(_LocalVariable._DATA_DIRECTORY)
    FILENAME = "prediction_result-gardian.pkl"
    pd.to_pickle(data_predicted, FILENAME)
    
print("--- %s seconds ---" % (time.time() - start_time))
