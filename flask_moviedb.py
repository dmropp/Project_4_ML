# Import the dependencies.
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify, request
import datetime as dt

# flask guru
from flask import Flask, request, render_template
from flask_cors import cross_origin
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from difflib import get_close_matches
from tmdbv3api import TMDb, Movie
import requests



#################################################
# Database Setup
#################################################
# path to engine, POST
engine = create_engine("sqlite:///Resources/movie_sqlite.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# references to each table
movies = Base.classes.movies
tags = Base.classes.tags
users = Base.classes.users

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
#################################################
# fuckin' routes
#################################################



@app.route("/")
def home():
    return (
        f"<h1>Home: Climate Analysis API</h1>"
        f"<h3>Available Routes:</h3>"
        f"<b><a href=\"/api/v1.0/precipitation\">/api/v1.0/precipitation</a></b> <br />"
        f"<br />"
        f"<b><a href=\"/api/v1.0/stations\">/api/v1.0/stations</a></b><br />"
        f"<br />"
        f"<b><a href=\"/api/v1.0/tobs\">/api/v1.0/tobs</a></b> <br />"
        f"<br />"
        f"<b><a href=\"/api/v1.0/range?start=2016-03-12&end=2016-08-19\">/api/v1.0/range</a></b> <br />"
        f"<br />"
        f"Set a range using start and end dates, or set a single date using start or end parameters. <br />" 
        f"If a <strong>start</strong> date is specified, data will be ranged from your start date to the end of the set. <br />"
        f"If a <strong>end</strong> date is specified, data will range from the start of the set to your specified end date. <br />"
        f"Dates should follow yyyy-mm-dd format using <strong>start</strong> and <strong>end</strong> parameters.<br />"
        f"<li>for example: /api/v1.0/range?start=2016-03-12&end=2016-08-19</li>"
        f"<li>alternative, with one parameter: /api/v1.0/range?start=2016-03-12</li>"
        f"<li>start and end dates should be chronological in order</li>"
    )

# precipitation pathing
@app.route("/api/v1.0/precipitation")
# create precipitation query function
def precipitation():
    # session creation
    session = Session(engine)
    
    # data obs stop at 2017.8.23, managing year increment with timedelta, BCA is magic
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    # selecting two cols, date and prcp
    # filter alters query by filtering rows greater than or equal to the date calc on prev_year
    # all appends rows that match our conditions, returns as a list of tuples
    precipitation = session.query(measurement.date, measurement.prcp).filter(measurement.date >= prev_year).all()
    
    # dictionary setup, iterates over each tuple pair in precipitation
    # precip dictionary, date is our key, prcp is a value
    precip = [{'date': date, 'prcp': prcp} for date, prcp in precipitation]
    
    session.close()
    # precip=precip so json isn't a really long list
    return jsonify(precip=precip)

 
# stations pathing
@app.route("/api/v1.0/stations")
def stations():
    # session creation
    session = Session(engine)
    
    # query list of all the stations
    results = session.query(station.station).all()
    
    # station list can stay like this, basically makes a dictionary where the only key value is 'stations'
    stations = list(np.ravel(results))
    
    session.close()
    # stations=stations will auto format to json 
    return jsonify(stations=stations)

# tobs for USC00519281 pathing
@app.route("/api/v1.0/tobs")
def temp_monthly():
    # session creation
    session = Session(engine)
    
    # data obs stop at 2017.8.23, managing year increment with timedelta, BCA is magic
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    # query listing for tobs data
    usc_results = session.query(measurement.date, measurement.tobs).filter(measurement.station == 'USC00519281').filter(measurement.date >= prev_year).all()
    
    # total obs dictionary, date is our key, tobs is a value
    total_obs = [{'date': date, 'tobs': tobs} for date, tobs in usc_results]
    
    session.close()
    return jsonify(total_obs=total_obs)

# range of dates pathing
@app.route("/api/v1.0/range")
def range():
    # parameter setup is range?start=yyyy-mm-dd&end=yyyy-mm-dd
    start_date = request.args.get('start')
    end_date = request.args.get('end')
    
    # if no start or end is specified, default values
    # if only start or end, this subs in start/end dates 
    if end_date is None:
        end_date = "2017-08-23"
    if start_date is None:
        start_date = "2010-01-01"
        
    session = Session(engine)
    
    # selection statement, selects the date and the augmented stat values for prcp
    sel = [measurement.date, func.min(measurement.prcp), func.max(measurement.prcp), func.avg(measurement.prcp)]
    
    # query list, using *sel to select the date and augmented stat values
    date_range = session.query(*sel).\
                filter(measurement.date >= start_date).\
                filter(measurement.date <= end_date).\
                group_by(measurement.date).all()
                
    # exporting as a dictionary instead of a 1d list, I think it looks better
    range_temps = [{'date': date,
                    'min_prcp': min_prcp, 
                    'max_prcp': max_prcp, 
                    'avg_prcp': avg_prcp} for date, min_prcp, max_prcp, avg_prcp in date_range]
    
    session.close()
    app.json.sort_keys = False
    return jsonify(range_temps=range_temps)


if __name__ == "__main__":
    app.run(debug=True)