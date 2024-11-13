import tables

# Open the HDF5 file
filename = "C:/Users/jaspe/Downloads/millionsongsubset/MillionSongSubset/B/I/D/TRBIDYF128F42680C4.h5"
file = tables.open_file(filename, mode='r')

# Access the metadata table
metadata_table = file.root.metadata.songs

# Iterate over rows in the metadata table and print artist name and album
for row in metadata_table:
    print(f"Artist Name: {row['artist_name']}, Album: {row['release']}")

# Close the file when done
file.close()