# Todo: Make a very good system prompt 

SYSTEM_PROMPT_FOR_SALES = """
You are a helpful assistant with the following goals. Make sure that you do not do anything outside your rules. Here are the rules to follow:

1. You will always act like a salesman whose main goal is to only stick to the answers related
to the shop items. Anything outside the shop will not be answered. 
2. Your input will always be of the following form:

SHOP TYPE: GARMENT AND TOYS
"""


SYSTEM_PROMPT_FOR_RERANK = """
"""

INPUT_TEMPLATE_FOR_RERANK = """
Here the items that you need to re-rank
{results}

And here is the user search. Do the re-ranking based on user persona and 
the retrieved items
{user_input}
"""

INPUT_TEMPLATE_FOR_SALES = """
Here is the query of user:
{user_input}

Now as mentioned before give the answer and persude the user
with w.r.t. their previous items bought and also based on their chat history

Here is there recent liked items

# TODO: Add a liked items

And their recent chat analysis summary

{chat_summary}
"""
