import os
import pandas as pd
import hdf5_getters
import json

count = 0

def combine_files(lastfm_file_path, millionsong_file_path, data):
    global count

    h5 = hdf5_getters.open_h5_file_read(millionsong_file_path)
    artist_name = hdf5_getters.get_artist_name(h5)
    title = hdf5_getters.get_title(h5)
    release = hdf5_getters.get_release(h5)

    with open(lastfm_file_path, 'r') as json_file:
        lastfm_data = json.load(json_file)
        tags = lastfm_data.get('tags', [])
        
        # Append the data to the list
        data.append({
            'artist_name': artist_name,
            'title': title,
            'release': release,
            'tags': tags
        })

        print(count)
        count += 1

    # Close the files when done
    h5.close()

lastfm_path = './lastfm_subset'
millionsong_path = './millionsongsubset'
data = []

for root, subdirs, files in os.walk(lastfm_path):
    for file in files:
        file_name, _ = os.path.splitext(file)
        lastfm_file_path = os.path.join(root, file_name + '.json')
        relative_path = os.path.relpath(root, lastfm_path)
        millionsong_file_path = os.path.join(millionsong_path, relative_path, file_name + '.h5')

        if os.path.exists(millionsong_file_path):
            combine_files(lastfm_file_path, millionsong_file_path, data)

# Convert the data to a DataFrame and write to a CSV file
df = pd.DataFrame(data)
df.to_csv('combined_data.csv', index=False)