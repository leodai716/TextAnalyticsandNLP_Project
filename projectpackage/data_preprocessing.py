# -*- coding: utf-8 -*-
'''
'''
__all__ = ['DataCleansing', 'DataTransformation', 'DataReduction',]
#%% Init 
import sys

sys.path.append("..")
#%% Setup
import _LocalVariable
import re

#%% Data processing functions
MONTH_DICT = {"jan":"01", "feb":"02", "mar":"03",
							  "apr":"04", "may":"05", "jun":"06",
							  "jul":"07", "aug":"08", "sep": "09",
							  "oct":"10", "nov":"11", "dec":"12"
							 }


class DataCleansing():
	'''
	This functions contains Data Processing functions
	'''
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


class DataTransformation():

	def get_word_index_map():
		pass


	def get_term_vector():
		pass



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
    
    

	
