import warnings
warnings.filterwarnings("ignore")

import numpy as np
import datetime as dt
import os

import sqlite3

import sqlalchemy as db
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify, render_template, request, session, redirect, url_for

import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors
import numpy as np
import random
from joblib import Parallel, delayed

engine = create_engine("sqlite:///movie_ratings_db.sqlite")

conn = sqlite3.connect('movie_ratings_db.sqlite')

# Query a subset of the data to speed up development/testing
# Adjust the LIMIT clause based on your dataset size
query = """
    SELECT r.userId, r.movieId, r.rating, m.title, m.genres
    FROM ratings r
    JOIN movies m ON r.movieId = m.movieId
    LIMIT 10000  -- Adjust this limit based on your dataset size
"""
df = pd.read_sql_query(query, conn)

# Assuming the genres column is in the format "Genre1|Genre2|Genre3"
# Convert genres into a list
df['genres'] = df['genres'].str.split('|')

# Content-Based Filtering (using Genres)
df['genres_str'] = df['genres'].apply(lambda x: ' '.join(x))
tfidf_vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)  # Adjust max_features
tfidf_matrix = tfidf_vectorizer.fit_transform(df['genres_str'])

# Approximate Nearest Neighbors with NearestNeighbors
nn = NearestNeighbors(n_neighbors=5, algorithm='auto', metric='cosine')
nn.fit(tfidf_matrix)

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route("/")
def welcome():
    return render_template("index.html")

@app.route("/genre")
def genre():
    return render_template("reregenre.html")

@app.route("/random")
def random_movie():
    return render_template("random.html")

@app.route("/title")
def title():
    return render_template("reretitle.html")

# Counter to keep track of the number of movie selections
selection_counter = 0

@app.route("/recommendation_engine", methods=['GET', 'POST'])
def rec_engine():
    global result
    global selection_counter

    if request.method == 'POST':
        selected_movies = request.form.getlist('selected_movies')

    # Collaborative Filtering (User-Item Interactions)
    user_movie_ratings = df.pivot_table(index='userId', columns='title', values='rating', fill_value=0)
    movie_user_ratings = user_movie_ratings.T
    movie_similarity = cosine_similarity(movie_user_ratings)

    # Function to get similar items based on NearestNeighbors
    def get_similar_items_nn(movie_index):
        distances, indices = nn.kneighbors(tfidf_matrix[movie_index])
        similar_items = df.iloc[indices[0]]['title'].tolist()
        return similar_items

    # Function to get similar items based on Collaborative Filtering
    def get_similar_items_cf(movie_title, top_n=5):
        movie_ratings = user_movie_ratings[movie_title].values.reshape(1, -1)

        # Calculate similarity scores using cosine_similarity
        similar_scores = cosine_similarity(movie_ratings, movie_user_ratings)

        # Extract the similarity scores for the given movie
        similarity_scores_for_movie = similar_scores.flatten()

        # Create a DataFrame with movie titles and similarity scores
        similar_movies_df = pd.DataFrame({'movie': movie_user_ratings.index, 'similarity': similarity_scores_for_movie})

        # Sort by similarity and get the top N
        similar_movies_df = similar_movies_df.sort_values(by='similarity', ascending=False).head(top_n)

        return similar_movies_df['movie'].tolist()

    # Function to get hybrid recommendations (combining CF and CB)
    def get_hybrid_recommendations(selected_movies, top_n=5):
        cf_recommendations = Parallel(n_jobs=-1)(delayed(get_similar_items_cf)(movie_title, top_n=top_n) for movie_title in selected_movies)
        cf_recommendations = [item for sublist in cf_recommendations for item in sublist]

        cb_recommendations = Parallel(n_jobs=-1)(delayed(get_similar_items_nn)(df[df['title'] == movie_title].index[0]) for movie_title in selected_movies)
        cb_recommendations = [item for sublist in cb_recommendations for item in sublist]

        genre_filter = set().union(*(tuple(genre) for movie_title in selected_movies for genre in df[df['title'] == movie_title]['genres']))
        cb_recommendations_filtered = [movie for movie in cb_recommendations if any(set(genre) & genre_filter for genre in df[df['title'] == movie]['genres'])]

        hybrid_recommendations = list(set(cf_recommendations + cb_recommendations_filtered))[:top_n]

        return hybrid_recommendations

    # Function to allow the user to choose movies from a random list
    def choose_movies():
        random_movies = random.sample(df['title'].tolist(), 10)
        return random_movies

    # Function to allow the user to redraw recommendations
    def redraw_recommendations():
        selected_movies = choose_movies()
        hybrid_recommendations = get_hybrid_recommendations(selected_movies, top_n=5)
        global result
        result = hybrid_recommendations.copy()
        print(f'Hybrid recommendations based on user-selected movies:\n{hybrid_recommendations}')
        
        # Commenting out user input code for now to simplify app
        # while True:
        #     selected_movies = choose_movies()
        #     hybrid_recommendations = get_hybrid_recommendations(selected_movies, top_n=5)
        #     global result
        #     result = hybrid_recommendations.copy()
        #     print(f'Hybrid recommendations based on user-selected movies:\n{hybrid_recommendations}')

        #     redraw = input("Do you want to redraw recommendations? Enter 'yes' or 'no': ").lower()
        #     if redraw != 'yes':
        #         break
    
    if 'like_counter' not in session:
        session['like_counter'] = 0

    if request.method == 'POST':
        action = request.form.get('action')
        if action in ['like', 'dislike', 'skip', 'unsure']:
            # Handle the user's action (like, dislike, skip, unsure)
            # Update user preferences or store data accordingly

            if action == 'like':
                session['like_counter'] += 1

            # Increment the selection counter
            selection_counter += 1

            # If the user has liked 5 movies, generate recommendations
            if session['like_counter'] == 5:
                # Call the function to start the recommendation process
                redraw_recommendations()
                # Reset the like counter
                session['like_counter'] = 0
                # https://stackoverflow.com/questions/48148131/how-can-we-call-one-route-from-another-route-with-parameters-in-flask
                # Referenced for how to use redirect
                return redirect(url_for("movie_recs"))


    # If the user has not liked 5 movies, continue choosing movies
    if session['like_counter'] < 5:
        random_movie = df['title'].sample().iloc[0]
        # https://www.geeksforgeeks.org/flask-rendering-templates/#, referenced for rendering variables in HTML using Jinja
        return render_template("rec_engine_interactive.html", movie_title=random_movie, like_counter=session['like_counter'])    

@app.route("/recommended_movies")
def movie_recs():
    return render_template("rec_engine.html", recs=result)

if __name__ == "__main__":
    app.run(debug=True)
