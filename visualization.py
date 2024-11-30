import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import preprocessing
import seaborn as sns

# Numerical distribution
def featureDist(songs):
    songs.hist(bins=50, figsize=(20, 8))
    plt.title('Feature Distribution')

# Genre distribution
def genreDist(songs):
    songs['genre'].value_counts().sort_index().plot(kind='bar')
    plt.title('Genre Distribution')
    plt.xlabel('Genre')
    plt.ylabel('Count')
    plt.xticks(rotation=45)

def featureCorrelation(songs):
    correlation = songs.corr(numeric_only=True)
    plt.figure(figsize=(12, 8))
    sns.heatmap(correlation, annot=True, cmap='coolwarm')
    plt.title('Feature Correlation Heatmap')
    plt.xticks(rotation=45)

def genreFeatureAvgs(songs, feature):
    genre_averages = songs.groupby('genre')[feature].mean()
    genre_averages.plot(kind='bar')
    plt.title(f'Average {feature.capitalize()} by Genre')
    plt.ylabel(f'Average {feature.capitalize()}')
    plt.xlabel('Genre', fontsize=14)
    plt.xticks(rotation=45)

def main():
    # Load data
    songs = pd.read_csv('songs.csv', encoding='latin1')

    # Preprocess data
    songs_preprocessed = preprocessing.preprocess_data('songs.csv')[0]

    # Show tables
    #numericalDist(songs)
    #genreDist(songs)
    #featureDist(songs_preprocessed)
    #genreDist(songs_preprocessed)
    #featureCorrelation(songs_preprocessed)
    genreFeatureAvgs(songs_preprocessed, 'energy')

    plt.show()

if __name__ == "__main__":
    main()