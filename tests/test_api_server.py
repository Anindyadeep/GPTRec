import uuid
import requests

# Import the functions or code snippets you want to test

BASE_URL = "https://92b2-203-192-244-60.ngrok-free.app" # "http://0.0.0.0:8000"

# Define the endpoint URLs
RECOMMEND_URL = f"{BASE_URL}/api/v1/recommend"
MOVIES_URL = f"{BASE_URL}/api/v1/movies"
MOVIE_DETAILS_URL = f"{BASE_URL}/api/v1/movie/573a13f6f29313caabde514d"

# Define payloads and parameters for testing
RECOMMEND_PAYLOAD = {
    "id": str(uuid.uuid4()),
    "query": "jedi and sith war, movie by george lucas, released around 2004",
}
MOVIES_PARAMS = {
    "page": 6,
    "page_size": 10
}



def test_recommend_api():
    response = requests.post(RECOMMEND_URL, json=RECOMMEND_PAYLOAD)
    assert response.status_code == 200

def test_movies_api():
    response = requests.get(MOVIES_URL, params=MOVIES_PARAMS)
    assert response.status_code == 200

def test_movie_details_api():
    response = requests.get(MOVIE_DETAILS_URL)
    assert response.status_code == 200
