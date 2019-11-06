# This code is scripted for mining twitter tweets data
import sys
import os
import tweepy

#%% Init 
sys.path.append("..")
import _LocalVariable

os.chdir(_LocalVariable._DATA_DIRECTORY)

#%% Get tweets
#API log in
auth = tweepy.OAuthHandler(_LocalVariable._TWITTER_CONSUMER_KEY,\
                           _LocalVariable._TWITTER_CONSUMER_SECRET)
auth.set_access_token(_LocalVariable._TWITTER_ACCESS_TOKEN,\
                      _LocalVariable._TWITTER_ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

#Output file name and/or directory
outputFile = 'raw_data-tweets-streaming.tsv'

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
