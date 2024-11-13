"""
This script deletes all files in the MSD that are not in the LastFM dataset.
"""

import os

def get_files_in_directory(directory):
  file_dict = {}
  for _, _, files in os.walk(directory):
    for file in files:
      file_name, _ = os.path.splitext(file)
      file_dict[file_name] = None
  return file_dict

def delete_non_shared_files(shared_keys_dict, path):
  for root, _, files in os.walk(path):
    for file in files:
      file_name, _ = os.path.splitext(file)
      if file_name not in shared_keys_dict:
        os.remove(os.path.join(root, file))

lastfm_path = './lastfm_subset/'
msd_path = "./millionsongsubset/"

last_fm_files = get_files_in_directory(lastfm_path)
msd_files = get_files_in_directory(msd_path)

shared_keys_dict = {key: None for key in last_fm_files if key in msd_files}
delete_non_shared_files(shared_keys_dict, msd_path)