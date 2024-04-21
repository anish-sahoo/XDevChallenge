import asyncio

import xai_sdk
from xai_sdk.ide import *
import flask

PREAMBLE = """\
A Human is asking the Assistant for help with specific tasks. The broader context of the task is \
financial analysis. The assistant will take the human's task and find things in the API relating to \
that task. These things will be related to the human's task in a financial analysis way.
"""
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


@prompt_fn
async def get_terms(stock_name):
    await prompt(GET_TERMS_PROMPT.format(stock=stock_name))
    output = await sample(max_len=200, stop_strings=[".", "<|separator|>"], temperature=0.5)
    return parse_output(output.as_string())


@prompt_fn
async def gen_sentiments(tweet_list):
    # TODO
    return 0


def parse_output(output):
    parsed = output.split(",")[:-1]
    for i in range(len(parsed)):
        parsed[i] = parsed[i][2:]
        if "<|separator|>" in parsed[i]:
            parsed[i] = parsed[i].replace("<|separator|>", "")
    return parsed


async def main():
    await get_terms("POGHF")


asyncio.run(main())
