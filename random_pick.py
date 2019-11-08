# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 01:31:41 2019

@author: LeoDai
"""
#%% Init
import random
import _LocalVariable
import pandas as pd
import os

#%% Load data
DATA_PATH = _LocalVariable._DATA_DIRECTORY + "\\raw_data-opinion-gardian.tsv"
data = pd.read_csv(DATA_PATH, sep="\t", engine="python")


#%% Pick random data
NUM_LIST = range(len(data.index))
random_list = random.sample(NUM_LIST, 60)

random_data = data.iloc[random_list, :]

random_data['brexit'] = None

for i in range(len(random_data.index)):
    text = random_data['text'].iloc[i]
    print(text)
    while True:
        brexit_binom = input()
        if brexit_binom == "1" or brexit_binom == "0":
            break
    random_data['brexit'].iloc[i] = brexit_binom

    if i % 10 == 0:
        print("you are doing well, keep it up :)")

print(random_data['brexit'])
input()
#%% Save data frame
    
os.chdir(_LocalVariable._DATA_DIRECTORY)

FILENAME = "raw_data-BrexitorNot-gardian.tsv"

header = random_data.columns
header = "\t".join(header) + "\n"

file = open(FILENAME, "w")
file.write(header)
file.close

for i in range(len(random_data.index)):
    row_list = list(random_data.iloc[i])
    text = "\t".join(row_list) + "\n"
    file = open(FILENAME, "a")
    file.write(text)
    file.close()