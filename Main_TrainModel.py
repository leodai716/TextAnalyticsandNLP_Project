# This Script is written for training the machine learning model

#%% init
import _LocalVariable

import pandas as pd

#%% import data

# import binomial brexit or not data
BINOM_DATA_PATH = _LocalVariable._DATA_INPUT_DIRECTORY + r"\BinomialBrexit.tsv"

binom_data = pd.read_csv(BINOM_DATA_PATH, sep = "\t")

#%% process data 




#%% run classification model on binom data


# Model Score 

#%% save the trained model


