import json
from spotify_api import get_spotify_access_token, get_track_features, get_track_id
import os
from dotenv import load_dotenv
import sqlite3

load_dotenv()

client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

tags_include = [
    "rock",
    "pop",
    "alternative",
    "indie",
    "electronic",
    "dance",
    "jazz",
    "singer-songwriter",
    "metal",
    "soul",
    "folk",
    "instrumental",
    "punk",
    "ambient",
    "hip-hop",
    "country",
]

def get_spotify_features(artist, track, release):
    track_id = get_track_id(artist, track, release)
    if track_id:
        return get_track_features(track_id)
    else:
        print('Track not found in Spotify database:', artist, track, release)
        return None

if __name__ == "__main__":
    print("Starting script...")
    # Initialize the Spotify API
    get_spotify_access_token(client_id, client_secret)

    # Connect to the SQLite database
    conn = sqlite3.connect('msd.db')
    cursor = conn.cursor()

    # Create combined_data table if it does not already exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS combined_data (
        track_id TEXT PRIMARY KEY,
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
    max_songs = 20000
    spotify_error_occured = False
    for root, _, files in os.walk("lastfm_test"):
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
                    song_id = os.path.splitext(file)[0]

                    cursor.execute('SELECT * FROM songs WHERE track_id = ?', (song_id,))
                    track_entry = cursor.fetchone()

                    cursor.execute('SELECT 1 FROM combined_data WHERE track_id = ?', (song_id,))
                    entry_exists = cursor.fetchone() is not None
                    
                    # If the song data is already in the combined_data table, skip it
                    if entry_exists:
                        print("Entry already exists for", song_id)
                    else:
                        title = track_entry[1]
                        release = track_entry[3]
                        artist = track_entry[6]

                        try:
                            # Get Spotify features for the song
                            spotify_features = get_spotify_features(artist, title, release)
                            if not spotify_features:
                                cursor.execute('''
                                INSERT OR REPLACE INTO combined_data (track_id, artist, title, release, genre, danceability, energy, key, loudness, mode, speechiness, acousticness, instrumentalness, liveness, valence, tempo)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                                ''', (song_id, artist, title, release, top_tag, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1))
                                songs_added_to_db += 1
                                print(songs_added_to_db, "songs added to the database")
                                conn.commit()
                                continue
                        except Exception as e:
                            print('Error getting Spotify features: ', e)
                            spotify_error_occured = True
                            break

                        # Insert the new entry into the combined_data table
                        cursor.execute('''
                        INSERT OR REPLACE INTO combined_data (track_id, artist, title, release, genre, danceability, energy, key, loudness, mode, speechiness, acousticness, instrumentalness, liveness, valence, tempo)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ''', (song_id, artist, title, release, top_tag,
                              spotify_features.get('danceability', None),
                              spotify_features.get('energy', None),
                              spotify_features.get('key', None),
                              spotify_features.get('loudness', None),
                              spotify_features.get('mode', None),
                              spotify_features.get('speechiness', None),
                              spotify_features.get('acousticness', None),
                              spotify_features.get('instrumentalness', None),
                              spotify_features.get('liveness', None),
                              spotify_features.get('valence', None),
                              spotify_features.get('tempo', None)))
                        songs_added_to_db += 1
                        print(songs_added_to_db, "songs added to the database")
                        conn.commit()

    # Close the connection
    conn.close()