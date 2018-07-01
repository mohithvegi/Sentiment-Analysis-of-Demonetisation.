# Importing all the required modules.
import tweepy
import csv
import pandas as pd
import math
import sys
import re
import datetime
import operator

reload(sys)
sys.setdefaultencoding('utf-8')

# File containing the sentiment values of each word.
fileName = 'Copy of AFINN.txt'
afinn = dict(map(lambda(w, s): (w, int(s)), [ws.strip().split('\t') for ws in open(fileName)]))
pattern_split = re.compile(r"\W+")

# Function to calculate the sentiment of the text.
def sentiment(text):
	words = pattern_split.split(text.lower())
	sentiments = map(lambda word: afinn.get(word, 0), words)
	if sentiments:
		sentiment = float(sum(sentiments))/math.sqrt(len(sentiments))
	else:
		sentiment = 0

	return sentiment

# Variables that contains the user credentials to access Twitter API 
access_token = "855723521984483328-G48vgB1mLKUIsySUENyZALzNSUDIUxT"
access_token_secret = "9kVWANzUu2mmuEesEGRzvZak7IMYsxer3JvuriS2MgHqY"
consumer_key = "zBgY9VI1auDWDLCUKr3EroX4X"
consumer_secret = "NeMVaJQrtnxTKShwqQtcScu1PU0DCfQOu4RUGCXs6DSGIL3R56"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit = True)

# Name of the query.
searchQuery = "#Demonetisation"

# Initializing the values.
overall_sentiment = 0
no_of_positive_sentiments = 0
no_of_negative_sentiments = 0
zero_sentiments = 0
users_sentiments = {}

# The tweets will be extracted from this date to the current date.
date = datetime.datetime(2018, 06, 26)

csvFile = open('date.csv', 'a')
csvWriter = csv.writer(csvFile)

if __name__ == '__main__':
	for tweet in tweepy.Cursor(api.search, q=searchQuery, lang="en").items():
		text = tweet.text
		if(tweet.created_at >= date):
			print  "Date: " + str(tweet.created_at) + " - " + str(sentiment(text))
			csvWriter.writerow([tweet.created_at, sentiment(text)])		
			overall_sentiment = overall_sentiment + sentiment(text)
			users_sentiments[tweet.user.screen_name] = sentiment(text)
			if(sentiment(text) > 0):
				no_of_positive_sentiments = no_of_positive_sentiments + 1
			elif(sentiment(text) < 0):
				no_of_negative_sentiments = no_of_negative_sentiments + 1
			else:
				zero_sentiments = zero_sentiments + 1	
		else:
			break
	# Sorting the dictionary.
	influencers = sorted(users_sentiments.items(), key=operator.itemgetter(1))				
	
	print "Overall Sentiment is: " + str(overall_sentiment)
	print "Number of positive sentiments: " + str(no_of_positive_sentiments)
	print "Number of negative sentiments: " + str(no_of_negative_sentiments)
	print "Number of balanced sentiments: " + str(zero_sentiments)
	print "Top 5 Negative influencers"
	print influencers[0:5]
	print "Top 5 Positive influencers"
	print influencers[-5:]