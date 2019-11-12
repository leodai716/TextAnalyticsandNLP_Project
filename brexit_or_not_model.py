# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 14:18:03 2019

@author: LeoDai
"""

'''
This is for building a model that predict whether anarticle is Brexit related
or not.
@author: leodai
'''
#%% Init
import sys
import os
import pandas as pd
import numpy as np
import _LocalVariable
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB # naive base model
from sklearn.ensemble import AdaBoostClassifier # ada boost model
import pickle


sys.path.append(".")

#%% Loading the data
DATA_PATH = _LocalVariable._DATA_DIRECTORY + "\cleaned_db-BrexitorNot.pkl"
data = pd.read_pickle(DATA_PATH)

#%% Data Transformation
from projectpackage.data_preprocessing import TextProcessing

data['combined_text'] = data['combined_text'].apply(lambda x: x.lower())
data['combined_text'] = data['combined_text'].apply(TextProcessing.combine_specialwords)

#%% Tokenization
from projectpackage.data_preprocessing import DataTransformation

data['tokens'] = None

data['tokens'] = data['combined_text'].apply(DataTransformation.get_tokens)
    
#%% Data transformation (text to numbers)
from projectpackage.data_preprocessing import DataTransformation

# generate word index map
word_index_map = DataTransformation.get_word_index_map(data['tokens'])

data['bow_vector'] = None

data['bow_vector'] = data['tokens'].apply(\
    lambda x: DataTransformation.get_bow_vector(x, word_index_map))

DTM = DataTransformation.get_DTM(data, word_index_map)

#%% Data Processing
T_DTM = DTM[DTM.iloc[:,-1]==1]
F_DTM = DTM[DTM.iloc[:,-1]==0]
random_list = random.sample(range(len(F_DTM)),len(T_DTM))
F_DTM = DTM.iloc[random_list,:]
DTM_mod = T_DTM.append(F_DTM)

x_ori = DTM.iloc[:,:-1]
y_ori = DTM.iloc[:,-1]

x = DTM_mod.iloc[:,:-1]
y = DTM_mod.iloc[:,-1]

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3)


model_nb = MultinomialNB()
model_nb.fit(x_train, y_train)
print("naive base model score (train) :" + str(model_nb.score(x_train, y_train)))
print("naive base model score (test) :" + str(model_nb.score(x_test, y_test)))

model_ab = AdaBoostClassifier()
model_ab.fit(x_train, y_train)
print("ada boost model score (train): " + str(model_ab.score(x_train, y_train)))
print("ada boost model score (test): " + str(model_ab.score(x_test, y_test)))
print("ada boost model score (test): ",str(model_ab.score(x_ori, y_ori)) )

#%% Saving the results
os.chdir(_LocalVariable._WORKING_DIRECTORY)


def save_object(obj, name):
    with open('Object/' + name +'.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


save_object(word_index_map, 'word_index_map')

save_object(model_nb, "model_nb")
save_object(model_ab, "model_ab")