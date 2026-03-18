# import streamlit as st
# import joblib
# import requests

# def fetch_poster(movie_id):
#     try:
#         url = url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
#         data = requests.get(url).json()
#         poster_path = data.get("poster_path")
#         if poster_path:
#             return "https://image.tmdb.org/t/p/w500/" + poster_path
#     except Exception:
#         pass
#     return "https://via.placeholder.com/500x750?text=No+Poster+Available"

# # 1. Load the data once
# movies_df = joblib.load("movies.joblib")
# similarity = joblib.load("similarity.joblib")

# def recommend(movie):
#     # Search the DataFrame for the index of the movie
#     movie_index = movies_df[movies_df["title"] == movie].index[0]
#     distances = similarity[movie_index]
    
#     # Get the top 5 similar movies
#     recommendations_indices = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

#     recommended_movies = []
#     recommended_movies_posters = []
    
#     for i in recommendations_indices:
#         # FIX: Use ['id'] or check your actual column name here
#         # If 'movie_id' fails, try 'id'
#         try:
#             movie_id = movies_df.iloc[i[0]]['movie_id']
#         except KeyError:
#             movie_id = movies_df.iloc[i[0]]['id'] 
            
#         recommended_movies.append(movies_df.iloc[i[0]]['title'])
#         recommended_movies_posters.append(fetch_poster(movie_id))
        
#     return recommended_movies, recommended_movies_posters

# st.title("Movie Recommender System")

# # 2. Use the 'title' column for the dropdown
# selected_movie_name = st.selectbox(
#     "Select a movie to get recommendations:",
#     movies_df["title"].values
# )

# if st.button("Recommend"):
#     names, posters = recommend(selected_movie_name)
    
#     cols = st.columns(5) 
    
#     for i in range(5):
#         with cols[i]:
#             st.text(names[i])
#             st.image(posters[i])

import os
import joblib
import streamlit as st
import requests

# --- 1. SET UP PATHS ---
# This ensures Python looks in the same folder as this script for the files
BASE_PATH = os.path.dirname(__file__)
MOVIES_PATH = os.path.join(BASE_PATH, "movies.joblib")
SIMILARITY_PATH = os.path.join(BASE_PATH, "similarity.joblib")

# --- 2. LOAD DATA WITH CACHING ---
# Using @st.cache_resource prevents the app from reloading 
# heavy files every time you click a button.
@st.cache_resource
def load_data():
    if not os.path.exists(MOVIES_PATH) or not os.path.exists(SIMILARITY_PATH):
        st.error(f"Files not found! Make sure 'movies.joblib' and 'similarity.joblib' are in: {BASE_PATH}")
        st.stop()
    
    movies = joblib.load(MOVIES_PATH)
    similarity = joblib.load(SIMILARITY_PATH)
    return movies, similarity

movies, similarity = load_data()

# --- 3. HELPER FUNCTIONS ---
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        return "https://via.placeholder.com/500x750?text=No+Poster+Found"
    except Exception:
        return "https://via.placeholder.com/500x750?text=Network+Error"

def recommend(movie):
    # Get index of the selected movie
    index = movies[movies['title'] == movie].index[0]
    # Get similarity scores and sort them
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    
    recommended_movie_names = []
    recommended_movie_posters = []
    
    # Get top 5 recommendations (excluding the movie itself)
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].id
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))

    return recommended_movie_names, recommended_movie_posters

# --- 4. STREAMLIT UI ---
st.header('Movie Recommender System')

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    with st.spinner('Fetching recommendations...'):
        names, posters = recommend(selected_movie)
        
        cols = st.columns(5) 
        for i in range(5):
            with cols[i]:
                st.text(names[i])
                st.image(posters[i])