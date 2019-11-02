# -*- coding: utf-8 -*-
# %% Init
import pandas as pd

from sklearn.model_selection import train_test_split # train-test-split 
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer # tokenization 
from sklearn.naive_bayes import MultinomialNB # naive base model
from sklearn.ensemble import AdaBoostClassifier # ada boost model

# %% Data Preprocessing

# load data
data = pd.read_csv(r"TrainData/Brexit_NotBrexit_Independent.txt", sep = "\t", engine='python')

# create dependent and independent variable 
X = data['text'].values
Y = data['brexit'].values

# split data into train and test data 
df_train, df_test, Y_train, Y_test = train_test_split(X,Y, test_size = 0.2)

# %% Tokenization 

tfidf = TfidfVectorizer(decode_error = "ignore")
X_train = tfidf.fit_transform(df_train)
X_test = tfidf.transform(df_test)

#%% prediction
model_nb = MultinomialNB()
model_nb.fit(X_train, Y_train)
print("naive base model score (train) :" + str(model_nb.score(X_train, Y_train)))
print("naive base model score (test) :" + str(model_nb.score(X_test, Y_test)))

model_ab = AdaBoostClassifier()
model_ab.fit(X_train, Y_train)
print("ada boost model score (train): " + str(model_ab.score(X_train, Y_train)))
print("ada boost model score (test): " + str(model_ab.score(X_test, Y_test)))

