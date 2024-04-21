import asyncio

import xai_sdk
from xai_sdk.ide import *
import flask
PREAMBLE = """\
A Human is asking the Assistant for help with specific tasks. The broder context of the taks is \
financial analysis. The assistant 
"""
GET_TERMS_PROMPT = """\
Human: Get the ten most relevant terms to the following stock. Only output \
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

async def main():
    """Runs the example."""
    client = xai_sdk.Client(api_key='Eh97MbeIZ4p4UjhF4D8JVyTRAZm7oErMkdePDVi1jWzNYWPq47XPUFWgqcBd0Ysa7bfaAwrHZCVxK+pzGSVBaXUvHmKzZ8F34vsqwtDpI3hKBCf3rhIz/Obwir0obKZ9PQ')
    term_list = await get_terms()
    # await gen_modified(term_list)

    # print(Ge, end="")
@prompt_fn
async def get_terms():
    await prompt(GET_TERMS_PROMPT.format(stock="WMT"))
    output = await sample(max_len=200, stop_strings=[".", "<|separator|>"], temperature=0.5)
    print(parse_output(output.as_string()))
    return parse_output(output.as_string())
@prompt_fn
async def gen_modified(term_list):
    await prompt(GENERATE_SECONDARY_TERMS_PROMPT.format(list=term_list))
    output = await sample(max_len=200, stop_strings=[".", "<|separator|>"], temperature=0.5)
    print(parse_output(output.as_string()))
    return parse_output(output.as_string())
    # second_output = ""
    # async for token in client.sampler.sample(GENERATE_SECONDARY_TERMS_PROMPT.format(list=output), max_len=200, stop_strings=[".", "<|separator|>"]):
    #     second_output += token.token_str
    # print(second_output)
    

def parse_output(output):
    parsed = output.split(",")[:-1]
    for i in range(len(parsed)):
        # parsed[i] = parsed[i][2:]
        if "<|separator|>" in parsed[i]:
            parsed[i] = parsed[i].replace("<|separator|>", "")
    return parsed





asyncio.run(main())