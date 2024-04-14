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


RECSYS_PROMPT = """
TASK: Given the text, return a json in the OUTPUT_FORMAT form the text QUERY_MESSAGE. All the content from the JSON should
be from the QUERY_MESSAGE only.

OUTPUT_FORMAT:
json```
{
"release_year": // year in which movie was released, if mentioned in QUERY_MESSAGE else ""
"directors": // list of directors, else []
"actors": // list of directors, else []
"fullplot": // description of the movie, else ""
"genres": // list of genres of movie from the QUERY_MESSAGE, the genres should be one of these ['News', 'Talk-Show', 'Comedy', 'Drama', 'Thriller', 'Family', 'History', 'Fantasy', 'Musical', 'War', 'Horror', 'Action', 'Adventure', 'Romance', 'Biography', 'Animation', 'Short', 'Sci-Fi', 'Western', 'Crime', 'Documentary', 'Film-Noir', 'Mystery', 'Music', 'Sport'], else []
}```

QUERY_MESSAGE: {message}
"""
