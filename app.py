import streamlit as st
import pickle
import pandas as pd
import requests

# Load data
movies = pickle.load(open('/Users/thakur/Downloads/Movie-Recommender-System-Using-Machine-Learning-master/artifacts/movie_list.pkl', 'rb'))
similarity = pickle.load(open('/Users/thakur/Downloads/Movie-Recommender-System-Using-Machine-Learning-master/artifacts/similarity.pkl', 'rb'))

# Convert to DataFrame if needed
if isinstance(movies, list):
    movies = pd.DataFrame(movies)

# TMDb API Key
API_KEY = "c730c6819eecf7df47e2b6f57363a2f2"

# Fetch movie poster using TMDb API
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            return "https://via.placeholder.com/500x750?text=No+Image"
    except requests.exceptions.RequestException as e:
        print(f"Error fetching poster: {e}")
        return "https://via.placeholder.com/500x750?text=No+Image"

# Recommend function
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movie_names = []
    recommended_movie_posters = []

    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))

    return recommended_movie_names, recommended_movie_posters

# Streamlit UI
st.set_page_config(layout="wide")
st.title("🎬 Movie Recommender System")

selected_movie = st.selectbox("Type or select a movie from the dropdown", movies['title'].values)

if st.button("Recommend"):
    names, posters = recommend(selected_movie)

    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])
