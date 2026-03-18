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

import joblib
import streamlit as st
import requests

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    try:
        # Set a timeout so the app doesn't hang forever (e.g., 5 seconds)
        response = requests.get(url, timeout=5)
        response.raise_for_status() # Check if the request was successful
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        return "https://via.placeholder.com/500x750?text=No+Poster+Found"
    except Exception as e:
        # If there's a timeout or connection error, return a placeholder image
        return "https://via.placeholder.com/500x750?text=Network+Error"

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters


st.header('Movie Recommender System')
movies = joblib.load("movies.joblib")
similarity = joblib.load("similarity.joblib")

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
    
    cols = st.columns(5) 
    
    for i in range(5):
        with cols[i]:
            st.text(recommended_movie_names[i])
            st.image(recommended_movie_posters[i])
            
