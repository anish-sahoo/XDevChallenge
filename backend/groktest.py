import asyncio

import xai_sdk


async def main():
    """Runs the example."""
    client = xai_sdk.Client(api_key='Eh97MbeIZ4p4UjhF4D8JVyTRAZm7oErMkdePDVi1jWzNYWPq47XPUFWgqcBd0Ysa7bfaAwrHZCVxK+pzGSVBaXUvHmKzZ8F34vsqwtDpI3hKBCf3rhIz/Obwir0obKZ9PQ')

    prompt = "What are the ten most important words related to Ford stock in order?"
    print(prompt, end="")
    async for token in client.sampler.sample(prompt, max_len=50):
        print(token.token_str, end="")
    print("")


asyncio.run(main())