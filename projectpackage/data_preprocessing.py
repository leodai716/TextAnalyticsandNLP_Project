# -*- coding: utf-8 -*-
'''
'''
__all__ = ['DataCleansing', 'TextProcessing', 'DataTransformation', 'DataReduction',]
#%% Init 
import sys

sys.path.append("..")
#%% Setup
import _LocalVariable
import re
import numpy as np
import pandas as pd

#%% Data cleansing functions
MONTH_DICT = {"jan":"01", "feb":"02", "mar":"03",
                              "apr":"04", "may":"05", "jun":"06",
                              "jul":"07", "aug":"08", "sep": "09",
                              "oct":"10", "nov":"11", "dec":"12"
                             }

    

class DataCleansing():
    '''
    This functions contains Data Processing functions
    '''
    
    
    # clean date
    def get_standard_date(nonstandard_date, year = "2019"):
        # ensure year in str
        year = str(year)
        
        # get month str
        month_string = nonstandard_date[0:3]
        month_string = month_string.lower()
        month = MONTH_DICT[month_string]
        
        # get date str
        date = nonstandard_date[3:]
        date = int(date)
        date = "%02d" % date
        date = str(date)
        
        # join year, month, & date
        standard_date = "-".join([year, month, date])
        
        return standard_date
    
    
    # clean text
    def get_tidy_text(text_string):
        '''
        need improvements
        '''
        text_string = text_string.lower()
        text_string = re.sub("[^a-zA-Z]", " ", text_string)
        return text_string


#%% Text Processing
SPECIAL_WORD_DICT = {"theresa may" : "theresamay", #1st Brexit Prime Minister
                     "boris johnson" : "borisjohnson", #2nd Brexit Prime Minister
                     "jeremy hunt" : "jeremyhung", #opponent of Boris Johnson for the Presidency
                     "oliver robbins" : "oliverrobbins", #Europe adivosr to the Prime Minister
                    "david davis" : "daviddavis", #1st Brexit Secretary
                    "dominic raab" : "dominicraab", #2nd Brexit Secretary
                    "stephen barclay" : "stephen barclay", #3rd Brexit Secretary
                    "jacob rees-mogg" : "jacobreesmogg", #contributed to the defeat of May's deal
                    "jeremy corbyn" : "jeremycorbyn", #leader of the biggest opposition of Brexit
                    "yvette cooper" : "yvttecooper", #leader of the biggest opposition of Brexit
                    "michel barnier" : "michelbarnier", #chief neogtiator of European Commission
                    "jean-claude junker" : "jeanclaudejuncker", #president of the European Commission
                    "donald tusk" : "donaldtsuk", #president of the European Council
                    "guy verhofstadt" : "guyverhofstadt", # Brexit coordinator from the European Parlilament
                    "article 50" : "article50", #the treaty to exit Europe
                    "blind brexit" : "blindbrexit", #scenario where the UK leaves the EU without clarity on the terms for future trade deals. Unlike hard brexit, it involves vague commitments
                    "blindfold brexit" : "blindbrexit", #same as blind brexit
                    "no deal" : "nodeal",
                    "clean break brexit" : "hardbrexit", #hard brexit
                    "no-deal brexit" : "hardbrexit", #hard brexit
                    "no deal brexit" : "hardbrexit", #hard brexit
                    "hard brexit" : "hardbrexit", #hard brexit
                    "soft brexit" : "softbrexit", #soft brexit
                    "slow brexit" : "slowbrexit", #the brexit process may be extended and it implies a longer period of political uncertainty
                    "customs union" : "customsunion", #not imposing tariff on member countries and imposing the same tariff to non-member countries
                    "divorce bill" : "divorcebill", #concerning the payment made by the UK to the EU for Brexit
                    "exit bill" : "divorcebill", #same as divorce bill
                    "hard border" : "hardborder", #concerning the border between the UK and the Northern Ireland
                    "second referendum" : "secondreferendum", #second referendum for Brexit
                    "norway model" : "norwaymodel", #the UK replicates the model of Norway
                    "norway plus" : "norwayplus", #the UK replicates thh model of Norway with some changes
                    "canada model" : " canadamodel", #the UK replciates the model of Canada
                    "canada plus" : "canadaplus", #the UK replicates the of Canada with some changes
                }

class TextProcessing():

    
    def combine_specialwords(text_string):
        text_string = text_string
        for key,value in SPECIAL_WORD_DICT.items():
            text_string = re.sub(key, value, text_string)
        
        return text_string
#%%  Data Transformation

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

wnl = WordNetLemmatizer()


class DataTransformation():


    def get_tokens(text_string):
        text_string = text_string
        # tokenise words
        tokens = word_tokenize(text_string)
        # remove words that are too short
        tokens = [token for token in tokens if len(token) > 2]
        #remove stopword
        tokens = [token for token in tokens if tokens not in stopwords.words('english')]
        # lemmatize words
        tokens = [wnl.lemmatize(token) for token in tokens]
        
        tokens = np.array(tokens)
    
        return tokens


    def get_word_index_map(array):
        '''
        pass in a 2D array
        '''
        word_index_map = {}
        index_count = 0
        for item in array:
            for token in item:
                if token not in word_index_map:
                    word_index_map[token] = index_count
                    index_count += 1
        return word_index_map


    def get_bow_vector(tokens, word_index_map):
        v = np.zeros(len(word_index_map))
        for token in tokens:
            if token in word_index_map:
                i = word_index_map[token]
                v[i] += 1
        v = v/v.sum()
        v = np.array(v)
        return v


    def get_DTM(dataframe, word_index_map):
        # create Document Term Matrix
        DTM = pd.DataFrame(columns=np.arange(len(word_index_map)+1))

        for i in range(len(dataframe.index)):
            vector = dataframe['bow_vector'].iloc[i]
            brexit = dataframe['brexit'].iloc[i]
            vector = np.append(vector, brexit)
            vector_df = pd.DataFrame(vector)
            vector_df = vector_df.T
            DTM = DTM.append(vector_df)
 
        return DTM


    def get_DTM_predict(dataframe, word_index_map):
        # create Document Term Matrix
        DTM = pd.DataFrame(columns=np.arange(len(word_index_map)))

        for i in range(len(dataframe.index)):
            vector = dataframe['bow_vector'].iloc[i]
            vector_df = pd.DataFrame(vector)
            vector_df = vector_df.T
            DTM = DTM.append(vector_df)
 
        return DTM




class DataReduction():
    
    def LSA():
        pass



class DataValidation():
    
    
    def check_standard_date_format(date_string):
        '''
        Check whether date is in "yyyy-mm-dd" format
        input: date string 
        return: bollean value
        '''
        if len(date_string) > 10:
            return False
            exit
        
        STANDARD_DATE_PATTERN = "[0-9]{4}[-]{1}[0-9]{2}[-]{1}[0-9]{2}"
        if re.match(STANDARD_DATE_PATTERN, date_string):
            return True
        else:
            return False
    
    
    def check_nonstandard_date_format(date_string):
        '''
        Check whether date is in "MMMdd" format
        input: date string
        return: bollean value
        '''
        month_string = date_string[0:3]
        date_string = date_string[3:]
        
        if len(date_string) > 2:
            return False
            exit
        
        if re.fullmatch("[a-zA-Z]+", month_string) and\
        re.fullmatch("[0-9]+", date_string):
            return True
        else:
            return False
    
    

    
