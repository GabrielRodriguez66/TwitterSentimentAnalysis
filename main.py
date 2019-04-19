import tweepy
import credentials as cred
import pandas as pd
import re


def remove_url(tweet):
    return re.sub(r"http\S+", "", tweet)


auth = tweepy.OAuthHandler(cred.API_KEY, cred.API_SECRET_KEY)
auth.set_access_token(cred.ACCESS_TOKEN, cred.ACCESS_TOKEN_SECRET)

api = tweepy.API(auth, wait_on_rate_limit=True)

search_words = "UPRM -filter:retweets"
date_since = "2019-01-01"

tweets = tweepy.Cursor(api.search,
                       q=search_words,
                       lang="es",
                       since=date_since,
                       tweet_mode='extended').items(50)

tweet_list = [[tweet.user.screen_name, remove_url(tweet.full_text)] for tweet in tweets]

df = pd.DataFrame(data=tweet_list, columns=['Username', 'Tweet'])

df.to_csv('tweets.csv', encoding='utf-8-sig')



