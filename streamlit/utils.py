import os
import json
import requests
import streamlit as st
from typing import Iterable
from dotenv import load_dotenv

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


def fetch_recommendation(response) -> None:

    cols = st.columns(len(response))
    for i in range(len(cols)):
        with cols[i]:
            st.write(
                f' <b style="color:#E50914"> {response[i]["name"]} </b>', unsafe_allow_html=True
            )
            st.image(response[i]["link"])
            st.write(
                '<b style="color:#DB4437">Rating</b>:<b> 0.99 </b>',
                unsafe_allow_html=True,
            )


def dummy_recommend(text: str):
    # right now going for a dummy recommendation
    dummy_response = requests.post(
        url=f"{os.environ.get('SERVER_URL')}/api/v1/recommend",
        json={"query": text}
    ).json()

    dummy_data = dummy_response["search_results"]["result"]

    st.text("Here are few Recommendations..")
    fetch_recommendation(response=dummy_data)

    st.text("From your history.")
    fetch_recommendation(response=dummy_data)


def search():
    expander = st.expander("Tap to Select a Movie  🌐️")
    move_text_box = expander.text_area(
        label="What kind of movie you are planing to watch"
    )

    if expander.button("recommend"):
        dummy_recommend(text=move_text_box)


def chat():
    if prompt := st.chat_input("Ask me about movies"):
        with st.chat_message("user"):
            st.markdown(prompt)
        
        def stream() -> Iterable:
            response = requests.post(
                url=f"{os.environ.get('SERVER_URL')}/api/v1/chat",
                json={"query": prompt},
                stream=True
            )
            for line in response.iter_lines():
                if line:
                    yield json.loads(line.decode("utf-8"))["text"]

        with st.chat_message("ai"):
            st.write_stream(stream)