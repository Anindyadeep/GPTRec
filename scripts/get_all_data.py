from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

import dotenv
import os


dotenv.load_dotenv()

uri = os.getenv("MONGO_URI")
client = MongoClient(uri, server_api=ServerApi("1"))

db = client["sample_mflix"]
collection = db.get_collection("movies")

for document in collection.find():
    print(document)
    break
