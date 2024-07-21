import pandas as pd
import numpy as np
import os
import streamlit as st
from transformers import pipeline

# Load preprocessed data
tv_df = pd.read_csv("C:/Users/Srijan/Movie-recommender-application/src/data/Preprocessed/tv_preprocessed.csv")
movies_df = pd.read_csv("C:/Users/Srijan/Movie-recommender-application/src/data/Preprocessed/movies_preprocessed.csv")

# Add 'age_appropriate' column based on 'adult' field
tv_df['age_appropriate'] = ~tv_df['adult']
movies_df['age_appropriate'] = ~movies_df['adult']

# Helper functions
def extract_unique_genres(df):
    genres = set()
    for genre_list in df['genre_names']:
        genres.update(eval(genre_list))  # Using eval to convert string representation of list back to list
    return list(genres)

def filter_by_genre(df, genres):
    return df[df['genre_names'].apply(lambda x: any(genre in eval(x) for genre in genres))]

def filter_by_popularity(df, threshold):
    return df[df['popularity'] >= threshold]

# Load similarity model once globally
similarity_model = pipeline('feature-extraction', model='sentence-transformers/paraphrase-MiniLM-L6-v2')

# Function to get similar overviews using Hugging Face's Transformers pipeline
def get_similar_overview(target_overview, candidates):
    target_embedding = similarity_model(target_overview)[0]
    candidate_embeddings = similarity_model(candidates)

    similarities = []
    for idx, candidate_embedding in enumerate(candidate_embeddings):
        similarity = np.inner(target_embedding, candidate_embedding[0]) / (np.linalg.norm(target_embedding) * np.linalg.norm(candidate_embedding[0]))
        similarities.append((similarity, candidates[idx]))

    similarities.sort(reverse=True, key=lambda x: x[0])
    return [overview for _, overview in similarities[:5]]

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
    if not favorite_series_overviews:
        st.warning("No favorite series selected. Please select at least one favorite series.")
        return pd.DataFrame()

    movie_overviews = filtered_movies_df['overview'].tolist()
    
    similar_overviews = []
    for target_overview in favorite_series_overviews:
        similar_overviews += get_similar_overview(target_overview, movie_overviews)
    
    # Get top N recommendations
    recommendations = filtered_movies_df[filtered_movies_df['overview'].isin(similar_overviews)].head(top_n)
    
    # Check for age-appropriateness and add warning if necessary
    for index, row in recommendations.iterrows():
        if not row['age_appropriate']:
            st.warning(f"The recommended movie '{row['title']}' might contain explicit content.")
    
    return recommendations

# Extract unique genres from both datasets
unique_genres = list(set(extract_unique_genres(tv_df) + extract_unique_genres(movies_df)))

# Streamlit interface
st.title('Movie Recommendation Based on TV Series Preferences')

# User inputs
user_language = st.selectbox('Select Language', tv_df['language'].unique())
user_genres = st.multiselect('Select Genres', unique_genres)
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
    if not recommendations.empty:
        st.write(recommendations[['title', 'overview', 'genre_names', 'popularity']])
    else:
        st.write("No recommendations found based on your preferences.")
