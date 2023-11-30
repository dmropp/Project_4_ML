# Project_4_ML

Movie recommendation systems help users discover content of interest, providing personalized recommendations to suit their taste while offering businesses tools for retention and increased user engagement. This project aims to craft a movie recommender system employing machine learning methodologies. Leveraging the MovieLens dataset, our analysis will curate an immersive, personalized journey into the realm of movie recommendations. This comprehensive endeavor spans data collection, cleansing, model development, optimization, and eventual deployment.

This movie recommendation app utilizes three kinds of recommendation systems:
* Collaborative filtering - An algorithm that recommends movies based on similar user preferences. This approach relies on the idea that people with similar preferences are likely to enjoy the same movies.
* Content-based filtering - This approach recommends movies based on the content of their attributes, such as genre, tag, and description.
* Hybrid systems - These systems combine both collaborative filtering and content-based strategies to perform a thorough analysis of a user's preferences, rating history, and details about a movie to deliver a more tailored recommendation.

## ETL
### Data Structure
* User Ratings: Ratings given by users to movies (usually on a scale of 1 to 5).
* Movie Information: Details about the movies (titles, genres, release years, etc.).
### Database Schema
* Designing an efficient database schema tailored to movie data attributes optimizes data storage and retrieval.
* Integration with SQLite allows seamless access to the movie dataset for application development.
* Utilizing Flask, a Python-based web framework, to connect the front-end user interface with the recommendation system's backend functionality.

## Content-Based
### Understanding Content-Based Filtering
* Content-Based Filtering relies on the intrinsic characteristics of items (movies, in this case) to make recommendations.
* It analyzes attributes or features of items to establish similarity and suggest items based on the user's preferences for similar attributes.
### Utilizing Genres as Features
* Genres serve as pivotal features in Content-Based Filtering for movies.
* Using genres, the system identifies similarities between movies based on shared genre categories.

## Collaborative-Based 
### Understanding Collaborative Filtering
* Collaborative Filtering recommends items based on the preferences of similar users.
* It identifies patterns by considering users' historical interactions (ratings) with items.
### User-Item Matrix and Similarity Measures
* Collaborative Filtering operates on a user-item interaction matrix.
* Similarity measures (cosine similarity) quantify the likeness between users or items based on their interaction patterns.

## Our Hybrid Approach
### TF-IDF Vector and Cosine for Content-Based
* This technique captures the uniqueness of words in each document, enabling the representation of genres or tags as numerical feature vectors.
* Cosine Similarity measures the similarity between TF-IDF vectors of different movies based on the angle between them.
* Higher cosine similarity scores imply greater similarity in terms of content between movies.
### Nearest Neighbor for Collaborative Filtering
* Using attributes derived from nearest neighbors in Collaborative Filtering involves identifying similar users or items based on their attributes or features.
* The hybrid model helps mitigate the cold start problem for new users/items by utilizing both content and attributes shared with similar users.

## Hybrid Testing
### TF-IDF Vector and Cosine Similarity on Content
* Utilizing the cosine similarity function to compute the similarity between test and train matrices.
* Calculating the accuracy percentage by comparing the number of correct predictions against the total number of test items.
* Ending accuracy: 74.5%
### Subset interaction in Collaborative
* Utilizing subsets to simulating a more realistic scenario where users may consider a limited subset of their actual preferences.
* Calculating the accuracy metric by dividing the number of correct recommendations by the total recommendations considered for all users.
* Accuracy reflects the proportion of correctly recommended movies within the user subsets.
* Ending accuracy: 66.41%
### Hybrid Ending Accuracy: 82.44%

## Web Interface Development
### HTML, CSS, and Bootstrap for Interface Design
* Leveraging HTML for structuring, CSS for styling, and Bootstrap for responsive design to craft an engaging and visually appealing user interface.
### Flask Interactions
* Defining API endpoints and routes within Flask , to facilitate communication between the front-end interface and the recommendation engine's backend functionality.
### Interactive Experience
* These endpoints handle requests for movie recommendations that occur by genre, hybrid recommendation system, or completely random.

## Deploying Movie Recommendations
### Genre-Based Recommendation
* The system employs a straightforward yet effective mechanism that matches movie titles to their respective genres from a curated list. Modulated with slight randomization so that picks within a genre are not the same repeated set.
### Hybrid Recommendation
* Users have the power to influence their recommendations by providing feedback on suggested movies. Once five movies garner positive feedback, our algorithm springs into action, using this valuable input to refine its recommendations.
### Random Recommendation
* Exactly as the name implies.

## How to Use the Application
* create_movie_sqlite_db.py - File to create the SQLite database from the original CSV files (links.csv, movies.csv, ratings.csv, tags.csv).
* movie_rec_app.py - Movie recommendation app. Run this app to utilize the web interface.

## Data Source
* https://grouplens.org/datasets/movielens/
