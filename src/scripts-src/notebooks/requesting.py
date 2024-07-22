import requests
import json
import os

# Your TMDb API key
api_key = '58e058ef203e8d708105781819ad424c'

# Base URL for TMDb API
base_url = 'https://api.themoviedb.org/3'

# Endpoints for movies and TV shows
movie_endpoint = f'{base_url}/movie/popular'
tv_endpoint = f'{base_url}/tv/popular'
genres_endpoint = f'{base_url}/genre/movie/list'

# Parameters for the API request
params = {
    'api_key': api_key,
    'language': 'en-US',
    'page': 1
}

# Maximum number of pages to fetch to prevent overflow
MAX_PAGES = 20

# Function to fetch all pages of data
def fetch_all_pages(endpoint, params, max_pages=MAX_PAGES):
    all_results = []
    page = 1
    while page <= max_pages:
        params['page'] = page
        response = requests.get(endpoint, params=params)
        if response.status_code != 200:
            print(f"Error fetching page {page}: {response.status_code}")
            break
        data = response.json()
        if 'results' not in data:
            break
        results = data['results']
        if not results:
            break
        all_results.extend(results)
        page += 1
        if page > data.get('total_pages', max_pages):
            break
    return all_results

# Function to fetch genre names for a list of genre IDs
def get_genre_names(genre_ids, genre_dict):
    genre_names = [genre_dict.get(id, "Unknown") for id in genre_ids]
    return genre_names

# Fetch genres (one-time fetch)
genres_response = requests.get(genres_endpoint, params={'api_key': api_key, 'language': 'en-US'})
genres_data = genres_response.json()
print("Genres Response Data:", genres_data)  # Debug print to check the structure
genre_dict = {genre["id"]: genre["name"] for genre in genres_data.get("genres", [])}

# Fetch all popular movies
movies = fetch_all_pages(movie_endpoint, params)

# Process movie data
for movie in movies:
    genre_ids = movie.get('genre_ids', [])  # Handle missing 'genre_ids' key
    movie['genre_names'] = get_genre_names(genre_ids, genre_dict)

# Fetch all popular TV shows
tv_shows = fetch_all_pages(tv_endpoint, params)

# Process TV show data (similar to movies)
for tv_show in tv_shows:
    genre_ids = tv_show.get('genre_ids', [])
    tv_show['genre_names'] = get_genre_names(genre_ids, genre_dict)

# Define the directory to save the data
data_dir = 'src\data'

# Ensure the directory exists
if not os.path.exists(data_dir):
    print(f"Creating directory: {data_dir}")
    os.makedirs(data_dir, exist_ok=True)

# Save data to JSON files in the specified directory
movies_path = os.path.join(data_dir, 'movies.json')
tv_shows_path = os.path.join(data_dir, 'tv_shows.json')

print(f"Saving movies to {movies_path}")
with open(movies_path, 'w') as movie_file:
    json.dump(movies, movie_file, indent=4)

print(f"Saving TV shows to {tv_shows_path}")
with open(tv_shows_path, 'w') as tv_file:
    json.dump(tv_shows, tv_file, indent=4)

print('Data fetched and saved to ../data/movies.json and ../data/tv_shows.json with genre names!')
