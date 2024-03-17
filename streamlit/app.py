import requests
import streamlit as st
from utils import search, chat

st.set_page_config(layout="wide")
st.header("GPT4Rec")

with st.sidebar:
    chat()

search()