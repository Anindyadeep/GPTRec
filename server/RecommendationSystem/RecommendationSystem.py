import subprocess
import dotenv
import json
import copy
import os

import gdown
import lancedb
from premai import Prem
from transformers import AutoModel
from pymongo.server_api import ServerApi
from pymongo.mongo_client import MongoClient


class RecommendationSystem:
    dotenv.load_dotenv("../../.env")

    model_id = os.environ.get("HF_MODEL_ID")
    prem_api_key = os.environ.get("PREM_API_KEY")
    prem_project_id = os.environ.get("PREM_PROJECT_ID")
    mongo_connection_uri = os.environ.get("MONGO_CONNECTION_URI")

    def __init__(
        self,
        rerank_config,
    ):
        device = rerank_config["device"]
        self.rerank_config = rerank_config
        self.client = Prem(api_key=self.prem_api_key)

        url = "https://drive.google.com/uc?id=1HpM0rWT9SZr8MTeJ_KMG9G9utWDVn0Qk"
        output = "./server/RecommendationSystem/data.zip"
        data_output_path = "./server/RecommendationSystem/."
        data_path = "./server/RecommendationSystem/data"

        gdown.download(url, output)
        subprocess.run(["unzip", str(output), "-d", data_output_path])

        self.model = AutoModel.from_pretrained(
            self.model_id, trust_remote_code=True
        ).to(device)

        self.lance_db = lancedb.connect(data_path)
        self.fullplot_vectors = self.lance_db.open_table("fullplot_vectors")

    def prompt_generator(self, message):
        prompt = (
            f"""TASK: Given the text, return a json in the OUTPUT_FORMAT form the text QUERY_MESSAGE. All the content from the JSON should
        be from the QUERY_MESSAGE only.

        OUTPUT_FORMAT:
        json```
        """
            + """{"""
            + """
        "release_year": // year in which movie was released, if mentioned in QUERY_MESSAGE else ""
        "directors": // list of directors, else []
        "actors": // list of directors, else []
        "fullplot": // description of the movie, else ""
        "genres": // list of genres of movie from the QUERY_MESSAGE, the genres should be one of these ['News', 'Talk-Show', 'Comedy', 'Drama', 'Thriller', 'Family', 'History', 'Fantasy', 'Musical', 'War', 'Horror', 'Action', 'Adventure', 'Romance', 'Biography', 'Animation', 'Short', 'Sci-Fi', 'Western', 'Crime', 'Documentary', 'Film-Noir', 'Mystery', 'Music', 'Sport'], else []
        """
            + """}"""
            + f"""```

        QUERY_MESSAGE: {message}
        """
        )

        return prompt

    def parse(self, response):
        response = response[0].to_dict()
        string = (
            response["message"]["content"]
            .replace("json", "")
            .replace("```", "")
            .replace("OUTPUT_FORMAT:", "")
            .replace("\n", "")
        )
        result = json.loads(string)

        return result

    def generate(self, message):
        messages = [
            {"role": "user", "content": self.prompt_generator(message)},
        ]

        response = self.client.chat.completions.create(
            project_id=self.prem_project_id, messages=messages, temperature=1.0
        )
        response = self.parse(response.choices)
        return response

    def get_data_from_mongo(self, query):
        client = MongoClient(self.mongo_connection_uri, server_api=ServerApi("1"))
        db = client["gpt_rec"]
        collection = db.get_collection("movies")
        result = collection.find(query)

        return result

    def rerank(self, query_json, docs, search_results):
        for result in search_results:
            del result["vector"]
            result["mongo_doc"] = [
                doc for doc in docs if int(doc["vector_id"]) == int(result["index"])
            ][0]

        all_indexes = [int(result["index"]) for result in search_results]
        org_docs = copy.copy(search_results)
        final_docs = search_results

        if query_json.get("release_year"):
            release_year = int(query_json.get("release_year"))
            fuzzy_range = self.rerank_config["release_year_fuzzy_value"]
            filtered_list = []
            for doc in final_docs:
                if doc["mongo_doc"].get("released") and (
                    (release_year - fuzzy_range)
                    <= int(doc["mongo_doc"]["released"]["$date"].split("-")[0])
                    <= (release_year + fuzzy_range)
                ):
                    filtered_list.append(doc)
            final_docs = filtered_list

        if query_json.get("directors"):
            directors = query_json.get("directors")
            final_docs = [
                doc
                for doc in final_docs
                if (
                    len(
                        list(set(directors).intersection(doc["mongo_doc"]["directors"]))
                    )
                    > 0
                )
            ]

        if query_json.get("actors"):
            actors = query_json.get("actors")
            final_docs = [
                doc
                for doc in final_docs
                if (len(list(set(actors).intersection(doc["mongo_doc"]["cast"]))) > 0)
            ]

        if query_json.get("genres"):
            genres = query_json.get("genres")
            final_docs = [
                doc
                for doc in final_docs
                if (len(list(set(genres).intersection(doc["mongo_doc"]["genres"]))) > 0)
            ]

        if len(final_docs) >= self.rerank_config["total_recommendations_required"]:
            final_docs = final_docs[
                self.rerank_config["total_recommendations_required"]
            ]
        else:
            final_docs = sorted(final_docs, key=lambda x: x["_distance"])
            indexes = [int(doc["index"]) for doc in final_docs]
            rem_indexes = [index for index in all_indexes if index not in indexes]

            remaining_docs = [
                doc for doc in org_docs if int(doc["index"]) in rem_indexes
            ]
            remaining_docs = sorted(remaining_docs, key=lambda x: x["_distance"])

            for doc in remaining_docs[
                : (self.rerank_config["total_recommendations_required"] - len(indexes))
            ]:
                final_docs.append(doc)

        results = []
        for index, doc in enumerate(final_docs):
            new_doc = doc["mongo_doc"]
            new_doc["rank"] = index
            results.append(new_doc)

        return results

    def recommend(self, input, show_structured_json=False):
        if type(input) == dict:
            response_json = input
        else:
            response_json = self.generate(input)
            response_json["fullplot"] = input
            print(response_json) if show_structured_json else ...

        total_recommendations_required = self.rerank_config[
            "total_recommendations_required"
        ]
        embeddings = self.model.encode(response_json["fullplot"])
        result = self.fullplot_vectors.search(embeddings).limit(
            total_recommendations_required * 2
        )

        docs = [
            doc
            for doc in self.get_data_from_mongo(
                {
                    "vector_id": {
                        "$in": [int(x) for x in list(result.to_df()["index"].values)]
                    }
                }
            )
        ]
        reranked_docs = self.rerank(
            query_json=response_json, docs=docs, search_results=result.to_list()
        )

        return reranked_docs
