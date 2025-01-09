import requests

API_KEY = "84822b92"  # Replace with your OMDb API key
BASE_URL = "http://www.omdbapi.com/"

def fetch_movie_by_title(title):
    """
    Fetch movie data from OMDb API by title.
    :param title: Title of the movie to fetch.
    :return: Dictionary containing basic movie details or error message.
    """
    params = {
        "apikey": API_KEY,
        "t": title,  # 't' parameter specifies the movie title
        "plot": "full"
    }
    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        if data.get("Response") == "True":  # Check if the movie was found
            # Extract required fields
            return {
                "name": data.get("Title"),
                "year": data.get("Year"),
                "description": data.get("Plot"),
                "poster": data.get("Poster")
            }
        else:
            return {"error": "Movie not found"}
    else:
        return {"error": f"Failed to fetch data. Status code: {response.status_code}"}
