import json
from spotify_api import get_spotify_access_token, get_multiple_track_features, get_track_id
import os
from dotenv import load_dotenv
import sqlite3
import time

load_dotenv()

client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

tags_include = [
    # "rock",
    #"pop",
    #"alternative",
    #"indie",
    #"electronic",
    #"dance",
    #"jazz",
    # "singer-songwriter",
    "metal",
    #"soul",
    #"folk",
    #"instrumental",
    #"punk",
    "ambient",
    #"hip-hop",
    #"country",
]

def get_spotify_features(artist, track, release):
    track_id = get_track_id(artist, track, release)

    if track_id:
        return get_multiple_track_features(track_id)
    else:
        print('Track not found in Spotify database:', artist, track, release)
        return None

def main():
    # Initialize the Spotify API
    get_spotify_access_token(client_id, client_secret)

    # Connect to the SQLite database
    conn = sqlite3.connect('msd.db')
    cursor = conn.cursor()

    # Create combined_data table if it does not already exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS combined_data (
        track_id TEXT PRIMARY KEY,
        spotify_id TEXT,
        artist TEXT,
        title TEXT,
        release TEXT,
        genre TEXT,
        danceability REAL,
        energy REAL,
        key INTEGER,
        loudness REAL,
        mode INTEGER,
        speechiness REAL,
        acousticness REAL,
        instrumentalness REAL,
        liveness REAL,
        valence REAL,
        tempo REAL
    )
    ''')

    cursor.execute('SELECT COUNT(*) FROM combined_data')
    num_entries = cursor.fetchone()[0]

    # Parse the last.fm data
    songs_added_to_db = num_entries
    max_songs = 30000
    spotify_error_occured = False
    spotify_ids_batch = []
    for root, _, files in os.walk("lastfm_train"):
        if spotify_error_occured:
            print("Spotify error occured, skipping remaining songs")
            break

        for file in files:
            if spotify_error_occured:
                print("Spotify error occured, skipping remaining songs")
                break

            if songs_added_to_db >= max_songs:
                break

            with open(root + "\\\\" + file, "r") as json_file:
                lastfm_data = json.load(json_file)
                tags = lastfm_data.get("tags", [])

                # Remove tags that are not strongly associated with the song,
                # or not in the list of included tags. Assumes that each song
                # can only contain one included tag with a score of 100
                top_tag = ""
                for tag in tags:
                    tag[0] = tag[0].lower()
                    if tag[1] == "100" and tag[0] in tags_include:
                        top_tag = tag[0]

                if top_tag == "":
                    continue
                else:
                    msd_id = os.path.splitext(file)[0]

                    # Fetch song data from the songs table
                    cursor.execute('SELECT * FROM songs WHERE track_id = ?', (msd_id,))
                    track_entry = cursor.fetchone()

                    if not track_entry:
                        print(f"No track entry found for track ID {msd_id}")
                        continue

                    cursor.execute('SELECT 1 FROM combined_data WHERE track_id = ?', (msd_id,))
                    entry_exists = cursor.fetchone() is not None
                    
                    # If the song data is already in the combined_data table, skip it
                    if entry_exists:
                        print("Entry already exists for", msd_id)
                        continue

                    title = track_entry[1]
                    release = track_entry[3]
                    artist = track_entry[6]

                    try:
                        spotify_id = get_track_id(artist, title, release)

                        cursor.execute('''
                        INSERT OR REPLACE INTO combined_data (track_id, spotify_id, artist, title, release, genre, danceability, energy, key, loudness, mode, speechiness, acousticness, instrumentalness, liveness, valence, tempo)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ''', (msd_id, spotify_id, artist, title, release, top_tag, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1))
                        songs_added_to_db += 1
                        conn.commit()

                        if spotify_id:
                            spotify_ids_batch.append(spotify_id)
                            print("Track IDs list length:", len(spotify_ids_batch))

                        # Get Spotify features for the current batch of track IDs
                        if len(spotify_ids_batch) == 99:
                            print("Getting Spotify features for", len(spotify_ids_batch), "tracks")
                            spotify_features = get_multiple_track_features(spotify_ids_batch)
                            time.sleep(10)
                            if not spotify_features:
                                print("Error getting Spotify features for batch")
                                spotify_ids_batch = []
                                continue

                            
                            i = 0
                            for features in spotify_features:
                                cursor.execute('''
                                UPDATE combined_data
                                SET danceability = ?,
                                    energy = ?,
                                    key = ?,
                                    loudness = ?,
                                    mode = ?,
                                    speechiness = ?,
                                    acousticness = ?,
                                    instrumentalness = ?,
                                    liveness = ?,
                                    valence = ?,
                                    tempo = ?
                                WHERE spotify_id = ?
                                ''', (features.get('danceability', None),
                                    features.get('energy', None),
                                    features.get('key', None),
                                    features.get('loudness', None),
                                    features.get('mode', None),
                                    features.get('speechiness', None),
                                    features.get('acousticness', None),
                                    features.get('instrumentalness', None),
                                    features.get('liveness', None),
                                    features.get('valence', None),
                                    features.get('tempo', None),
                                    spotify_ids_batch[i]))
                                i += 1
                                conn.commit()
                            songs_added_to_db += len(spotify_features)
                            print(len(spotify_features), "songs updated in the database")
                            spotify_ids_batch = []
                    except Exception as e:
                        print('Error getting Spotify features: ', e)
                        spotify_error_occured = True
                        break

    # Close the connection
    conn.close()

if __name__ == "__main__":
    print("Starting script...")
    main()
    