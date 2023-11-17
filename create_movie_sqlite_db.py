# This file only serves to create the movie_ratings_db.sqlite file

import sqlite3
import pandas as pd

from pathlib import Path

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy import Column, Integer, String, Float

database_path = "movie_ratings_db.sqlite"

Path(database_path).touch()

conn = sqlite3.connect(database_path)
c = conn.cursor()

# This code creates classes and tables and imports the data from the csv files. 
# The SQLite database was created via commands in the terminal.
# Only use the terminal commands if the .sqlite database file needs to be created from scratch.
# Additional code is added to drop tables and vacuum the database if debugging the tables needs to be done.

# If the database file needs to be created, enter the following commands in the terminal to create
# the SQLite database before running the code blocks below:
# sqlite3 movie_ratings_db.sqlite
# .save movie_ratings_db.sqlite
# .quit

# Import csv data to tables. Run this code block second.
# links_data = pd.read_csv("data/links.csv")
# links_data.to_sql("links", conn, if_exists='append', index=False)
# movies_data = pd.read_csv("data/movies.csv")
# movies_data.to_sql("movies", conn, if_exists='append', index=False)
# ratings_data = pd.read_csv("data/ratings.csv")
# ratings_data.to_sql("ratings", conn, if_exists='append', index=False)
# tags_data = pd.read_csv("data/tags.csv") 
# tags_data.to_sql("tags", conn, if_exists='append', index=False)

# If there are issues creating the tables, use this code block to drop the tables and delete the empty space in the database
# https://stackoverflow.com/questions/4712929/how-to-use-sqlite-3s-vacuum-command-in-python, how to use vacuum to clear unused space from database
c.execute('''DROP TABLE links''')
c.execute('''DROP TABLE movies''')
c.execute('''DROP TABLE ratings''')
c.execute('''DROP TABLE tags''')
c.execute("VACUUM") 

conn.commit()

conn.close()

# Creates links, movies, ratings, and tags classes and tables with desired columns. Run this code block first.
# class Links(Base):
#     __tablename__ = "links"
#     movieId = Column(Integer, primary_key=True) 
#     imdbId = Column(Integer)
#     tmdbId = Column(Integer)
# class Movies(Base):
#     __tablename__ = "movies"
#     movieId = Column(Integer, primary_key=True)
#     title = Column(String)
#     genres = Column(String)
# class Ratings(Base):
#     __tablename__ = "ratings"
#     userId = Column(Integer, primary_key=True)
#     movieId = Column(Integer, primary_key=True) # Do we need to make this a foreign key?
#     rating = Column(Float)
#     timestamp = Column(Integer)
# class Tags(Base):
#     __tablename__ = "tags"
#     userId = Column(Integer, primary_key=True)
#     movieId = Column(Integer, primary_key=True) # Do we need to make this a foreign key?
#     tag = Column(String, primary_key=True)
#     timestamp = Column(Integer)
# from sqlalchemy import create_engine
# engine = create_engine("sqlite:///movie_ratings_db.sqlite")
# connection = engine.connect()
# Base.metadata.create_all(engine)
# from sqlalchemy.orm import Session
# session = Session(bind=engine)
# session.commit()
# session.close()