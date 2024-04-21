import tweepy
from collections import Counter
import os
import requests
from dotenv import load_dotenv

load_dotenv()

# auth = tweepy.OAuthHandler(os.getenv('API_KEY'), os.getenv('API_SECRET'))
# auth = tweepy.OAuthHandler(access_token=os.getenv('ACCESS_TOKEN'), access_token_secret=os.getenv('ACCESS_TOKEN_SECRET'),
#                            consumer_secret=os.getenv('CONSUMER_SECRET'), consumer_key=os.getenv('CONSUMER_KEY'))
# # auth.set_access_token(os.getenv('ACCESS_TOKEN'), os.getenv('ACCESS_SECRET'))
# print(os.getenv('ACCESS_TOKEN'))
# print(os.getenv('ACCESS_SECRET'))
# print(os.getenv('API_KEY'))
# print(os.getenv('API_SECRET'))

# api = tweepy.API(auth)

api = tweepy.Client(bearer_token=os.getenv('BEARER_TOKEN'))

# # def Gather_Tweets():
# #     all_tweets = []
# #     # Retrieve the authenticated user's friend IDs
# #     friends_ids = api.friends_ids()
# #     # Iterate over each friend and fetch their latest tweets
# #     for friend_id in friends_ids:
# #         # Retrieve friend's latest tweets
# #         new_tweets = api.user_timeline(user_id=friend_id, count=20, tweet_mode="extended")
# #         # Extract full text from each tweet and append to all_tweets
# #         tweets = [tweet.full_text.upper() for tweet in new_tweets]
# #         all_tweets.extend(tweets)
# #     return all_tweets
# #
# # def Split_Tweets():
# #     all_tweets = Gather_Tweets()
# #     split_tweets = []
# #     # Split each tweet into words and append to split_tweets
# #     for tweet in all_tweets:
# #         split_tweets.extend(tweet.split())
# #     return split_tweets
# #
# # def Sort_Ticker():
# #     split_tweets = Split_Tweets()
# #     tickers = []
# #     # Extract ticker symbols from words
# #     for word in split_tweets:
# #         if word.startswith("$") and word[1:].isalpha() and len(word) < 6:
# #             tickers.append(word)
# #     return tickers
# #
# # def Organize_Trending():
# #     tickers = Sort_Ticker()
# #     # Use Counter to count occurrences of each ticker symbol
# #     data = Counter(tickers).most_common(25)
# #     return data
# #
# #
# # print(Organize_Trending())
#
# def get_trending_topics():
#     try:
#         # Get the list of trending topics
#         trends = api.trends_place(id=1)  # id=1 for global trends, you can specify other locations' WOEID
#         if trends:
#             trending_topics = trends[0]['trends']
#             # Extract topic names
#             topics = [topic['name'] for topic in trending_topics]
#             return topics
#         else:
#             print("No trending topics found.")
#             return []
#     except tweepy.TweepError as e:
#         print("Error:", e)
#         return []
#
# # Example usage
# trending_topics = get_trending_topics()
# print("Trending topics:")
# for i, topic in enumerate(trending_topics, start=1):
#     print(f"{i}. {topic}")

# def Gather_Tweets():
#     all = []
#     friends = api.get_friend_ids()
#     for friend in friends:
#         new_tweets = api.user_timeline(api.get_user(friend).screen_name, count=20, page = 5, tweet_mode='extended')
#         tweets = [tweet.full_text.upper() for tweet in new_tweets]
#         all.append(tweets)
#     return all
# print(Gather_Tweets())



# assign the values accordingly

# authorization of consumer key and consumer secret
# auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
#
# # set access to user's access key and access secret
# auth.set_access_token(access_token, access_token_secret)

# calling the api

# WOEID of London
woeid = 23424977

# fetching the trends
# trends = api.get_place_trends(id=woeid)

# printing the information
#print("The top trends for the location are :")

# for value in trends:
#     for trend in value['trends']:
#        print(trend['name'])

def get_trending_topics(query):
    try:
        tweets = api.search_all_tweets(q=query, lang='en', count=100)
        hashtags = []
        for tweet in tweets:
            for hashtag in tweet.entities.get('hashtags', []):
                hashtags.append(hashtag['text'])
        hashtag_counts = {}
        for hashtag in hashtags:
            hashtag_counts[hashtag] = hashtag_counts.get(hashtag, 0) + 1
        sorted_hashtags = sorted(hashtag_counts.items(), key=lambda x: x[1], reverse=True)
        return sorted_hashtags[:10]
    except tweepy.errors.TweepyException as e:
#        print("Error:", e)
        return []


# company_query = 'Apple'
# trending_topics = get_trending_topics(company_query)
# print("Trending topics related to", company_query)
# for topic, count in trending_topics:
#     print(f"{topic}: {count} tweets")


# def get_trending_from_hashtag(hashtag, count=30):
#     try:
#         search_url = f"https://api.twitter.com/1.1/search/tweets.json?q=%23{hashtag}&count={count}"
#         response = requests.get(search_url, headers={"Authorization": f"Bearer {os.getenv('ACCESS_TOKEN')}"})
#         response.raise_for_status()  # Raise an exception for unsuccessful requests
#         hashtags = []
#         for tweet in response.json().get('statuses', []):
#             for hashtag in tweet['entities']['hashtags']:
#                 hashtags.append(hashtag['text'])
#         hashtag_counts = {}
#         for hashtag in hashtags:
#             hashtag_counts[hashtag] = hashtag_counts.get(hashtag, 0) + 1
#         sorted_hashtags = sorted(hashtag_counts.items(), key=lambda x: x[1], reverse=True)
#         return sorted_hashtags[:count]  # Return top `count` trending hashtags
#     except Exception as e:
#         print("Error:", e)
#         return []
#
# # Example usage: Get trending topics from a hashtag (e.g., #python)
# hashtag = 'python'
# trending_topics = get_trending_from_hashtag(hashtag, count=30)
# print(f"Trending topics from #{hashtag}:")
# for topic, count in trending_topics:
#     print(f"{topic}: {count} occurrences")
#
#

# def get_top_tweets_with_hashtags(hashtag, count=30):
#     try:
#         # Define a filter rule to listen for tweets containing the hashtag and filtered by 'like'
#         rules = [{"value": f"#{hashtag} has:likes", "tag": "hashtag_likes"}]
#
#         # Create or update the filter rules
#         response = api.create_stream_filter(rules=rules)
#         filter_id = response.data.get('id')
#
#         # Collect tweets from the filtered stream
#         for tweet in api.filtered_stream(filter_id):
#             # Extract relevant information from the tweet
#             tweet_info = {
#                 'text': tweet.text,
#                 'likes': tweet.favorite_count
#             }
#             top_tweets.append(tweet_info)
#             # Stop collecting tweets once we have enough
#             if len(top_tweets) >= count:
#                 break
#
#         # Delete the filter rules
#         api.delete_stream_filter(filter_id)
#
#         return top_tweets
#     except tweepy.errors.TweepyException as e:
#         print("Error:", e)
#         return []
#
# hashtag = 'python'
# top_tweets = get_top_tweets_with_hashtags(hashtag, count=30)
# print(f"Top tweets with #{hashtag} (sorted by likes count):")
# for index, tweet_info in enumerate(top_tweets, start=1):
#     print(f"{index}. Likes: {tweet_info['likes']}, Tweet: {tweet_info['text']}")