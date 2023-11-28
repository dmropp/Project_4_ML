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
