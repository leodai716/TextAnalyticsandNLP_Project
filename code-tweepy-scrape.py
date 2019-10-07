import tweepy

#API log in
access_token = "1181129334968336384-q2TTL9ujFCfxHBfUxghKfR09JVQLaJ"
access_token_secret = "Pa0Z5Zoo6O24DgnrxFh0RQstx65yx5aTTcWQQKK2p4u2I"
consumer_key = "9eBNPCiIe7AExJxE0SvauYMDY"
consumer_secret = "igPSn0FddQasy2LTPUHMzzUGW27s3VofInIdGpYxPY3LKhuLlS"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Check the tweets in your stream.
class listener(tweepy.StreamListener):
    def on_status(self, status):
        with open('data-streaming-tweets.tsv', 'a', encoding = "utf-8") as f:
            retweet = False 
            extendedTweet = False
            try:
                refinedText = status.retweeted_status.extended_tweet['full_text']
                retweet = True 
                extendedTweet = True
            except AttributeError:
                try:
                    refinedText = status.extended_tweet['full_text']
                    extendedTweet = True
                except AttributeError:
                    refinedText = status.text
                
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
