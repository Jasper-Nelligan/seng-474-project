import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split

def preprocess_data(file_path):
    # Loading data
    songs = pd.read_csv(file_path, encoding='latin1')

    # Drop spotify_id and invalid entries
    songs = songs.drop('spotify_id', axis=1)
    songs = songs[songs['danceability'] != -1]

    # Balance dataset by downsampling
    min_genre = songs['genre'].value_counts().min()
    songs = songs.groupby('genre').sample(n=min_genre, random_state=42)

    # Get genre distribution
    print(songs['genre'].value_counts())

    # Get features
    print(songs.columns.tolist())

    # Normalize features
    min_max_scaler = MinMaxScaler()
    songs[['tempo', 'loudness', 'speechiness']] = min_max_scaler.fit_transform(songs[['tempo', 'loudness', 'speechiness']])

    # Split data into testing and training sets
    train_set, test_set = train_test_split(songs, test_size=0.2, random_state=42)
    print(len(train_set), len(test_set))

    return songs, train_set, test_set

songs, train_set, test_set = preprocess_data('songs.csv')
