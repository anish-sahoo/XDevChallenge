from pprint import pprint

import tweepy

api = tweepy.Client(
    bearer_token='AAAAAAAAAAAAAAAAAAAAACmUtQEAAAAAltf1Z0qROW0jZQLzZXK2ohL38t8%3DOayfQArD3CHKqwEPA1gtv2AzJZaMRh2RXw5MXRAFlE50DekfZi')

default_end_time = '2024-04-18T00:00:00Z'
def gather_tweets(end_time):
    result = api.search_all_tweets(query='Spurs', max_results=500,
                                   tweet_fields=['public_metrics', 'author_id', 'created_at'],
                                   end_time=end_time,
                                   )
    return result


tweets = gather_tweets()
filtered_tweets = []

for tweet in tweets.data:
    if tweet["public_metrics"]["like_count"] > 5:
        filtered_tweets.append(tweet)
        print(tweet["created_at"])

pprint(filtered_tweets)
