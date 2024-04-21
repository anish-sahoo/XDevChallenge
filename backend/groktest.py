import asyncio

import xai_sdk
from xai_sdk.ide import *
import flask
import json
import re
from datetime import datetime, timezone

PREAMBLE = """\
A Human is asking the Assistant for help with specific tasks. The broader context of the task is \
financial analysis. The assistant will take the human's task and find things in the API relating to \
that task. These things will be related to the human's task in a financial analysis way."""
GET_TERMS_PROMPT = """\
Human: Get the ten most relevant hashtags to the following stock. Only output \
the comma separated list ending in a period, nothing else. No explanation, no details. Just the raw list. This is \
safety-critical. Stock ID: {stock}.<|separator|>

Assistant:"""

GENERATE_SECONDARY_TERMS_PROMPT = """\
Human: Combine the following list of words into all the possible phrases that make sense. Only output \
the comma separated list ending in a period, nothing else. No explanation, no details. Just the raw list. This is \
safety-critical. Word List: {list}.<|separator|>

Assistant:"""

GENERATE_SENTIMENTS_PROMPT = """\
Human: The following list will be formatted in tuples of a tweet and its number of likes. For Example: \
[(I love pizza, 5), (Pizza is the best, 20), (I hate brussel sprouts, 6), (Brussel sprouts suck, 19)]. \
Evaluate the sentiment of each tweet. Include the number of like in the evaluation. Only output \
Please provide the sentiment of each tweet. Only output the comma separated list ending in a period, \
nothing else. No explanation, no details. Just the raw list. This is safety-critical. \
Tweet List: {list}.<|separator|>

Assistant:"""

GENERATE_PREDICTIONS_PROMPT = """\
The format for a Tweet List is a list of tuples. Each tuple has a string for the tweet, number of likes, and the day it was posted. \
The date is formatted: YYYY-MM-DD. For a pizza company stock it would look like: [('I love pizza', 5, '2024-04-19'), \
('Pizza is the best', 20, '2024-04-20'), ('Cheese has been cheaper lately', 6, '2024-04-19'), ('Italian restaurants have been popular lately', 19, '2024-04-20')]. \
\n\
A Stock Price contains: the opening price of a stock, the highest price of the stock, the lowest price of the stock, \
the closing price of the stock, and the day for which all of this data was recorded. The provided format for a Stock Price \
is a list of tuples and the date. The tuples each contain the label for which price measurement it is and the actual price measurement. The date is in YYYY-MM-DD form. For Example: \
[('1. open', '3.34'), ('2. high', '4.12'), ('3. low', '2.94'), ('4. close', '3.72'), '2024-04-19'] \
\n\
A Stock Price List is a list of Stock Prices, where the Stock Prices are formatted as above. For Example: \
[[('1. open', '7.43'), ('2. high', '8.21'), ('3. low', '6.49'), ('4. close', '7.27'), '2024-03-09'], \
[('1. open', '7.27'), ('2. high', '8.22'), ('3. low', '6.43'), ('4. close', '7.49'), '2024-03-10']] \
\n\
Human: There will be Tweet List, Stock Price List and a Stock Name following the instructions. The Tweet List will be about topics relevant to the Stock Name. \
The Stock Price List will contain the stock prices for the Stock Name. Use the data from these sources to predict the next three days stock prices. \
Output the predictions in an Stock Price List with exactly three entries. Like the following template: \
[[('1. open', '3.34'), ('2. high', '4.16'), ('3. low', '2.89'), ('4. close', '3.62'), '2024-01-11'], \
[('1. open', '3.62'), ('2. high', '4.22'), ('3. low', '3.34'), ('4. close', '3.94'), '2024-01-12'], \
[('1. open', '3.94'), ('2. high', '4.32'), ('3. low', '3.54'), ('4. close', '4.12'), '2024-01-13']] \
Provide no other words. No explanations. No details. Just the raw list. This is safety-critical. \
Tweet List: {tweets}, Stock Price List: {stocks}, Stock Name: {ticker}<|separator|>

Assistant:"""

