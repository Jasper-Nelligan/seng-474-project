import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('msd.db')
cursor = conn.cursor()

query = """
SELECT COUNT(*) as count
FROM combined_data
"""

cursor.execute(query)
results = cursor.fetchall()
print(f"Total rows in combined_data: {results[0]}")

# Query to get the count for each genre feature, sorted from most to least
query = """
SELECT COUNT(*) as count
FROM combined_data
WHERE danceability = -1
"""

# Execute the query
cursor.execute(query)

# Fetch all results
results = cursor.fetchall()

# Print the results
print(f"Count of rows with -1 values: {results[0]}")

# SQL query to count occurrences of each genre
query = '''
SELECT genre, COUNT(*) as count
FROM combined_data
WHERE danceability != -1
GROUP BY genre
ORDER BY count DESC;
'''

# Execute the query
cursor.execute(query)

# Fetch all results
results = cursor.fetchall()

# Print the results
print("Occurrences of each genre with valid data:")
for row in results:
    print(f"Genre: {row[0]}, Count: {row[1]}")

# Close the connection
conn.close()