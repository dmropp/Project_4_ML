from flask import Flask, render_template, request, jsonify
import sqlite3
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import random
from joblib import Parallel, delayed

app = Flask(__name__)

# Connect to the SQLite database
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
    if movie_title not in user_movie_ratings.columns:
        return []  # Return an empty list if the movie has no ratings

    movie_ratings = user_movie_ratings[movie_title].values.reshape(1, -1)

    # Calculate similarity scores using dot product
    similar_scores = np.dot(movie_ratings, movie_similarity)

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

# Initialize variables to keep track of liked movies
liked_movies = []
max_likes = 5  # Set the maximum number of liked movies

# Function to get random movie for rating
def get_random_movie():
    return df.sample(1).iloc[0]

# Routes
@app.route('/')
def index():
    global liked_movies
    if len(liked_movies) < max_likes:
        random_movie = get_random_movie()
        return render_template('index.html', random_movie=random_movie)
    else:
        return "You have reached the maximum number of liked movies. Check your recommendations!"

@app.route('/rate_movie', methods=['POST'])
def rate_movie():
    global liked_movies
    movie_id = request.form['movie_id']
    feedback = request.form['feedback']  # Change 'rating' to 'feedback'

    # Here you can save the user's feedback to the database if needed
    # For simplicity, let's just print the movie ID and feedback
    print(f"User provided feedback for Movie ID {movie_id}: {feedback}")

    # Add the movie to the liked movies list if feedback is 'like'
    if feedback == 'like':
        liked_movies.append(movie_id)

    # Get another random movie for the user to provide feedback
    if len(liked_movies) < max_likes:
        random_movie = get_random_movie()
        return jsonify({'random_movie': random_movie.to_dict()})

    else:
        # Provide recommendations when the user reaches the maximum liked movies
        hybrid_recommendations = get_hybrid_recommendations(liked_movies, top_n=5)
        return jsonify({'recommendations': hybrid_recommendations})

if __name__ == '__main__':
    conn.close()
    app.run(debug=True)