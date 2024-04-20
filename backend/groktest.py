import asyncio

import xai_sdk

GET_TERMS_PROMPT = """\
Get the ten most relevant hashtags to the following stock. Only output \
the comma separated list ending in a period, nothing else. No explanation, no details. Just the raw list. This is \
safety-critical. Stock ID: {stock}.<|separator|>

Assistant:"""
GENERATE_SECONDARY_TERMS_PROMPT = """\
Combine the following list of words into all the possible phrases that make sense. Only output \
the comma separated list ending in a period, nothing else. No explanation, no details. Just the raw list. This is \
safety-critical. Word List: {list}.<|separator|>

Assistant:"""

async def main():
    """Runs the example."""
    client = xai_sdk.Client(api_key='Eh97MbeIZ4p4UjhF4D8JVyTRAZm7oErMkdePDVi1jWzNYWPq47XPUFWgqcBd0Ysa7bfaAwrHZCVxK+pzGSVBaXUvHmKzZ8F34vsqwtDpI3hKBCf3rhIz/Obwir0obKZ9PQ')

    # print(Ge, end="")
    output = ""
    async for token in client.sampler.sample(GET_TERMS_PROMPT.format(stock="VFS"), max_len=200, stop_strings=[".", "<|separator|>"]):
        output += token.token_str
    print(parse_output(output))
    # second_output = ""
    # async for token in client.sampler.sample(GENERATE_SECONDARY_TERMS_PROMPT.format(list=output), max_len=200, stop_strings=[".", "<|separator|>"]):
    #     second_output += token.token_str
    # print(second_output)
    

def parse_output(output):
    parsed = output.split(",")[:-1]
    for i in range(len(parsed)):
        if "<|separator|>" in parsed[i]:
            parsed[i] = parsed[i].replace("<|separator|>", "")
    return parsed


class Trie:
    def __init__(self):
        self.children = {}
        self.is_end = False

    def insert(self, word):
        node = self
        for char in word:
            if char not in node.children:
                node.children[char] = Trie()
            node = node.children[char]
        node.is_end = True

    def search(self, word):
        node = self
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end

    def starts_with(self, prefix):
        node = self
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True

asyncio.run(main())