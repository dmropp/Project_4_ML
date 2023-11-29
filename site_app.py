# flask app setup
from flask import Flask, render_template, request
import requests
import torch
from torch.autograd import Variable
from torch.utils.data.dataset import Dataset
from torch.utils.data import DataLoader
from tqdm import tqdm_notebook as tqdm

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors
from joblib import load

import sqlite3

import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)


# Recommendation route - handle movie input and provide recommendations
@app.route('/recommend', methods=['POST'])
def recommend():
    entered_movie = request.form['movie']  # Get the entered movie from the form
    
    # Paste the huge chunk of code here
    con = sqlite3.connect("movie_ratings_db.sqlite")
    movies_df = pd.read_sql_query("SELECT * FROM Movies", con)
    ratings_df = pd.read_sql_query("SELECT * FROM Ratings", con)

    # mapping movie titles to Ids using to_dict
    movie_titles = movies_df.set_index('movieId')['title'].to_dict()

    entered_movie_id = next((movie_id for movie_id, title in movie_titles.items() if title == entered_movie), None)

    # confirm length of ratings_df, need det for users and movies
    n_users = len(ratings_df.userId.unique())
    n_items = len(ratings_df.movieId.unique())

    # weight matrix, matrix1 will use n_users, matrix2 will use n_items, 
    # overlap will be n_users to movies that they have rated
    # class inherits torch.nn, further integration into native pytorch
    class MatrixFactorization(torch.nn.Module):
        # factors default to 20, pair process of users and movies
        def __init__(self, n_users, n_items, n_factors=20):
            super().__init__()
            # unique_user embedding, initialized as lookup tables
            self.user_factors = torch.nn.Embedding(n_users, n_factors)
            # unique_movie embedding, ""
            self.item_factors = torch.nn.Embedding(n_items, n_factors)
            
            # lookup tables, embeddings, initialized small random values 
            self.user_factors.weight.data.uniform_(0, 0.05)
            self.item_factors.weight.data.uniform_(0, 0.05)
            
        def forward(self, data):
            # data[] for movie indicies, takes user/movie pairs rep as index
            users, items = data[:,0], data[:,1].long()
            # dot product : user/movie position mult then sum into factor with axis=1
            return (self.user_factors(users)*self.item_factors(items)).sum(1)
        def predict(self, user, item):
                return self.forward(user, item)

    # data loader creation
    class Loader(Dataset):
        def __init__(self):
            self.ratings = ratings_df.copy()
            
            # Extract all user IDs and movie IDs
            users = ratings_df.userId.unique()
            movies = ratings_df.movieId.unique()
            
            # unique values dict, pair to index
            self.userid2idx = {o:i for i,o in enumerate(users)}
            self.movieid2idx = {o:i for i,o in enumerate(movies)}
            
            # append continuous ID for users and movies as .items in dict
            self.idx2userid = {i:o for o,i in self.userid2idx.items()}
            self.idx2movieid = {i:o for o,i in self.movieid2idx.items()}
            
            # baseball bat
            self.ratings.movieId = ratings_df.movieId.apply(lambda x: self.movieid2idx[x])
            self.ratings.userId = ratings_df.userId.apply(lambda x: self.userid2idx[x])
            
            # remove timestamp and rating, we got what we need
            self.x = self.ratings.drop(['rating', 'timestamp'], axis=1).values
            self.y = self.ratings['rating'].values
            # convert x and y to tensor for model application
            self.x, self.y = torch.tensor(self.x), torch.tensor(self.y)

        def __getitem__(self, index):
            return (self.x[index], self.y[index])

        def __len__(self):
            return len(self.ratings)
        
    # model call
    model = MatrixFactorization(n_users, n_items, n_factors=8)
    model = model.to(torch.float32)
    print(model)
    for name, param in model.named_parameters():
        if param.requires_grad:
            print(name, param.data)

    # Mean Squared Error loss function
    loss_fn = torch.nn.MSELoss()

    # adam optimize
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

    # train data load and set
    train_set = Loader()
    train_loader = DataLoader(train_set, batch_size=100, shuffle=True)

    # Training loop
    epochs = 10

    for epoch in range(epochs):
            total_loss = 0
            for batch_idx, (data, target) in enumerate(train_loader):
                    # Zero the gradients
                    optimizer.zero_grad()
                    # Forward pass
                    data = data.to(torch.int)
                    output = model(data)
                    # Compute loss
                    target = target.to(torch.float)
                    loss = loss_fn(output, target)
                    # Backpropagation
                    loss.backward()
                    optimizer.step()
            # Track total loss
            total_loss += loss.item()

            # Print average loss per epoch
            print(f"Epoch [{epoch + 1}/{epochs}], Loss: {total_loss / len(train_loader)}")

##########

    trained_movie_embeddings = model.item_factors.weight.data.cpu().numpy()

    import json

    # Fit the clusters based on the movie weights
    kmeans = KMeans(n_clusters=10, random_state=42).fit(trained_movie_embeddings)

    # [1] is entry for now, entry should be toy story
    entered_movie_cluster = kmeans.predict(trained_movie_embeddings[[entered_movie]])

    # movies in the same cluster as the entered movie
    movies_in_same_cluster = []
    for movidx, cluster_label in enumerate(kmeans.labels_):
        if cluster_label == entered_movie_cluster:
            movies_in_same_cluster.append(train_set.idx2movieid[movidx])
            # exit loop to limit the number of entries that populate
            if len(movies_in_same_cluster) == 10:
                break 
    # recommendation list, use movie_title map to form array based on movies_in_same_cluster
    titles_array = [movie_titles[movie_id] for movie_id in movies_in_same_cluster if movie_id in movie_titles]

    
    # Returning recommendations to an HTML page
    return render_template('recommendations.html', titles_array=titles_array)

if __name__ == '__main__':
    app.run(debug=True)
