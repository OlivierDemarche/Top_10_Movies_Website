import os
import requests
import pprint

# -----------------------------------------------------------------------
# ----------------------------- CONSTANT --------------------------------
# -----------------------------------------------------------------------
API_KEY = os.environ["tmdb_key"]
API_ENDPOINT = "https://api.themoviedb.org/3/search/movie"


# -----------------------------------------------------------------------
# ---------------------------- Functions --------------------------------
# -----------------------------------------------------------------------
def get_movies_from_api(title):
    parameters = {
        "api_key": API_KEY,
        "query": title
    }
    response = requests.get(url=API_ENDPOINT, params=parameters)
    data = response.json()["results"]
    pprint.pprint(data)
    return data


def find_selected_movie(movie_id):
    endpoint = f"https://api.themoviedb.org/3/movie/{movie_id}"
    parameters = {"api_key": API_KEY, "language": "en-US"}
    response = requests.get(endpoint, params=parameters)
    data = response.json()
    return data
