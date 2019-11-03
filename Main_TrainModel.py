# This Script is written for training the machine learning model

#%% Init
import _LocalVariable

import pandas as pd

#%% Import data

# import binomial brexit or not data
BINOM_DATA_PATH = _LocalVariable._DATA_INPUT_DIRECTORY + r"\BinomialBrexit.tsv"

binom_data = pd.read_csv(BINOM_DATA_PATH, sep = "\t")

#%% Clean data 



#%% Validate data



#%% Run classification model on binom data


# Evaluate model

#%% Save trained models


