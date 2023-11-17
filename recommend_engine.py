# import dependencies
## flask interaction
from flask import Flask, request, render_template
from flask_cors import cross_origin
## data pre-process
from sklearn.feature_extraction.text import CountVectorizer
## get route attribution
from difflib import get_close_matches
## TEMP MODEL LOADING
from sklearn.externals import joblib

import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify, request
import datetime as dt


def preprocess(movie_cart):
    # convert chosen movies into a feature vector
    vectorizer = CountVectorizer()
    movie_features = vectorizer.fit_transform(movie_cart)
    return movie_features

movie_cart=[]

@app.route('/', methods=['POST', 'GET'])
def recommendation():
    if request.method == 'POST':
        try:
            # reading the inputs given by the user
            # indeterminate if we want variable length restrictions
            title1 = request.form['search1'].lower()
            title2 = request.form['search2'].lower()
            title3 = request.form['search3'].lower()

            # Combining the three titles into a single string
            combined_titles = ' '.join([title1, title2, title3])

            # Create count matrix from the combined column
            vectorizer = CountVectorizer()
            movie_features = vectorizer.fit_transform()

            # declare model, compute similarity index, REFACTOR w. sklearn
            

            # get close matches from our movie list
            correct_titles = [get_close_matches(title, movie_cart, n=3, cutoff=0.6)[0] for title in [title1, title2, title3]]

            # run string into pre calibrated model
            
            # 

            return render_template('recommended.html')

        except Exception as e:
            print(e)
            return render_template("error.html")