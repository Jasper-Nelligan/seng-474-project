import pandas as pd
import matplotlib.pyplot as plt

# Loading data
songs = pd.read_csv('songs.csv', encoding='latin1')

# Drop spotify_id and invalid entries
songs = songs.drop('spotify_id', axis=1)
songs = songs[songs['danceability'] != -1]

# Balance dataset by downsampling
min_genre = songs['genre'].value_counts().min()
songs = songs.groupby('genre').sample(n=min_genre, random_state=42)

# Get genre distribution
print(songs['genre'].value_counts())

# Show numerical distributions
songs.hist(bins=50, figsize=(20, 8))
plt.show()