from textblob import TextBlob
import tweepy
import csv
import os

# Authentication
auth = tweepy.OAuthHandler(os.environ['TWITTER_CONSUMER_KEY'], os.environ['TWITTER_CONSUMER_SECRET'])
auth.set_access_token(os.environ['TWITTER_ACCESS_TOKEN'], os.environ['TWITTER_ACCESS_TOKEN_SECRET'])

# Get API's main object
api = tweepy.API(auth)

# Ask user for a keyword
keyword = input("Enter the keyword you'd like to analyse: ")

# Get public tweets
public_tweets = api.search(keyword)

results_list = []

for tweet in public_tweets:
#   Check what people are thinking
    analysis = TextBlob(tweet.text)
    
#   Translate foreign tweets to English
    if( analysis.detect_language() == 'en' ):
        tweet_text = tweet.text
    else:
        tweet_text = analysis.translate(to='en')
    
#   Removing line breaks
    tweet_text = tweet_text.replace('\n', ' ').replace('\r', '')
    
    results_list.append([tweet_text, analysis.sentiment.polarity, analysis.sentiment.subjectivity])


# Write every tweet to CSV
with open('./out/analysis.csv', 'w') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter='§')
    
#   Header
    spamwriter.writerow(['Tweet','Polarity','Subjectivity'])
    
#   Content    
    for data_point in results_list:
        spamwriter.writerow(data_point)

print('Done!')
print('Go check the CSV file at the "out" folder.')
