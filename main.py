import pickle
import streamlit as st
import requests
import time

def fetch_poster(movie_id, max_retries=3):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=68b3cfc303a616245b1205eece27375f&language=en-US".format(movie_id)
    retries = 0
    while retries < max_retries:
        try:
            data = requests.get(url)
            data.raise_for_status()  # Raise an HTTPError for bad responses
            data = data.json()
            poster_path = data['poster_path']
            full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
            return full_path
        except requests.exceptions.RequestException as e:
            retries += 1
            print(f"Error fetching poster data (attempt {retries}): {e}")
            time.sleep(1)  # Wait for a moment before retrying
    print("Max retries reached. Unable to fetch poster data.")
    return None


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters

# Load pickled data
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.header('Movie Recommender System')

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    num_columns = 5
    cols = st.columns(num_columns)

    for i in range(num_columns):
        with cols[i]:
            st.text(recommended_movie_names[i])
            st.image(recommended_movie_posters[i])
