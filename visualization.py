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

# Feature Correlation Heatmap
def featureCorrelation(songs):
    correlation = songs.corr(numeric_only=True)
    plt.figure(figsize=(12, 8))
    sns.heatmap(correlation, annot=True, cmap='coolwarm')
    plt.title('Feature Correlation Heatmap')
    plt.xticks(rotation=45)

# Feature Averages by Genre
def genreFeatureAvgs(songs):
    features = songs.select_dtypes(include=['number']).columns.tolist()

    print("Select a feature to get average by genre:")
    for i, feature in enumerate(features):
        print(f"{i + 1}. {feature}")

    num = int(input("Enter the number corresponding to your choice: "))
    feature = features[num -1]
    genre_averages = songs.groupby('genre')[feature].mean().sort_values()

    genre_averages.plot(kind='bar')
    plt.title(f'Average {feature.capitalize()} by Genre')
    plt.ylabel(f'Average {feature.capitalize()}')
    plt.xlabel('Genre')
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
    genreFeatureAvgs(songs_preprocessed)

    plt.show()

if __name__ == "__main__":
    main()