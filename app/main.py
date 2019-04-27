from app.TwitterClient import TwitterClient

# creating object of TwitterClient Class
api = TwitterClient()

# query parameters
search_words = "Notre Dame #NotreDame -filter:retweets"
since = "2019-04-15"

# calling function to get tweets
api.get_tweets(query=search_words, date_since=since, count=200)
api.make_analysis()
api.to_csv("results/client_test.csv")
