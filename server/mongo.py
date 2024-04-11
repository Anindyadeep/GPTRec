from pymongo.server_api import ServerApi
from pymongo.mongo_client import MongoClient
import os 

mongo_connection_uri = os.environ.get("MONGO_CONNECTION_URI")

mongo_client = MongoClient(mongo_connection_uri, server_api=ServerApi("1"))
db = mongo_client["gpt_rec"]
collection = db.get_collection("movies")
