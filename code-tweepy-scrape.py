# set director
import os

os.chdir(r"D:\Google Drive\HKU\Year 4 Sem 1\FINA4350 Text Analytics adn NLP in Finance\TextAnalyticsandNLP_Project")

import tweepy

#API log in
access_token = "1181129334968336384-q2TTL9ujFCfxHBfUxghKfR09JVQLaJ"
access_token_secret = "Pa0Z5Zoo6O24DgnrxFh0RQstx65yx5aTTcWQQKK2p4u2I"
consumer_key = "9eBNPCiIe7AExJxE0SvauYMDY"
consumer_secret = "igPSn0FddQasy2LTPUHMzzUGW27s3VofInIdGpYxPY3LKhuLlS"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

#Output file name and/or directory
outputFile = 'data-streaming-tweets.tsv'

# Check the tweets in your stream.
class listener(tweepy.StreamListener):
    def on_status(self, status):
        with open(outputFile, 'a', encoding = "utf-8") as f:

            #Whether the tweet is a retweet and whether it is an extended tweet
            retweet = hasattr(status, "retweeted_status")
            extendedTweet = True    #by default

            try:    #for rare cases where some machines fail to process certain emojis (aka the "Flag Bug"); or overall uncaptured bugs
                #try-except operations to extract full texts from status
                try:
                    refinedText = status.retweeted_status.extended_tweet['full_text']
                except AttributeError:
                    try:
                        refinedText = status.extended_tweet['full_text']
                    except AttributeError:
                        refinedText = status.text
                        extendedTweet = False

                #Removing new line and tabs
                refinedText = refinedText.replace("\n", " ").replace("\t", " ").replace("\ufffd", " ")

                #Print to console (unecessary; just cool to stare at and for debug use)
                print(status.user.screen_name, status.user.followers_count, status.created_at,\
                      refinedText, retweet, extendedTweet, "\n", sep="\n")

                f.write(            # Write the data to file.
                    status.user.screen_name + '\t' + \
                    str(status.user.followers_count) + '\t' + \
                    str(status.created_at) + '\t' + \
                    refinedText + '\t' + \
                    str(retweet) + '\t' + \
                    str(extendedTweet) + '\n')
            except: #for rare cases where some machines fail to process certain emojis (aka the "Flag Bug"); or overall uncaptured bugs
                f.close()
                on_error
                pass
    def on_error(self, status_code):
        print(status_code)

# Instantiate an object of class `tweepy.Stream`.
mystream = \
    tweepy.Stream(
        auth=api.auth,
        listener=listener(),
        tweet_mode = 'extended')

# Filter
mystream.filter(languages=["en"], track=['Brexit'])
