# Import the dependencies.
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify, request
import datetime as dt


#################################################
# Database Setup
#################################################
# path to engine, POST
engine = create_engine("sqlite:///movie_ratings_db.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# references to each table
ratings = Base.classes.ratings
movies = Base.classes.movies
tags = Base.classes.tags

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
#################################################
# fuckin' routes
#################################################


# TEMPORARY for testing
@app.route("/")
def home():
    return (
        f"<h1>Pick a movie:</h1>"
        f"<h3>If it doesn't populate the list then it might not exist.</h3>"
        f"<b><a href=\"/api/v1.0/movies\">/api/v1.0/movies</a></b> <br />"
        f"<br />"
        
    )

# TEMPORARY movies pathing for testing
# combining tables to indicate movie title to rating
@app.route("/api/v1.0/movies")
def movies():
    # session creation
    session = Session(engine)
    # selecting for ratings.userId, ratings.movieId, ratings.rating
    # selecting for movies.movieId and movies.title
    combined_data = session.query(ratings, movies).filter(ratings.movieId == movies.movieID).all()
    
    result = [{'Movies ID': item.movies.movieId, 
            'Movie Title': item.movies.title,
                'User ID': item.ratings.userID,
                'Rating': item.ratings.rating} for item in combined_data]
    
    session.close()
    app.json.sort_keys = False
    return jsonify(result=result)


if __name__ == "__main__":
    app.run(debug=True)