# Project 4
### Created by Adam Ropp, Christina Tetreault, Ben Jarrell, Mitchel Rounds, and Thor Black
# Movie Recommendation System

Presentation slides: https://gamma.app/public/Movie-Recommendation-System-dzdlk3mcnwm5xkc

Movie recommendation systems offer personalized suggestions, aiding users in discovering content they're likely to enjoy. These systems not only enhance user satisfaction but also contribute to increased engagement and revenue for businesses.

## Why Personalized Recommendations Matter

- **Reducing Choice Overload:** With an abundance of movie options, tailored suggestions alleviate decision fatigue and prompt user engagement.
- **Improved User Satisfaction:** Tailored recommendations increase the likelihood of user return visits.
- **Boosting Engagement and Revenue:** Enhanced user engagement and satisfaction translate into increased revenue for businesses.

## Challenges in Movie Recommendation

- **Cold Start Problem:** New users lack interaction history, posing a challenge in offering personalized recommendations.
- **Data Sparsity:** Gaps in data pertaining to movies, users, and ratings hinder accurate recommendations.

## Project Scope

Our project focuses on crafting a movie recommender system using machine learning techniques. Leveraging the MovieLens dataset, the project involves data collection, cleansing, model development, optimization, and deployment.

### ETL

- **Data Structure:** Utilizing user ratings and movie information for analysis.
- **Database Schema:** Optimizing storage and retrieval efficiency using SQLite.
- **Integration with Flask:** Connecting the front-end UI with the backend recommendation system.

### Content-based and Collaborative Filtering

- **Content-Based Filtering:** Utilizes movie attributes like genres to suggest similar movies.
- **Collaborative Filtering:** Recommends based on user preferences and historical interactions.

### Hybrid Approach

- **TF-IDF Vector and Cosine for Content-Based:** Captures uniqueness and similarity between movies based on genres.
- **Nearest Neighbor for Collaborative Filtering:** Utilizes attributes from similar users or items.
- **Hybrid Testing:** Evaluates accuracy using cosine similarity and subset interactions.

### Web Interface Development

- **HTML, CSS, and Bootstrap:** Crafting an engaging UI with HTML structure, CSS styling, and Bootstrap for responsiveness.
- **Flask Interactions:** Defining endpoints for communication between UI and backend functionality.

## Deploying Movie Recommendations

- **Genre-Based Recommendation:** Matches movie titles to genres from a curated list.
- **Hybrid Recommendation:** Refines suggestions based on user feedback.
- **Random Recommendation:** Provides entirely random movie suggestions.

## Conclusion

### Successes

- **Hybrid Recommendations:** Delivering accurate, diverse, and personalized suggestions.
- **Generalization:** Guarding against overfitting by ensuring the system generalizes well to unseen data.

### Struggles

- **Cold Start Problem:** Addressing new user/item recommendations with limited data.
- **Complexity:** Weighing and integrating multiple techniques within the hybrid system.
