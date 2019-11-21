# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 03:14:17 2019

@author: LeoDai
"""

import pandas as pd
import random

class DataStorage():


    def convert_df_to_tsv(df,file_name):
        header = random_data.columns
		header = "\t".join(header) + "\n"

		file = open(file_name), "w")
		file.write(header)
		file.close
        
        for i in range(len(random_data.index)):
    		row_list = list(random_data.iloc[i])
    		text = "\t".join(row_list) + "\n"
    		file = open(file_name, "a")
    		file.write(text)
    		file.close()