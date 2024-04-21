import sys
from datetime import datetime, timedelta, timezone
from pprint import pprint
import threading
import time
import tweepy

api = tweepy.Client(
    bearer_token='AAAAAAAAAAAAAAAAAAAAACmUtQEAAAAAltf1Z0qROW0jZQLzZXK2ohL38t8%3DOayfQArD3CHKqwEPA1gtv2AzJZaMRh2RXw5MXRAFlE50DekfZi',
    wait_on_rate_limit=True)

default_end_time = (datetime.now(timezone.utc) - timedelta(hours=3, minutes=0)).strftime("%Y-%m-%dT%H:%M:%SZ")



def gather_tweets(end_time, query):
    result = api.search_all_tweets(query=query, max_results=500,
                                   tweet_fields=['public_metrics', 'author_id', 'created_at'],
                                   end_time=end_time,
                                   )
    return result




def get_all_tweets(list_terms):

    for i in range(0, len(list_terms), -2):
        list_terms[i] += " " + list_terms[i - 1]
        list_terms.pop(i - 1)
    filtered_tweets = []
    def filter_tweets(tweets_list):
        temp_list = []
        for tweet in tweets_list:
            if tweet["public_metrics"]["like_count"] > 9:
                temp_list.append(tweet)
        filtered_tweets.extend(temp_list)
    t_list = []

    for term in list_terms:
        format_string = "%Y-%m-%dT%H:%M:%SZ"
        datetime_time = datetime.strptime(default_end_time, format_string).replace(tzinfo=timezone.utc)
        while (datetime.now(timezone.utc) - datetime_time).days < 7 and len(filtered_tweets) < 17:
            print(datetime_time.strftime(format_string))
            tweets = gather_tweets(datetime_time.strftime(format_string), term)
            if (tweets.data is None):
                break
            filter_tweets(tweets.data)
            # t = threading.Thread(target=filter_tweets, args=[tweets.data]).start()
            # t_list.append(t)
            datetime_time = tweets.data[-1]["created_at"].replace(tzinfo=timezone.utc)
    return filtered_tweets
