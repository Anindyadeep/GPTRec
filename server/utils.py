import os
import requests
from dotenv import load_dotenv
from prompts import SYSTEM_PROMPT_FOR_SALES, SYSTEM_PROMPT_FOR_RERANK, INPUT_TEMPLATE_FOR_RERANK, INPUT_TEMPLATE_FOR_SALES

load_dotenv()


def fetch_poster(movie_id):
    # Helper function to get posters from TMDB, will be helpful later
    api_key = os.environ.get("TMDB_API_KEY")
    response = requests.get(
        f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}"
    )
    data = response.json()
    print(data)
    return "https://image.tmdb.org/t/p/w500/" + data["poster_path"]


# TODO: Avoid redundant schema, since same things are also added on server

def dummy_recommend(search_id: str, query: str):
    dummy_data = [
        {
            "id": 50357,
            "name": "Apollo 18",
            "link": "https://image.tmdb.org/t/p/w500//oW6oUKY2oiQbynwllFboYscVzct.jpg",
        },
        {
            "id": 228326,
            "name": "The Book of Life",
            "link": "https://image.tmdb.org/t/p/w500//aotTZos5KswgCryEzx2rlOjFsm1.jpg",
        },
        {
            "id": 16911,
            "name": "The Inhabited Island",
            "link": "https://image.tmdb.org/t/p/w500//hG2PDKqPZwwC1MTDig3pbTkmXm4.jpg",
        },
        {
            "id": 27579,
            "name": "The American",
            "link": "https://image.tmdb.org/t/p/w500//5OEOsRaBsSxD0qBtAhus0iKDzr.jpg",
        },
        {
            "id": 679,
            "name": "Aliens",
            "link": "https://image.tmdb.org/t/p/w500//r1x5JGpyqZU8PYhbs4UcrO1Xb6x.jpg",
        },
    ]
    
    return {
        "id": search_id,
        "query": query,
        "result": dummy_data
    }


def get_user_history_insight_summary():
    window_size = 8
    chat_history = None # Fetch the previous chat history
    return ""


def prepare_input(text: str, recommend_results = None):
    # or we can do even better, run a LLM in parallel that will give insight of the chat
    # note: if we implement this function then it will update some database time to time 
    # after a certain batch of chat number is accumulated 

    user_history_insight_summary = get_user_history_insight_summary()
    
    # prompt will have two types of mode
    # one will be a chat mode which is like more of a persuation mode
    # where as other will be reranking mode, which will directly affect the search re-rank 

    system_prompt = SYSTEM_PROMPT_FOR_RERANK if recommend_results else SYSTEM_PROMPT_FOR_SALES
    
    if recommend_results:
        input_prompt = INPUT_TEMPLATE_FOR_RERANK.format(results=recommend_results or "", user_input=text)
    else:
        input_prompt = INPUT_TEMPLATE_FOR_SALES.format(user_input=text, chat_summary=user_history_insight_summary)
    
    return system_prompt, input_prompt