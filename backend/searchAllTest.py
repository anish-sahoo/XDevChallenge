import sys
from datetime import datetime
from pprint import pprint
import threading

import tweepy

api = tweepy.Client(
    bearer_token='AAAAAAAAAAAAAAAAAAAAACmUtQEAAAAAltf1Z0qROW0jZQLzZXK2ohL38t8%3DOayfQArD3CHKqwEPA1gtv2AzJZaMRh2RXw5MXRAFlE50DekfZi')

default_end_time = '2024-04-18T00:00:00Z'

def filter_tweets(tweets_list):
    temp_list = []
    for tweet in tweets_list:
        if tweet["public_metrics"]["like_count"] > 5:
            temp_list.append(tweet)
            print(tweet["created_at"])
    filtered_tweets.append(temp_list)

def gather_tweets(end_time, query):
    result = api.search_all_tweets(query=query, max_results=100,
                                   tweet_fields=['public_metrics', 'author_id', 'created_at'],
                                   end_time=end_time,
                                   )
    return result



#loop this
tweets = gather_tweets(default_end_time)
filtered_tweets = []
t_list = []
print(sys.getsizeof(tweets.data[0]))
t = threading.Thread(target=filter_tweets, args=(tweets.data)).start()
t_list.append(t)

while t_list:
    for i in range(len(t_list), 0, -1):
        if not t_list[i].is_alive():
            t_list.pop(i)

pprint(filtered_tweets)
