import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Read the connection string from the environment
CONNECTION_STRING = os.getenv("MONGO_CONNECTION_STRING")

# Define database and collection names
DATABASE_NAME = "userDatabase"
COLLECTION_NAME = "users"

def get_db_connection():
    """
    Returns a reference to the 'userDatabase' database.
    """
    client = MongoClient(CONNECTION_STRING)
    return client[DATABASE_NAME]

# Initialize the MongoDB client
client = MongoClient(CONNECTION_STRING)
db = client[DATABASE_NAME]
users_collection = db[COLLECTION_NAME]

print(f"Connected to database '{DATABASE_NAME}' and collection '{COLLECTION_NAME}'.")
