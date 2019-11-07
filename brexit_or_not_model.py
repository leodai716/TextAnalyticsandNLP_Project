'''
This is for building a model that predict whether anarticle is Brexit related
or not.
@author: leodai
'''
#%% Init
import sys
import pandas as pd
import numpy as np
import _LocalVariable
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB # naive base model
from sklearn.ensemble import AdaBoostClassifier # ada boost model
sys.path.append(".")

#%% Loading the data
DATA_PATH = _LocalVariable._DATA_DIRECTORY + "\cleaned_db-BrexitorNot.pkl"
data = pd.read_pickle(DATA_PATH)

#%% Data Transformation
from projectpackage.data_preprocessing import TextProcessing

data['combined_text'] = data['combined_text'].apply(lambda x: x.lower())
data['combined_text'] = data['combined_text'].apply(TextProcessing.combine_specialwords)

#%% Tokenization
from projectpackage.data_preprocessing import DataTransformation

data['tokens'] = None

data['tokens'] = data['combined_text'].apply(DataTransformation.get_tokens)
    
#%% Data transformation (text to numbers)
from projectpackage.data_preprocessing import DataTransformation

# generate word index map
word_index_map = DataTransformation.get_word_index_map(data['tokens'])

data['bow_vector'] = None

data['bow_vector'] = data['tokens'].apply(\
    lambda x: DataTransformation.get_bow_vector(x, word_index_map))

# create Document Term Matrix
TDM = pd.DataFrame(columns=np.arange(len(word_index_map)+1))

for i in range(len(data.index)):
    vector = data['bow_vector'].iloc[i]
    brexit = data['brexit'].iloc[i]
    vector = np.append(vector, brexit)
    vector_df = pd.DataFrame(vector)
    vector_df = vector_df.T
    TDM = TDM.append(vector_df)

#%% Data Processing
x = TDM.iloc[:,:-1]
y = TDM.iloc[:,-1]

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3)


model_nb = MultinomialNB()
model_nb.fit(x_train, y_train)
print("naive base model score (train) :" + str(model_nb.score(x_train, y_train)))
print("naive base model score (test) :" + str(model_nb.score(x_test, y_test)))

model_ab = AdaBoostClassifier()
model_ab.fit(x_train, y_train)
print("ada boost model score (train): " + str(model_ab.score(x_train, y_train)))
print("ada boost model score (test): " + str(model_ab.score(x_test, y_test)))

