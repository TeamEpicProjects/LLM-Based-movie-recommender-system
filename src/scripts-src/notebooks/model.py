import streamlit as st
import pandas as pd
import os
from groq import Groq

import os
os.environ["GROQ_API_KEY"] = "your key"
client = Groq()

# Load preprocessed data
try:
    tv_df = pd.read_csv("C:/Users/Srijan/Movie-recommender-application/src/data/Preprocessed/tv_preprocessed.csv")
    movies_df = pd.read_csv("C:/Users/Srijan/Movie-recommender-application/src/data/Preprocessed/movies_preprocessed.csv")
except Exception as e:
    print("Error loading CSV files:", e)
    raise

# Debugging: Print the columns to check for 'overview' and 'adult'
print("Columns in tv_df:", tv_df.columns)
print("Columns in movies_df:", movies_df.columns)

# Check for 'adult' column and handle missing columns
if 'adult' not in tv_df.columns:
    tv_df['adult'] = False  # Assuming False as default if 'adult' column is missing

if 'adult' not in movies_df.columns:
    movies_df['adult'] = False  # Assuming False as default if 'adult' column is missing

# Add 'age_appropriate' column based on 'adult' field
tv_df['age_appropriate'] = ~tv_df['adult']
movies_df['age_appropriate'] = ~movies_df['adult']

# Ensure 'overview' column exists
if 'overview' not in tv_df.columns:
    raise KeyError("'overview' column is missing from tv_df")
if 'overview' not in movies_df.columns:
    raise KeyError("'overview' column is missing from movies_df")

# Initialize the Groq LLaMA model
client = Groq(
    # This is the default and can be omitted
    api_key=os.environ.get("GROQ_API_KEY"),
)

def generate_recommendations(favorite_series_overviews):
    prompt = "I love these TV shows and the following are their overviews: " + ", ".join(favorite_series_overviews) + ". Can you recommend some movies based on these overviews?"
    
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "you are a helpful assistant."
            },
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama3-8b-8192",
    )
    
    return chat_completion.choices[0].message.content

# Function to get recommendations based on user input
def recommend_movies(user_preferences):
    favorite_series = user_preferences.get('favorite_series', [])
    favorite_series_overviews = tv_df[tv_df['name'].isin(favorite_series)]['overview'].tolist()
    
    if not favorite_series_overviews:
        return "No recommendations found based on your preferences."
    
    recommendations = generate_recommendations(favorite_series_overviews)
    return recommendations

# Streamlit interface
st.title('Movie Recommendation Based on TV Series Preferences')

# User inputs
user_language = st.selectbox('Select Language', tv_df['language'].unique())
user_genres = st.multiselect('Select Genres', tv_df['genre_names'].apply(eval).explode().unique())
user_popularity_threshold = st.slider('Select Popularity Threshold', 1, 10, 5)
user_favorite_series = st.multiselect('Select Your Favorite TV Series', tv_df['name'].unique())

if st.button('Recommend Movies'):
    user_preferences = {
        'language': user_language,
        'genres': user_genres,
        'popularity_threshold': user_popularity_threshold * 1000,  # Adjusting scale to match dataset
        'favorite_series': user_favorite_series
    }
    recommendations = recommend_movies(user_preferences)
    st.write(recommendations)