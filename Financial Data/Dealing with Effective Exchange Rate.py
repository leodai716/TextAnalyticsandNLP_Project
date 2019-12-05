# -*- coding: utf-8 -*-
"""
Created on Thu Nov 28 22:33:31 2019

@author: Darius Choi
"""
#%%
import pickle
import pandas as pd
monthdictionary = {"Jan":"-01-", 
                   "Feb":"-02-", 
                   "Mar":"-03-", 
                   "Apr":"-04-", 
                   "May":"-05-", 
                   "Jun":"-06-", 
                   "Jul":"-07-", 
                   "Aug":"-08-", 
                   "Sep":"-09-", 
                   "Oct":"-10-",
                   "Nov":"-11-",
                   "Dec":"-12-"}
file = pd.read_csv(r"C:\Documents\HKU\Courses\FINA 4350 Text Analytics and NPL\Project\Sterling Effective Exchange Rate Bank of England  Database.csv")

#Formatting
file = file.rename(columns = {"Date":"Date", "Effective exchange rate index, Sterling (Jan 2005 = 100)                          XUDLBK67":"GBPEER"})
for row in range(len(file)):
    file.at[row,"Date"] = ("20" + file.at[row,"Date"][7:] + monthdictionary[file.at[row,"Date"][3:6]] + file.at[row,"Date"][0:2])

#Create 30-day SD
SD_30day = ["NA"]*29
for i in range(len(file)-30+1):
    SD = file.loc[0+i:29+i,"GBPEER"].std()
    SD_30day.append(SD)

#Create 90-day SD
SD_90day = ["NA"]*89
for i in range(len(file)-90+1):
    SD = file.loc[0+i:89+i,"GBPEER"].std()
    SD_90day.append(SD)

#Add columns to dataframe
file["GBPEER30-day SD"] = SD_30day
file["GBPEER90-day SD"] = SD_90day

#Remove unwanted date
startdateidx = pd.Index(file["Date"]).get_loc("2019-01-02")
file = file.drop(file.index[0:startdateidx])
enddateidx = pd.Index(file["Date"]).get_loc("2019-10-15")
file = file.drop(file.index[enddateidx+1:])
file = file.reset_index(drop=True)

print(file)
#Save as new pickle file
picklefile = "GBPEER"
outfile = open(picklefile, "wb")
pickle.dump(file,outfile)
outfile.close()

#%%
import pickle
import pandas as pd
monthdictionary = {"Jan":"-01-", 
                   "Feb":"-02-", 
                   "Mar":"-03-", 
                   "Apr":"-04-", 
                   "May":"-05-", 
                   "Jun":"-06-", 
                   "Jul":"-07-", 
                   "Aug":"-08-", 
                   "Sep":"-09-", 
                   "Oct":"-10-",
                   "Nov":"-11-",
                   "Dec":"-12-"}
file = pd.read_csv(r"C:\Documents\HKU\Courses\FINA 4350 Text Analytics and NPL\Project\Sterling Effective Exchange Rate Bank of England  Database.csv")

#Formatting
file = file.rename(columns = {"Date":"Date", "Effective exchange rate index, Sterling (Jan 2005 = 100)                          XUDLBK67":"GBPEER"})
for row in range(len(file)):
    file.at[row,"Date"] = ("20" + file.at[row,"Date"][7:] + monthdictionary[file.at[row,"Date"][3:6]] + file.at[row,"Date"][0:2])


#Remove unwanted date
startdateidx = pd.Index(file["Date"]).get_loc("2019-12-31")
file = file.drop(file.index[0:startdateidx])
enddateidx = pd.Index(file["Date"]).get_loc("2019-10-15")
file = file.drop(file.index[enddateidx+1:])
file = file.reset_index(drop=True)





