import joblib
import requests
import streamlit as st
import pandas as pd
from compress_pickle import create_compress_file
import os

# for fetching API for movies poster

# Importing dataset

if not os.path.exists("data_dict_compressed.pkl"):
    create_compress_file()

data_dict = joblib.load("data_dict_compressed.pkl")
data = pd.DataFrame(data_dict)

# Getting list of movies titles from dataset
movies_list = data.title.values

# Web page interface
st.title('Movie Recommender System')

selected_movie = st.selectbox(
    "List of Movies",
    movies_list,
)

similarity = joblib.load("similarity.pkl")


def fetch_poster(movie_id):
    response =  requests.get("https://api.themoviedb.org/3/movie/{}?api_key=f1f911a959578e0925d9a1924f3b8b14".format(movie_id))
    poster5 = response.json()

    return "https://image.tmdb.org/t/p/original" + poster5["poster_path"]


# function for recommendation
def recommend(movie):
    """
    First finds the index of movie in the dataset that is given, then find it's similarity and look for the movies
    that has highest similarity value by using sort and then loop throughs it..
    """
    movie_index = data[data.title == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended = []
    recommended_movies_poster = []
    for i in movie_list:
        movie_id = data.movie_id[i[0]]

        recommended.append(data.title[i[0]])
        # Fetch movie poster from API
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended, recommended_movies_poster




if st.button("Recommend"):
    names, posters = recommend(selected_movie)
    col =  st.columns(5)

    # with col1:
    #     st.header(names[0])
    #     st.image(posters[0])
    #
    # with col2:
    #    st.header(names[1])
    #    st.image(posters[1])
    #
    # with col3:
    #    st.header(names[2])
    #    st.image(posters[2])

    for i in range(5):
        with col[i]:
            st.text(names[i])
            st.image(posters[i])