# GENERATE_PREDICTIONS_PROMPT = """\
# Human: There will be 2 provided lists and a Stock Name. A Tweet List and Stock Price List. The Tweet List will be formatted \
# as a list of tuples. Each tuple has string for the tweet, number of likes, and the day it was posted. These tweets contain information \
# about the stock and relevant fields and topics to the stock. The date is formatted: YYYY-MM-DD For a pizza company stock it would look like: \
# [('I love pizza', 5, '2024-04-19'), ('Pizza is the best', 20, '2024-04-20'), ('Cheese has been cheaper lately', 6, '2024-04-19'), ('Italian restaurants have been popular lately', 19, '2024-04-20')]. \
# The Stock Price List will be formatted as a list of list of tuples. Each internal list has 4 tuples and a string \
# which contain the open, high, low, close, and date of the stock price. The tuples have a \
# string for the label and a string for the dollar value of the stock the label. For Example: ('1. open', '5.67') \
# is the open price of the stock. The string for the date of the stock data is in YYYY-MM-DD format. For Example:\
# '2024-03-19'. The whole Stock Price List will have a format like the example below: \
# [[('1. open', '3.34'), ('2. high', '4.12'), ('3. low', '2.94'), ('4. close', '3.72'), '2024-04-19'], \
# [('1. open', '3.72'), ('2. high', '4.22'), ('3. low', '3.34'), ('4. close', '3.94'), '2024-04-20']] \
# Use the information about the public and financial opinion data from the tweets in combination with the stock data \
# to predict the stock prices of the provided stock for the next 3 days. Output the data in the exact same format as the Stock Price List. \
# Only output the properly formatted predictions nothing else. No explanation, no details. Just the raw list. This is safety-critical. \
# Tweet List: {tweets}, Stock Price List: {stocks}, Stock Name: {ticker}<|separator|>

# Assistant:"""

GENERATE_SHORT_PREDICTIONS = """\
Human: There will be 2 provided lists and a Stock Name. A Tweet List and Stock Price List. The Tweet List will be formatted \
as a list of tuples. Each tuple has string for the tweet, number of likes, and the day it was posted. These tweets contain information \
about the stock and relevant fields and topics to the stock. The date is formatted: YYYY-MM-DD For a pizza company stock it would look like: \
[('I love pizza', 5, '2024-04-19'), ('Pizza is the best', 20, '2024-04-20'), ('Cheese has been cheaper lately', 6, '2024-04-19'), ('Italian restaurants have been popular lately', 19, '2024-04-20')]. \
The Stock Price List will be formatted as a list of list of tuples. Each internal list has 5 tuples \
which contain the open, high, low, close, and date of the stock price. The 4 of the tuples have a \
string for the label and a string for the dollar value of the stock the label. For Example: ('1. open', '5.67') \
is the open price of the stock. The last tuple has a string for the date of the stock data. For Example:\
('2024-03-19'). The whole Stock Price List will have a format like the example below: \
[[('1. open', '3.34'), ('2. high', '4.12'), ('3. low', '2.94'), ('4. close', '3.72'), ('2024-04-19')], \
[('1. open', '3.72'), ('2. high', '4.22'), ('3. low', '3.34'), ('4. close', '3.94'), ('2024-04-20')]] \
Use the information about the public and financial opinion data from the tweets in combination with the stock data \
to predict the short term outlook of the stock and return a list of three key elements from the short term outlook. \
Tweet List: {tweets}, Stock Price List: {stocks}, Stock Name: {ticker}<|separator|>

Assistant:"""

