

# A Twitter Illiterate's Attempt at Twitter Mining
Hello, I am Mars Leung. In this project where we attempt to read market sentiment online regarding Brexit to predict the movement of the British Pound's strength, I'm responsible for designing the code for its very first stage - Twitter-mining. 

There's only one problem - I don't use Twitter - in fact, none of us does. So in this post,  not only will I walk you through the code, I'll also show you struggle and journey I went through.
## Objectives
To facilitate sentimental analysis through text analytics and natural language processing in the later stages of our project, this sub-project aims to collect raw text data.

 The mission is simple: with a given keyword, the programme should fetch every newly-made Tweet that contains the keyword from Twitter, and dump all of them into a file, all in real time.

Of course, later we'll see, my rather simplistic view of how Twitter works would soon be crushed by the mundanity and agony of the reality *(I'm saying that with a slight hyperbole)*.
## Applying for Access to the Twitter API
I am using the Tweepy packageto perform Twitter-scraping, and that requires access to the Twitter API, for which I needed to apply beforehand. Well actually by itself it's not a hard task. It's just that when I saw this application form, I was reminded of [the red tape of another online platform frequently criticized by their own online creators](https://www.youtube.com/results?search_query=youtube%20is%20broken). 

But it turned out that the approval from Twitter was almost instantaneous, for which I am so grateful, as I can't imagine the whole project being dragged behind waiting for some Twitter employee to manually review and accept my application. Looking back, it's kinda funny how I over-thought things.
![enter image description here](https://github.com/leodai716/TextAnalyticsandNLP_Project/blob/master/_posts/Tweepy%20blog%20post%20images/1.%20API%20application.jpg?raw=true)
So after this tiny speed bump, I went full-on and built a first prototype.
## Understanding Tweeting - the Hard Way
I have coded long enough to know that it's a miracle when a first prototype is working perfectly, if at all. The programme, which in theory could run indefinitely, ran into an error and stopped after about 5 seconds *(uplifting, I know)*.

Looking at the output, there are two problems:
1. The error that broke the programme was `UnicodeEncodeError: 'cp950' codec can't encode character '\U0001f525' in position 60: illegal multibyte sequence`, whatever that meant.
2. Many tweets output were cut off by an ellipsis (...).

![enter image description here](https://github.com/leodai716/TextAnalyticsandNLP_Project/blob/master/_posts/Tweepy%20blog%20post%20images/2.%20bug%20.jpg?raw=true)
So, what happened?

### The Emoji Bug
It turned out Python ran into problem using ordinary `f.write(string)` method when it attempts to output special characters, which are abundant on Twitter in the form of emojis. It's not that Python cannot process emojis  at all - the console can print them after simple string operations with no problem - it's outputting them into an external file that's problematic.
![enter image description here](https://github.com/leodai716/TextAnalyticsandNLP_Project/blob/master/_posts/Tweepy%20blog%20post%20images/3.%20Console.jpg?raw=true)
This problem is new to me, because as a student who learns coding mostly for panel-data analyses, I had had no reason dealing with emojis in my previous projects. 

I soon learnt that I could encode the output file in utf-8 with `open(outputFile, 'a', encoding = "utf-8")`, and somehow it just worked, just like magic. The code was able to run indefinitely at last, and the emojis went straight to the output file with no error. Boom - problem solved! With a grin in my face, I moved to problem 2...
### 140 - the Mystery of the Twitter Phantom
Okay so what the heck was going on with the ellipses? I had no idea, so I looked into the output for clues. Apparently, all cut-off Tweets were at the 140-character mark. 

140 characters - a clue. Does that ring a bell with you? It certainly did with me, but I just couldn't figure it out what it was...

It took me like an hour staring at the ceiling of my room, but it eventually hit - 140 characters - the Tweet character limit! Users could not tweet more than 140 characters. I vaguely remembered the buzz that was going on when [Twitter officially lifted this rule last year](https://techcrunch.com/2018/10/30/twitters-doubling-of-character-count-from-140-to-280-had-little-impact-on-length-of-tweets/) - the character limit now is 280 characters, so why was ye-olde 140 popping up in my code?
### The Unmasking of Erik
Tweets existed in Twitter in the form of objects of class Tweet. And when Twitter lifted the character limit from 140 to 280, instead of simply modifying the behaviour of the existing Tweet object, it creaded a new object class: Extended Tweet. Some additional attributes in this new class allows the Tweet texts to exceed 140 characters.

Simply saying, what my code was doing was reading all Tweets as if they were of the original Tweet class, so they lost the attribute from the Extended Tweet class and got cut off at the 140 mark.

And... it's not just that. Retweets also exist, and they are also of a separate object class themselves. So my code had to account for a Tweet that might or might not be extended, and might or might not be retweeted, any of which has a separate object-class structure.

I could pass the blame to the fact that I don't use Twitter, so I had no idea what a Retweet was or how the character cap was set. But honestly, and it's almost shameful to admit that, I should have read the [documentations](https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/intro-to-tweet-json#extendedtweet) before diving right into the coding. I guess that's the biggest takeaway here. :)

# Ending Words
The code at the end ran perfectly, and we are using it to stream Tweets in real time. After this we will move on to the sentimental-analysis stage, and start the main course. 

*And by the way do you know that on average 7 Tweets are made per second about Brexit? Crazy right?*
![enter image description here](https://github.com/leodai716/TextAnalyticsandNLP_Project/blob/master/_posts/Tweepy%20blog%20post%20images/4.%20Output.jpg?raw=true)
Overall it was quite a journey. I learnt to use a completely unfamiliar package, the importance of reading documentations, and actually built something useful. I look forward to what will be coming in the next few weeks, and I cannot be more excited.
