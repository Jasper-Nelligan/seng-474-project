import matplotlib.pyplot as plt
import pandas as pd
import preprocessing
import seaborn as sns

# Numerical distribution before preprocesing
def numericalDist(songs):
    songs.hist(bins=50, figsize=(20, 8))
    plt.title('Numerical Distribution')

# Genre distribution before preprocesing
def genreDist(songs):
    songs['genre'].value_counts().sort_index().plot(kind='bar')
    plt.title('Genre Distribution')
    plt.xlabel('Genre')
    plt.ylabel('Count')
    plt.xticks(rotation=45)

def main():
    # Load data
    songs = pd.read_csv('songs.csv', encoding='latin1')
    songs_preprocessed = preprocessing.preprocess_data('songs.csv')[0]

    #numericalDist(songs)
    #genreDist(songs)
    numericalDist(songs_preprocessed)
    #genreDist(songs_preprocessed)

    plt.show()

main()