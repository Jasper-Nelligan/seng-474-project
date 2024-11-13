"""
This script gives an example of how to read metadata from an HDF5 file in the MSD.
"""
import tables
import hdf5_getters

# Open the HDF5 file
h5 = hdf5_getters.open_h5_file_read("C:/Users/jaspe/Downloads/millionsongsubset/MillionSongSubset/B/I/D/TRBIDYF128F42680C4.h5")

print(hdf5_getters.get_title(h5))

# Close the file when done
h5.close()