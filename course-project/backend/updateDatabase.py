import pandas as pd
from pymongo import MongoClient

# TODO: Update below template to our project-specific information

# Connect to the MongoDB instance
client = MongoClient('mongodb://localhost:27017')
db = client['mydatabase']
collection = db['mycollection']

# Read the CSV file into a pandas DataFrame
df = pd.read_csv('yourfile.csv')

# Define the field(s) to use as a unique key for matching existing documents
key_field = 'unique_id_column'

# Add a new field to every row in the collection
new_field_name = 'new_field'
new_field_value = 'default_value'  # Change this to your desired value

# Option 1: Add field to all documents at once
collection.update_many({}, {'$set': {new_field_name: new_field_value}})

# Option 2: Add field while updating from CSV
for _, row in df.iterrows():
    query = {key_field: row[key_field]}
    row_dict = row.to_dict()
    row_dict[new_field_name] = new_field_value  # Add the new field
    update_data = {'$set': row_dict}
    collection.update_one(query, update_data, upsert=True)

# # Iterate over rows and perform an existing-column update with upsert=True
# for _, row in df.iterrows():
#     query = {key_field: row[key_field]}
#     update_data = {'$set': row.to_dict()} # Use $set to update specific fields
#     collection.update_one(query, update_data, upsert=True)
