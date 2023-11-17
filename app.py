import warnings
warnings.filterwarnings("ignore")

import numpy as np
import datetime as dt

import sqlalchemy as db
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify, render_template

import pandas as pd

engine = create_engine("sqlite:///movie_ratings_db.sqlite")

Base = automap_base()

Base.prepare(autoload_with=engine)

Links = Base.classes.links
Movies = Base.classes.movies
Ratings = Base.classes.ratings
Tags = Base.classes.tags

print(Base.classes.keys())

# https://www.geeksforgeeks.org/sqlalchemy-orm-conversion-to-pandas-dataframe/#

links_df = pd.read_sql_query(
    sql = db.select([Links.movieId,
                     Links.imdbId,
                     Links.tmdbId]),
    con = engine
)

print(len(links_df)) # Length should be 9742
links_df.head()

# We can probably ignore this table

movies_df = pd.read_sql_query(
    sql = db.select([Movies.movieId,
                     Movies.title,
                     Movies.genres]),
    con = engine
)

print(len(movies_df)) # Length should be 9742
movies_df.head()

ratings_df = pd.read_sql_query(
    sql = db.select([Ratings.userId,
                     Ratings.movieId,
                     Ratings.rating,
                     Ratings.timestamp]),
    con = engine
)

print(len(ratings_df)) # Length should be 100836
ratings_df.head()

tags_df = pd.read_sql_query(
    sql = db.select([Tags.userId,
                     Tags.movieId,
                     Tags.tag,
                     Tags.timestamp]),
    con = engine
)

print(len(tags_df)) # Length should be 3683
tags_df.head()

app = Flask(__name__)

@app.route("/")
def welcome():
    session = Session(engine)
    session.close()

    return ( # https://www.w3schools.com/html/html_links.asp, referenced for how to use HTML links
        f"<h2 id='Welcome Page Header'>Welcome to our Movie Recommendations App!</h2>" 
        f"<h3 id='Subheader'>Please use the following routes:</h3>"
        f"<p>"
        f"<a href='http://127.0.0.1:5000/movie_data'>movie_data </a>"
        f"for json data of all car crashes in Oregon involving wild animals<br>"
    )

@app.route("/movie_data")
def data():
    session = Session(engine)
    session.close()

    return render_template('simple.html', tables=[movies_df.to_html(classes="movies")], titles=movies_df.columns.values) # https://stackoverflow.com/questions/52644035/how-to-show-a-pandas-dataframe-into-a-existing-flask-html-table

if __name__ == "__main__":
    # load model
    app.run(debug=True)