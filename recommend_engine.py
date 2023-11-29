# import our dependencies
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import tensorflow as tf

import pandas as pd
import numpy as np
import datetime as dt

import sqlite3
import sqlalchemy as db
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify, render_template, request

import warnings
warnings.filterwarnings('ignore')
import requests

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from difflib import get_close_matches

#########################
con = sqlite3.connect("movie_ratings_db.sqlite")
links_df = pd.read_sql_query("SELECT * FROM Links", con)
movies_df = pd.read_sql_query("SELECT * FROM Movies", con)
ratings_df = pd.read_sql_query("SELECT * FROM Ratings", con)
tags_df = pd.read_sql_query("SELECT * FROM Tags", con)

# genre split, encode as categorical
genres_split = movies_df['genres'].str.get_dummies('|')
movies_encoded = pd.concat([movies_df, genres_split], axis=1)
movies_encoded.drop('genres', axis=1, inplace=True)

# prep tags_df, ratings_df
tags_df = tags_df.drop(columns='timestamp')
ratings_df = ratings_df.drop(columns='timestamp')

# rewrite for ratings only
tags_ratings_df = pd.merge(tags_df, ratings_df, on='userId', how='left')

@app.route('/', methods=['GET'])  # route to display the Home Page
@cross_origin()
def home():
    return render_template('index.html')


@app.route('/', methods=['POST', 'GET'])  # route to show the recommendation in web UI
@cross_origin()
# This function take movie name from user, and return 10 similar type of movies.
def recommendation():
    if request.method == 'POST':
        try:
            # reading the inputs given by the user
            title = request.form['search']
            title = title.lower()
            # create count matrix from this new combined column
            cv = CountVectorizer()
            count_matrix = cv.fit_transform(df['comb'])

            # now compute the cosine similarity
            cosine_sim = cosine_similarity(count_matrix)

            # correcting user input spell (close match from our movie list)
            correct_title = get_close_matches(title, movie_list, n=3, cutoff=0.6)[0]

            # get the index value of given movie title
            idx = df['movie_title'][df['movie_title'] == correct_title].index[0]

            # get the pairwise similarity scores of all movies with that movie
            sim_score = list(enumerate(cosine_sim[idx]))

            # sort the movie based on similarity scores
            sim_score = sorted(sim_score, key=lambda x: x[1], reverse=True)[0:15]

            # suggested movies are storing into a list
            suggested_movie_list = []
            for i in sim_score:
                movie_index = i[0]
                suggested_movie_list.append(df['movie_title'][movie_index])

            # calling get_poster_link function to fetch their title and poster link.
            poster_title_link = get_poster_link(suggested_movie_list)
            return render_template('recommended.html', output=poster_title_link)

        except:
            return 


if __name__ == '__main__':
    print("App is running")
    app.run(debug=True)