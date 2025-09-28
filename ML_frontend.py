# import streamlit as st
# import pickle
# import pandas as pd
# import requests

# # OMDb API key
# OMDB_API_KEY = "842f87eb"

# def fetch_poster(movie_title):
#     """Fetch poster using OMDb API with movie title"""
#     url = f"http://www.omdbapi.com/?t={movie_title}&apikey={OMDB_API_KEY}"
#     response = requests.get(url)
#     data = response.json()
#     poster_url = data.get("Poster")
#     if poster_url and poster_url != "N/A":
#         return poster_url
#     else:
#         return None

# # Streamlit app
# st.title("🎬 Movie Recommender System")

# # Load data
# movies_dict = pickle.load(open("movie_dict.pkl", "rb"))
# movies = pd.DataFrame(movies_dict)
# similarity = pickle.load(open("similarity.pkl", "rb"))

# # Dropdown to select movie
# selected_movie_name = st.selectbox(
#     "Select a movie:",
#     movies["title"].values
# )

# # Recommend button
# if st.button("Recommend"):
#     movie_index = movies[movies["title"] == selected_movie_name].index[0]
#     distances = similarity[movie_index]
#     movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

#     st.subheader("Recommended Movies:")

# # Create 5 columns (since we recommend 5 movies)
#     cols = st.columns(5)

#     for idx, i in enumerate(movies_list):
#         movie_title = movies.iloc[i[0]].title
#         poster_url = fetch_poster(movie_title)
#         with cols[idx]:
#             if poster_url:
#                 st.image(poster_url, caption=movie_title, use_container_width=True)
#             else:
#                 st.write(movie_title)
#                 st.write("Poster not available")

import streamlit as st
import pickle
import pandas as pd
import requests

# OMDb API key
OMDB_API_KEY = "842f87eb"

def fetch_movie_details(movie_title):
    """Fetch movie poster, rating, and year using OMDb API"""
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey={OMDB_API_KEY}"
    response = requests.get(url)
    data = response.json()
    
    poster_url = data.get("Poster") if data.get("Poster") != "N/A" else None
    rating = data.get("imdbRating", "N/A")
    year = data.get("Year", "N/A")
    
    return poster_url, rating, year

# Streamlit app
st.title("🎬 Movie Recommender System")

# Load data
movies_dict = pickle.load(open("movie_dict.pkl", "rb"))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open("similarity.pkl", "rb"))

# Dropdown to select movie
selected_movie_name = st.selectbox(
    "Select a movie:",
    movies["title"].values
)

# Recommend button
if st.button("Recommend"):
    movie_index = movies[movies["title"] == selected_movie_name].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    st.subheader("Recommended Movies:")
    cols = st.columns(5)

    for idx, i in enumerate(movies_list):
        movie_title = movies.iloc[i[0]].title
        poster_url, rating, year = fetch_movie_details(movie_title)

        with cols[idx]:
            if poster_url:
                st.image(poster_url, caption=movie_title, use_container_width=True)
            else:
                st.write(movie_title)
            
            st.markdown(f"⭐ **IMDb:** {rating}")
            st.markdown(f"📅 **Year:** {year}")
