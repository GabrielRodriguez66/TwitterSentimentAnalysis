import re
import pandas as pd
import tweepy
from textblob import TextBlob
from app import API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET


class TwitterClient:

    def __init__(self):

        # attempt authentication and create tweepy API object to fetch tweets
        self.auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
        self.auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        self.api = tweepy.API(self.auth)

        # instance field to store fetched tweets
        self.tweets = []

    '''
     Main function to fetch tweets and parse them in a custom way
    '''

    def get_tweets(self, query, date_since, count=10):

        # fetch tweets
        fetched_tweets = tweepy.Cursor(self.api.search,
                                       q=query,
                                       lang="en",
                                       since=date_since,
                                       tweet_mode='extended').items(count)

        # parsing tweets
        for tweet in fetched_tweets:
            # empty dictionary to store required params of a tweet
            parsed_tweet = {}

            # saving text of tweet and sentiment of tweet
            parsed_tweet['text'] = tweet.full_text
            parsed_tweet['sentiment'] = TwitterClient.__sentiment(tweet.full_text)
            parsed_tweet['username'] = tweet.user.screen_name

            # appending parsed tweet to tweets list
            if tweet.retweet_count > 0:
                # if tweet has retweets, ensure that it is appended only once
                if parsed_tweet not in self.tweets:
                    self.tweets.append(parsed_tweet)
            else:
                self.tweets.append(parsed_tweet)

        return self.tweets

    '''
        Calculate percentages of positive, neutral and negative tweets
    '''

    def make_analysis(self):

        # picking positive and negative tweets from tweets
        ptweets = [tweet for tweet in self.tweets if tweet['sentiment'] == 'positive']
        ntweets = [tweet for tweet in self.tweets if tweet['sentiment'] == 'negative']

        # printing percentages
        print("Positive tweets percentage: {} %".format(100 * len(ptweets) / len(self.tweets)))
        print("Negative tweets percentage: {} %".format(100 * len(ntweets) / len(self.tweets)))
        print("Neutral tweets percentage: {} % \
              ".format(100 * (len(self.tweets) - len(ntweets) - len(ptweets)) / len(self.tweets)))

        # printing first 5 positive tweets
        print("\n\nPositive tweets:")
        for tweet in ptweets[:10]:
            print(tweet['text'])

        # printing first 5 negative tweets
        print("\n\nNegative tweets:")
        for tweet in ntweets[:10]:
            print(tweet['text'])

    '''
        Export fetched tweets to csv in the specified path
    '''

    def to_csv(self, file_path):
        tweet_list = [[tweet['username'], tweet['text'], tweet['sentiment']] for tweet in self.tweets]
        df = pd.DataFrame(data=tweet_list, columns=['Username', 'Tweet', 'Sentiment_Value'])
        df.to_csv(file_path, encoding='utf-8-sig')

    '''
        Utility private function to classify sentiment of passed tweet
    '''

    @staticmethod
    def __sentiment(tweet):

        analysis = TextBlob(TwitterClient.__clean(tweet))
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    '''
        Utility private function to clean tweet text by removing links, special characters
        using simple regex statements.
    '''

    @staticmethod
    def __clean(tweet):
        return ' '.join(
            re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\ / \ / \S+)", " ", re.sub(r"http\S+", "", tweet)).split())

