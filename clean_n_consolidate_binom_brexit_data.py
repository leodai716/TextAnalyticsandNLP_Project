'''
This Script is written for training the machine learning model
for easy understanding of code logic, certain functions will be defined in other python scripts
@author: leod
'''
#%% Init
import os
import re
import fnmatch # match raw-data files
import pandas as pd
import _LocalVariable


#%% Locate Data and load existing database

# list desired files in data directory
files_in_data_dir = os.listdir(_LocalVariable._DATA_DIRECTORY)
FILE_PATTERN = "raw_data-BrexitorNot-*.tsv"
files_in_data_dir = [file for file in files_in_data_dir\
                if fnmatch.fnmatch(file, FILE_PATTERN)]

# load existing database
BINOM_DATA_BASE_PATH = _LocalVariable._DATA_DIRECTORY +\
                        "\\cleaned_db-BrexitorNot.pkl"
binom_data = pd.read_pickle(BINOM_DATA_BASE_PATH)

#%% Data Cleansing
# load functions for cleansing
from projectpackage.data_preprocessing import DataValidation
from projectpackage.data_preprocessing import DataCleansing

# define main function
def clean_data(binom_data_new):
    '''
    This function clean the data and transform to tidier dataframe
    * this is the main function of the script
    Input: raw data as data frame
    Output: clean and tidy data frame
    '''

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
                                 ' non-standard format ' + str(i))

        binom_data_new.loc[i, "Date"] = date

    ## change date from string to datetime
    binom_data_new["Date"] = pd.to_datetime(binom_data_new["Date"])


    # combine all text to form new column
    ## create new list
    binom_data_new['combined_text'] = None

    for i in range(len(binom_data_new.index)):
        ## combine text
        title = binom_data_new.iloc[i]["title"]
        text = binom_data_new.iloc[i]['text']
        combined_text = " ".join([title, text])

        binom_data_new.loc[i, "combined_text"] = combined_text

    # remove non characters from
    binom_data_new["combined_text"] = binom_data_new["combined_text"].apply(\
                          lambda x: re.sub("[^a-zA-Z]+", " ", x))


    # filter out unwanted columns
    binom_data_new = binom_data_new[["Date", "combined_text", "brexit"]]


    return binom_data_new



#%% Data Cleaning
for file in files_in_data_dir:
    '''
    This loops through every raw tsv in the data directory
    and apply the cleaning function
    Raw data file will be moved to a 'processed' folder
    Database will be expanded with every new raw data added
    '''

    # open tsv as df
    file_path = _LocalVariable._DATA_DIRECTORY + "\\" + file
    binom_data_new = pd.read_csv(file_path,\
                                 sep="\t", engine='python')


    # clean raw data
    binom_data_new = clean_data(binom_data_new)


    # merge existing db with new data
    binom_data = pd.concat([binom_data, binom_data_new], ignore_index=True)
    binom_data = binom_data[["Date", "combined_text", "brexit"]]


    # move cleaned raw-data
    new_file_path = _LocalVariable._DATA_DIRECTORY + "\\processed\\" + file
    os.rename(file_path, new_file_path)

#%% Save cleaned file

os.chdir(_LocalVariable._DATA_DIRECTORY)
CLEANED_FILE = "cleaned_db-BrexitorNot.pkl"
binom_data.to_pickle("./" + CLEANED_FILE)
