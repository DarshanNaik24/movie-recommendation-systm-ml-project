import streamlit as st
import pickle
import pandas as pd
import requests

st.markdown("""
    <style>
        /* Set background image with blur and transparency */
        .stApp {
            background: url("https://wallpapercave.com/wp/wp1945898.jpg") no-repeat center center fixed;
            background-size: cover;
            backdrop-filter: blur(9px); /* Apply blur to background */
        }

        /* Add a semi-transparent layer over background */
        .stApp::before {
            content: "";
            position: fixed;
            top: 0;
            left: 0;
            height: 100%;
            width: 100%;
            background-color: rgba(255, 255, 255, 0.3);  /* Semi-transparent white overlay */
            z-index: -1;
            backdrop-filter: blur(5px); /* Adjust blur strength */
        }
    </style>
""", unsafe_allow_html=True)

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8c2ef4c76dafcf488e32c36d6111d43a&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

movies_dict=pickle.load(open('movies_dict.pkl','rb'))
movies=pd.DataFrame(movies_dict)

similarity=pickle.load(open('similarity.pkl','rb'))

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]

    recommended_movies=[]
    recommended_movies_posters=[]

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)

        #fetch the movie posters
        recommended_movies_posters.append(fetch_poster(movie_id))


    return recommended_movies,recommended_movies_posters


st.markdown("<h1 style='color: black;'>Movie Recommender System</h1>", unsafe_allow_html=True)

st.markdown("<p style='font-size:20px; font-weight:bold; color:black;'>Get the Selected Similar Movies</p>", unsafe_allow_html=True)
selected_movie_name = st.selectbox('', movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown(f"<h4 style='color: black;'>{names[0]}</h4>", unsafe_allow_html=True)
        st.image(posters[0])
    with col2:
        st.markdown(f"<h4 style='color: black;'>{names[1]}</h4>", unsafe_allow_html=True)
        st.image(posters[1])
    with col3:
        st.markdown(f"<h4 style='color: black;'>{names[2]}</h4>", unsafe_allow_html=True)
        st.image(posters[2])
    with col4:
        st.markdown(f"<h4 style='color: black;'>{names[3]}</h4>", unsafe_allow_html=True)
        st.image(posters[3])
    with col5:
        st.markdown(f"<h4 style='color: black;'>{names[4]}</h4>", unsafe_allow_html=True)
        st.image(posters[4])

