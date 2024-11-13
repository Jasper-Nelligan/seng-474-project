import sqlite3
import csv

# Connect to the SQLite database
conn = sqlite3.connect('msd.db')
cursor = conn.cursor()

# Fetch all data from the combined_data table
cursor.execute('SELECT * FROM combined_data')
rows = cursor.fetchall()

# Get column names
column_names = [description[0] for description in cursor.description]

# Write data to a CSV file
with open('songs.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(column_names)  # Write header
    csvwriter.writerows(rows)  # Write data

# Close the database connection
conn.close()