from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import lancedb
import dotenv
import os
from tqdm.auto import tqdm
from transformers import AutoModel

dotenv.load_dotenv()
os.environ["HF_TOKEN"] = "HF_TOKEN"

# Connect to MongoDB
uri = os.getenv("MONGO_URI")
client = MongoClient(uri, server_api=ServerApi("1"))
db = client["sample_mflix"]
collection = db.get_collection("movies")

# Connect to LanceDB
lance_uri = "data/movies-data"
lance_db = lancedb.connect(lance_uri)

# Define keys for which to create vector databases
keys_to_embed = [
    "title",
    "genres",
    "cast",
    "fullplot",
    "directors",
    "countries",
]

# Loop over documents from MongoDB
for index, document in tqdm(
    enumerate(
        collection.find(filter={"year": {"$gte": 2005}}).max_await_time_ms(999999)
    )
):
    collection.update_one({"_id": document["_id"]}, {"$set": {"vector_id": index}})

    model = AutoModel.from_pretrained(
        "jinaai/jina-embeddings-v2-base-en", trust_remote_code=True
    ).to("cuda")
    output = model.encode(
        [
            (
                "; ".join(document[key])
                if type(document[key]) == list
                else str(document[key])
            )
            for key in document.keys()
            if key in keys_to_embed
        ]
    )

    for i, key in enumerate([key for key in document.keys() if key in keys_to_embed]):
        if key in document.keys():
            table_name = f"{key}_vectors"
            embeddings = output[i]

            if table_name not in lance_db:
                lance_db.create_table(
                    table_name,
                    data=[
                        {
                            "data": str(document[key]),
                            "index": str(index),
                            "vector": embeddings,
                        }
                    ],
                )
            else:
                table = lance_db.open_table(table_name)
                table.add(
                    [
                        {
                            "data": str(document[key]),
                            "index": str(index),
                            "vector": embeddings,
                        }
                    ]
                )
