import sys
from datetime import datetime
from pprint import pprint

import tweepy

api = tweepy.Client(
    bearer_token='AAAAAAAAAAAAAAAAAAAAACmUtQEAAAAAltf1Z0qROW0jZQLzZXK2ohL38t8%3DOayfQArD3CHKqwEPA1gtv2AzJZaMRh2RXw5MXRAFlE50DekfZi')

default_end_time = '2024-04-18T00:00:00Z'

def gather_tweets(end_time, query):
    result = api.search_all_tweets(query=query, max_results=100,
                                   tweet_fields=['public_metrics', 'author_id', 'created_at'],
                                   end_time=end_time,
                                   )
    return result




tweets = gather_tweets(default_end_time)
filtered_tweets = []
print(sys.getsizeof(tweets.data[0]))

for tweet in tweets.data:
    if tweet["public_metrics"]["like_count"] > 5:
        filtered_tweets.append(tweet)
        print(tweet["created_at"])

pprint(filtered_tweets)