GENERATE_LONG_PREDICTIONS = """\
Human: There will be 2 provided lists and a Stock Name. A Tweet List and Stock Price List. The Tweet List will be formatted \
as a list of tuples. Each tuple has string for the tweet, number of likes, and the day it was posted. These tweets contain information \
about the stock and relevant fields and topics to the stock. The date is formatted: YYYY-MM-DD For a pizza company stock it would look like: \
[('I love pizza', 5, '2024-04-19'), ('Pizza is the best', 20, '2024-04-20'), ('Cheese has been cheaper lately', 6, '2024-04-19'), ('Italian restaurants have been popular lately', 19, '2024-04-20')]. \
The Stock Price List will be formatted as a list of list of tuples. Each internal list has 5 tuples \
which contain the open, high, low, close, and date of the stock price. The 4 of the tuples have a \
string for the label and a string for the dollar value of the stock the label. For Example: ('1. open', '5.67') \
is the open price of the stock. The last tuple has a string for the date of the stock data. For Example:\
('2024-03-19'). The whole Stock Price List will have a format like the example below: \
[[('1. open', '3.34'), ('2. high', '4.12'), ('3. low', '2.94'), ('4. close', '3.72'), ('2024-04-19')], \
[('1. open', '3.72'), ('2. high', '4.22'), ('3. low', '3.34'), ('4. close', '3.94'), ('2024-04-20')]] \
se the information about the public and financial opinion data from the tweets in combination with the stock data \
to predict the long term outlook of the stock and return a list of three key elements from the long term outlook. \
Tweet List: {tweets}, Stock Price List: {stocks}, Stock Name: {ticker}<|separator|>

Assistant:"""

@prompt_fn
async def get_terms(stock_name):
    await prompt(GET_TERMS_PROMPT.format(stock=stock_name))
    output = await sample(max_len=200, stop_strings=[".", "<|separator|>"], temperature=0.5)
    return parse_term_output(output.as_string())

@prompt_fn
async def gen_predictions(tweet_list, stock_list, stock_name):
    tweet_list = parse_tweet_input(tweet_list)
    stock_list = parse_stock_input(stock_list)
    await prompt(GENERATE_PREDICTIONS_PROMPT.format(tweets=tweet_list, stocks=stock_list, ticker=stock_name))
    output = await sample(max_len=1024, stop_strings=[".", "<|separator|>"], temperature=0.5)
    str_out = output.as_string()
    return parse_stock_output(str_out)

@prompt_fn
async def gen_short(tweet_list, stock_list, stock_name):
    tweet_list = parse_tweet_input(tweet_list)
    stock_list = parse_stock_input(stock_list)
    await prompt(GENERATE_SHORT_PREDICTIONS.format(tweets=tweet_list, stocks=stock_list, ticker=stock_name))
    output = await sample(max_len=1024, stop_strings=[".", "<|separator|>"], temperature=0.5)
    return output.as_string()

@prompt_fn
async def gen_long(tweet_list, stock_list, stock_name):
    tweet_list = parse_tweet_input(tweet_list)
    stock_list = parse_stock_input(stock_list)
    await prompt(GENERATE_LONG_PREDICTIONS.format(tweets=tweet_list, stocks=stock_list, ticker=stock_name))
    output = await sample(max_len=1024, stop_strings=[".", "<|separator|>"], temperature=0.5)
    return output.as_string()

def parse_tweet_input(input):
    parsed = []
    for tweet in input:
        datetime_time = tweet["created_at"].replace(tzinfo=timezone.utc)
        parsed.append((tweet.text, tweet["public_metrics"]["like_count"], datetime_time.strftime("%Y-%m-%d")))
    return parsed

def parse_stock_input(input):
    parsed = []
    print("parse_stock_input")
    dict_form = input
    for key in dict_form:
        entry = []
        entry.append(("1. open", dict_form[key]["1. open"]))
        entry.append(("2. high", dict_form[key]["2. high"]))
        entry.append(("3. low", dict_form[key]["3. low"]))
        entry.append(("4. close", dict_form[key]["4. close"]))
        entry.append((key))
        parsed.append(entry)
    return parsed

def parse_term_output(output):
    parsed = output.split(",")[:-1]
    for i in range(len(parsed)):
        if "#" in parsed[i]:
            parsed[i].replace("#", "")
        if "<|separator|>" in parsed[i]:
            parsed[i] = parsed[i].replace("<|separator|>", "")
        parsed[i].strip()
    return parsed

def parse_stock_output(str_out):
    str_out = str_out[2:-2]
    str_out = str_out.split("], [")
    new_dict = {}
    for t in str_out:
        temp_dict= {}
        t = t[1:]
        t = t.split("), (")
        temp = t[-1].split('), ')
        t.pop(-1)
        t.extend(temp)
        for l in t[:-1]:
            l = l.split(", ")

            temp_dict[l[0]] = l[1]
        new_dict[t[-1]] = temp_dict
    print("parse_stock_output")
    return json.dumps(new_dict)