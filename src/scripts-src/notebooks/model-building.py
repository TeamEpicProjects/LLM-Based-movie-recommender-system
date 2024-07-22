import pandas as pd
import numpy as np
import os
import groq
import streamlit as st

# Load preprocessed data
tv_df = pd.read_csv("C:/Users/Srijan/Movie-recommender-application/src/data/Preprocessed/tv_preprocessed.csv")
movies_df = pd.read_csv("C:/Users/Srijan/Movie-recommender-application/src/data/Preprocessed/movies_preprocessed.csv")

# Helper functions
def filter_by_genre(df, genres):
    return df[df['genre_names'].apply(lambda x: any(genre in x for genre in genres))]

def filter_by_popularity(df, threshold):
    return df[df['popularity'] >= threshold]

groq.api_key = 'your key'

def get_similar_overview(target_overview, candidates):
    prompt = f"Find the closest matching overviews to: {target_overview}\n\nCandidates:\n" + "\n".join(candidates)
    response = groq.Completion.create(
        model="llama3-8b-8192",
        prompt=prompt,
        max_tokens=1024
    )
    return response['choices'][0]['text'].strip().split('\n')

def recommend_movies(user_preferences, top_n=5):
    # Layered filtering
    filtered_tv_df = tv_df[
        (tv_df['age_appropriate']) &
        (tv_df['language'] == user_preferences['language']) &
        (tv_df['popularity'] >= user_preferences['popularity_threshold'])
    ]
    filtered_tv_df = filter_by_genre(filtered_tv_df, user_preferences['genres'])
    
    filtered_movies_df = movies_df[
        (movies_df['age_appropriate']) &
        (movies_df['language'] == user_preferences['language']) &
        (movies_df['popularity'] >= user_preferences['popularity_threshold'])
    ]
    filtered_movies_df = filter_by_genre(filtered_movies_df, user_preferences['genres'])
    
    # LLM-based similarity
    favorite_series_overviews = tv_df[tv_df['name'].isin(user_preferences['favorite_series'])]['overview'].tolist()
    movie_overviews = filtered_movies_df['overview'].tolist()
    
    similar_overviews = []
    for target_overview in favorite_series_overviews:
        similar_overviews += get_similar_overview(target_overview, movie_overviews)
    
    # Get top N recommendations
    recommendations = filtered_movies_df[filtered_movies_df['overview'].isin(similar_overviews)].head(top_n)
    return recommendations

# Streamlit interface
st.title('Movie Recommendation Based on TV Series Preferences')

# User inputs
user_language = st.selectbox('Select Language', tv_df['language'].unique())
user_genres = st.multiselect('Select Genres', tv_df['genre_names'].explode().unique())
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
    st.write(recommendations[['title', 'overview', 'genre_names', 'popularity']])