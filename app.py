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

# print(len(links_df)) # Length should be 9742
links_df.head()

# We can probably ignore this table

movies_df = pd.read_sql_query(
    sql = db.select([Movies.movieId,
                     Movies.title,
                     Movies.genres]),
    con = engine
)

# print(len(movies_df)) # Length should be 9742
movies_df.head()

ratings_df = pd.read_sql_query(
    sql = db.select([Ratings.userId,
                     Ratings.movieId,
                     Ratings.rating,
                     Ratings.timestamp]),
    con = engine
)

# print(len(ratings_df)) # Length should be 100836
ratings_df.head()

tags_df = pd.read_sql_query(
    sql = db.select([Tags.userId,
                     Tags.movieId,
                     Tags.tag,
                     Tags.timestamp]),
    con = engine
)

# print(len(tags_df)) # Length should be 3683
tags_df.head()

# split genres column, drop original genres column, rename the first genre column to genre, drop additional genre columns
# in order to only keep first genre listed, assuming that's the most relevant 
movies_df_copy = movies_df.copy()
new = movies_df_copy["genres"].str.split("|",expand=True)
for i in new:
    movies_df_copy[f"genre{i + 1}"] = new[i]
movies_df_copy.drop(columns=["genres"], inplace=True)
movies_trimmed = movies_df_copy.rename(columns={"genre1": "genre"})
movies_trimmed.drop(columns=["genre2", "genre3", "genre4", "genre5", "genre6", "genre7", "genre8", "genre9", "genre10"], inplace=True)
# print(len(movies_trimmed))
movies_trimmed.dropna(inplace=True)
# print(len(movies_trimmed["title"].unique()))
movies_trimmed.set_index("movieId", inplace=True)
# movies_trimmed.head(100)

# add movie title and genre to tags dataframe based on movieId
tags_movies = tags_df.copy()
tags_movies["title"] = ""
tags_movies["genre"] = ""
for i in range(len(tags_movies)):
    movie = tags_movies.loc[i, "movieId"]
    film = movies_trimmed.at[movie, "title"]
    genre = movies_trimmed.at[movie, "genre"]
    tags_movies.loc[tags_movies.index[i], "title"] = film
    tags_movies.loc[tags_movies.index[i], "genre"] = genre
# print(len(tags_movies["userId"].unique()))
# tags_movies.head(25)

# Add ratings for each user/movie combo to movies + tags dataframe
tags_movies_ratings = tags_movies.copy()
tags_movies_ratings["rating"] = ""
for j in range(len(tags_movies_ratings)):
    user = tags_movies_ratings.loc[j, "userId"]
    movie = tags_movies_ratings.loc[j, "movieId"]
    rating = ratings_df.loc[((ratings_df["userId"]==user) & (ratings_df["movieId"]==movie)), "rating"] 
    if not rating.empty:
        tags_movies_ratings.loc[tags_movies_ratings.index[j], "rating"] = rating.item()
# tags_movies_ratings.head(25)

tmr_df = tags_movies_ratings.drop(columns="timestamp")  

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
        f"for json data of all movie titles in the database<br>"
    )

# API route returning a dataframe
# @app.route("/movie_data")
# def data():
#     session = Session(engine)

#     session.close()

#     return render_template('simple.html', tables=[tmr_df.to_html()], titles=tmr_df.columns.values) # https://stackoverflow.com/questions/52644035/how-to-show-a-pandas-dataframe-into-a-existing-flask-html-table

# API route returning jsonified dataframe
# @app.route("/movie_data")
# def data():
#     session = Session(engine)

#     session.close()

#     return tmr_df.to_json(orient="records")

# API route returning SQLite query results
@app.route("/movie_data")
def data():
    session = Session(engine)

    results = session.query(Movies.movieId, Movies.title, Movies.genres)

    session.close()

    movie_info = []

    for movieId, title, genres in results:
        movie_dict = {}
        movie_dict["movieId"] = movieId
        movie_dict["title"] = title
        movie_dict["genres"] = genres
        movie_info.append(movie_dict)

    return jsonify(movie_info)


if __name__ == "__main__":
    # load model
    app.run(debug=True)