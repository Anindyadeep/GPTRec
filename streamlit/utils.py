import os 
import requests
import streamlit as st
from typing import List 


def fetch_poster(movie_id):
    # Helper function to get posters from TMDB, will be helpful later
    api_key = os.environ.get("TMDB_API_KEY")
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}')
    data = response.json()
    print(data)
    return "https://image.tmdb.org/t/p/w500/" + data["poster_path"]


def fetch_recommendation(ids: List[int], names: List[str], links: List[str]) -> None:
    assert len(ids) == len(names) == len(links), ValueError("Length of ids, names and links should be same")
    num_recommendations, cols = len(ids), st.columns(len(ids))
    for i in range(num_recommendations):
        with cols[i]:
            st.write(f' <b style="color:#E50914"> {names[i]} </b>',unsafe_allow_html=True)
            st.image(links[i])
            st.write('<b style="color:#DB4437">Rating</b>:<b> 0.99 </b>',unsafe_allow_html=True)


def dummy_recommend(text: str):
    # right now going for a dummy recommendation
    dummy_data = {
        "ids": [50357, 228326, 16911, 27579, 679],
        "names": [
            "Apollo 18",
            "The Book of Life",
            "The Inhabited Island",
            "The American",
            "Aliens",
        ],
        "links": [
            "https://image.tmdb.org/t/p/w500//oW6oUKY2oiQbynwllFboYscVzct.jpg",
            "https://image.tmdb.org/t/p/w500//aotTZos5KswgCryEzx2rlOjFsm1.jpg",
            "https://image.tmdb.org/t/p/w500//hG2PDKqPZwwC1MTDig3pbTkmXm4.jpg",
            "https://image.tmdb.org/t/p/w500//5OEOsRaBsSxD0qBtAhus0iKDzr.jpg",
            "https://image.tmdb.org/t/p/w500//r1x5JGpyqZU8PYhbs4UcrO1Xb6x.jpg",
        ],
    }

    st.text("Here are few Recommendations..")
    fetch_recommendation(ids=dummy_data["ids"], names=dummy_data["names"], links=dummy_data["links"])
    st.text("From your history.")
    fetch_recommendation(ids=dummy_data["ids"], names=dummy_data["names"], links=dummy_data["links"])

def search():
    expander = st.expander("Tap to Select a Movie  🌐️")
    move_text_box = expander.text_area(
        label="What kind of movie you are planing to watch"
    )

    if expander.button("recommend"):
        dummy_recommend(text=move_text_box)
    

def chat():    
    #with st.container(height=800):
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            response = st.write("Hi hi")
        st.session_state.messages.append({"role": "assistant", "content": response})
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])