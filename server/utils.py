import os
import requests
from dotenv import load_dotenv
from prompts import (
    SYSTEM_PROMPT_FOR_SALES,
    SYSTEM_PROMPT_FOR_RERANK,
    INPUT_TEMPLATE_FOR_RERANK,
    INPUT_TEMPLATE_FOR_SALES,
)

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
            "id": "573a13adf29313caabd29a2b",
            "title": "Inglourious Basterds",
            "rating": 8.3,
            "banner_url": "https://m.media-amazon.com/images/M/MV5BOTJiNDEzOWYtMTVjOC00ZjlmLWE0NGMtZmE1OWVmZDQ2OWJhXkEyXkFqcGdeQXVyNTIzOTk5ODM@._V1_SY1000_SX677_AL_.jpg",
            "plot": "In Nazi-occupied France during World War II, a plan to assassinate Nazi leaders by a group of Jewish U.S. soldiers coincides with a theatre owner's vengeful plans for the same.",  # Replace with actual description
            "genres": ["Horror", "Sci-Fi"],
            "cast": ["Brad Pitt", "Mèlanie Laurent", "Christoph Waltz", "Eli Roth"],
            "directors": ["Quentin Tarantino", "Eli Roth"],
            "languages": ["English", "Spanish"],
            "countries": ["USA", "Germany"],
            "type": "movie",
            "year": 2009,
        },
        {
            "id": "573a13aef29313caabd2c99e",
            "plot": "The intertwined stories of three Marines during America's battle with the Japanese in the Pacific during World War II.",
            "genres": ["Action", "Adventure", "Drama"],
            "cast": [
                "James Badge Dale",
                "Joseph Mazzello",
                "Jon Seda",
                "Sebastian Bertoli",
            ],
            "directors": ["Yo Mama"],
            "banner_url": "https://m.media-amazon.com/images/M/MV5BNmEwNmI1MjItNjNjYy00NDE5LWJiNTYtM2QxMTI5ZjllZTBhL2ltYWdlXkEyXkFqcGdeQXVyNTAyODkwOQ@@._V1_SY1000_SX677_AL_.jpg",
            "title": "The Pacific",
            "languages": ["English"],
            "year": 2010,
            "rating": 8.3,
            "countries": ["USA"],
            "type": "series",
        },
        {
            "id": "573a13b0f29313caabd342c5",
            "rating": 8.5,
            "year": 2006,
            "plot": "An undercover cop and a mole in the police attempt to identify each other while infiltrating an Irish gang in South Boston.",
            "genres": ["Crime", "Drama", "Thriller"],
            "title": "The Departed",
            "languages": ["English", "Cantonese"],
            "type": "movie",
            "banner_url": "https://m.media-amazon.com/images/M/MV5BMTI1MTY2OTIxNV5BMl5BanBnXkFtZTYwNjQ4NjY3._V1_SY1000_SX677_AL_.jpg",
            "countries": ["USA", "Hong Kong"],
            "cast": [
                "Leonardo DiCaprio",
                "Matt Damon",
                "Jack Nicholson",
                "Mark Wahlberg",
            ],
            "directors": ["Martin Scorsese"],
        },
        {
            "id": "573a13b5f29313caabd42722",
            "rating": 9,
            "year": 2008,
            "plot": "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, the caped crusader must come to terms with one of the greatest psychological tests of his ability to fight injustice.",
            "genres": ["Action", "Crime", "Drama"],
            "title": "The Dark Knight",
            "languages": ["English", "Mandarin"],
            "type": "movie",
            "poster": "https://m.media-amazon.com/images/M/MV5BMTMxNTMwODM0NF5BMl5BanBnXkFtZTcwODAyMTk2Mw@@._V1_SY1000_SX677_AL_.jpg",
            "countries": ["USA", "UK"],
            "cast": [
                "Christian Bale",
                "Heath Ledger",
                "Aaron Eckhart",
                "Michael Caine",
            ],
            "directors": ["Christopher Nolan"],
        },
        {
            "id": "573a13b5f29313caabd447f5",
            "rating": 8.1,
            "year": 2007,
            "plot": "Violence and mayhem ensue after a hunter stumbles upon a drug deal gone wrong and more than two million dollars in cash near the Rio Grande.",
            "genres": ["Crime", "Drama", "Thriller"],
            "title": "No Country for Old Men",
            "languages": ["English", "Spanish"],
            "type": "movie",
            "poster": "https://m.media-amazon.com/images/M/MV5BMjA5Njk3MjM4OV5BMl5BanBnXkFtZTcwMTc5MTE1MQ@@._V1_SY1000_SX677_AL_.jpg",
            "countries": ["USA"],
            "cast": [
                "Tommy Lee Jones",
                "Javier Bardem",
                "Josh Brolin",
                "Woody Harrelson",
            ],
            "directors": ["Ethan Coen", "Joel Coen"],
        },
    ]

    return {"id": search_id, "query": query, "result": dummy_data}


def get_user_history_insight_summary():
    window_size = 8
    chat_history = None  # Fetch the previous chat history
    return ""


def prepare_input(text: str, recommend_results=None):
    # or we can do even better, run a LLM in parallel that will give insight of the chat
    # note: if we implement this function then it will update some database time to time
    # after a certain batch of chat number is accumulated

    user_history_insight_summary = get_user_history_insight_summary()

    # prompt will have two types of mode
    # one will be a chat mode which is like more of a persuation mode
    # where as other will be reranking mode, which will directly affect the search re-rank

    system_prompt = (
        SYSTEM_PROMPT_FOR_RERANK if recommend_results else SYSTEM_PROMPT_FOR_SALES
    )

    if recommend_results:
        input_prompt = INPUT_TEMPLATE_FOR_RERANK.format(
            results=recommend_results or "", user_input=text
        )
    else:
        input_prompt = INPUT_TEMPLATE_FOR_SALES.format(
            user_input=text, chat_summary=user_history_insight_summary
        )

    return system_prompt, input_prompt
