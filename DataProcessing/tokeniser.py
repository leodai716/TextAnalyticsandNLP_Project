# This script is created for developing word tokenizer for textual data

#%% Import Test DataSet
import numpy as np
from bs4 import BeautifulSoup
positive_reviews = BeautifulSoup(open(r"D:\Google Drive\Learning\NLP\domain_sentiment_data\sorted_data_acl\electronics\positive.review").read())
positive_reviews = positive_reviews.findAll('review_text')

negative_reviews = BeautifulSoup(open(r"D:\Google Drive\Learning\NLP\domain_sentiment_data\sorted_data_acl\electronics\negative.review").read())
negative_reviews = negative_reviews.findAll('review_text')

diff = len(positive_reviews) - len(negative_reviews)
idxs = np.random.choice(len(negative_reviews), size=diff)
extra = [negative_reviews[i] for i in idxs]
negative_reviews += extra


#%% Create Tokenizer
import nltk
from nltk.stem import WordNetLemmatizer
wordnet_lemmatizer = WordNetLemmatizer()
stopwords = set(w.rstrip() for w in open(r"D:\Google Drive\HKU\Year 4 Sem 1\FINA4350 Text Analytics adn NLP in Finance\TextAnalyticsandNLP_Project\DataProcessing\stopwords.txt"))

# =============================================================================
# this is a 1-gram tokenizer
# disadvantage: not and some negation words will be removed
# might not be very accurate for sentiment analysis, but could be useful for classification
# =============================================================================

def my_tokenizer(s):
    # convert all character to lower case
    s = s.lower()
    # tokenise with nltk word tokenizer 
    tokens = nltk.tokenize.word_tokenize(s)
    # remove stop words
    tokens = [t for t in tokens if t not in stopwords]
    # removing words that are too shart i.e len < 3
    tokens = [t for t in tokens if len(t) > 2]
    # put words into baseform
    tokens = [wordnet_lemmatizer.lemmatize(t) for t in tokens]
    
    return tokens

#%% Tokenizaton 
# creat word index map
word_index_map = {}
current_index = 0 

positive_tokenized = []
negative_tokenized = []
orig_reviews = []

for review in positive_reviews:
    # put reviews to the orig_review list 
    orig_reviews.append(review.text)
    # tokenize each word 
    tokens = my_tokenizer(review.text)
    # put the reviews to positive_tokenized list 
    # Note: tokens is a list (i.e. positive_tokenized is a 2D object)
    positive_tokenized.append(tokens)
    # append the information to the word_index_map
    for token in tokens:
        if token not in word_index_map:
            word_index_map[token] = current_index
            current_index += 1

for review in negative_reviews:
    # put reviews to the orig_review list 
    orig_reviews.append(review.text)
    # tokenize each word 
    tokens = my_tokenizer(review.text)
    # put the reviews to positive_tokenized list 
    # Note: tokens is a list (i.e. negative_tokenized is a 2D object)
    negative_tokenized.append(tokens)
    # append the information to the word_index_map
    for token in tokens:
        if token not in word_index_map:
            word_index_map[token] = current_index
            current_index += 1

print("len(word_index_map):", len(word_index_map))

# create input matrix 

# create function to turn tokens to vector
# Note: label = dependent variable
def tokens_to_vector(tokens, label):
    # create zero vector the size of word_index_map + 1
    v = np.zeros(len(word_index_map)+1)
    # counting the occurance of a word that existed in the string
    for t in tokens:
        i = tokens_to_vector[t]
        v[i] += 1
    # normalize count
    v = v/v.sum()
    # set label for vector
    v[-1] = label
    
    return v

# Vectorization
N = len(positive_tokenized) + len(negative_tokenized)

# create a N by D+1 matrix 
data = np.zeros(N,len(word_index_map) + 1)

i = 0

# create docutment-term matrix 
for tokens in positive_tokenized:
    v = tokens_to_vector(tokens, 1)
    data[i, :] = v
    i += 1

for tokens in negative_tokenized:
    v = tokens_to_vector(tokens, 1)
    data[i, :] = v
    i += 1
    