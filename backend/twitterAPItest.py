import tweepy
from collections import Counter
import os
from dotenv import load_dotenv

load_dotenv()
#
auth = tweepy.OAuthHandler(os.getenv('API_KEY'), os.getenv('API_SECRET'))
auth.set_access_token(os.getenv('ACCESS_TOKEN'), os.getenv('ACCESS_SECRET'))
api = tweepy.API(auth, wait_on_rate_limit=True)
#
# def Gather_Tweets():
#     all_tweets = []
#     # Retrieve the authenticated user's friend IDs
#     friends_ids = api.friends_ids()
#     # Iterate over each friend and fetch their latest tweets
#     for friend_id in friends_ids:
#         # Retrieve friend's latest tweets
#         new_tweets = api.user_timeline(user_id=friend_id, count=20, tweet_mode="extended")
#         # Extract full text from each tweet and append to all_tweets
#         tweets = [tweet.full_text.upper() for tweet in new_tweets]
#         all_tweets.extend(tweets)
#     return all_tweets
#
# def Split_Tweets():
#     all_tweets = Gather_Tweets()
#     split_tweets = []
#     # Split each tweet into words and append to split_tweets
#     for tweet in all_tweets:
#         split_tweets.extend(tweet.split())
#     return split_tweets
#
# def Sort_Ticker():
#     split_tweets = Split_Tweets()
#     tickers = []
#     # Extract ticker symbols from words
#     for word in split_tweets:
#         if word.startswith("$") and word[1:].isalpha() and len(word) < 6:
#             tickers.append(word)
#     return tickers
#
# def Organize_Trending():
#     tickers = Sort_Ticker()
#     # Use Counter to count occurrences of each ticker symbol
#     data = Counter(tickers).most_common(25)
#     return data
#
# print(Organize_Trending())


def Gather_Tweets():
    all = []
    friends = api.get_friend_ids()
    for friend in friends:
        new_tweets = api.user_timeline(api.get_user(friend).screen_name, count=20, page = 5, tweet_mode='extended')
        tweets = [tweet.full_text.upper() for tweet in new_tweets]
        all.append(tweets)
    return all
print(Gather_Tweets())