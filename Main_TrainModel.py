# This Script is written for training the machine learning model

#%% Init
import _LocalVariable

import pandas as pd

#%% Import data

# import binomial brexit or not data
BINOM_DATA_NEW_PATH = _LocalVariable._DATA_INPUT_DIRECTORY + r"\BinomialBrexit.tsv"

binom_data_new = pd.read_csv(BINOM_DATA_NEW_PATH, sep = "\t", engine='python')

#%% Preprocess data
from projectpackage.data_preprocessing import DataValidation

# Data cleansing
from projectpackage.data_preprocessing import DataCleansing


## change date format
for i in range(len(binom_data_new.index)):
    date = binom_data_new["Date"].iloc[i]
    date = str(date)
    
    ## check if it's already in stnadard format
    if DataValidation.check_standard_date_format(date):
        pass
    ## if not
    else:
        ## check if it's in the pre-defined nonstandard format
        if DataValidation.check_nonstandard_date_format(date):
            # change to standard format
            date = DataCleansing.get_standard_date(date)
        ## if not halt and handel error 
        else:
            raise ValueError('Date string is not stored'\
                             ' in standard format or pre-defined'\
                             ' non-standard format')
        
    
    binom_data_new["Date"].iloc[i] = date

 
# Data Transformation
from projectpackage.data_preprocessing import DataTransformation

#%% Validate data

#%% Merge data

#%% Run classification model on binom data


# Evaluate model

#%% Save trained models


