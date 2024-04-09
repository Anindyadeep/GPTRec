from RecommendationSystem import RecommendationSystem

# config
rerank_config = {
    "release_year_fuzzy_value": 5,
    "total_recommendations_required": 10,
    "device": "cuda",
    "lance_db_path": "data/movies-data",
}

rs = RecommendationSystem(rerank_config=rerank_config)

# recommend with text
docs = rs.recommend(
    "jedi and sith war, movie by george lucas, released around 2004", True
)

# recommend with json
# docs = rs.recommend(
#     {
#         "release_year": 2007,
#         "directors": ["Jir Menzel"],
#         "actors": [
#             "Ivan Barnev",
#             "Oldrich Kaiser",
#         ],
#         "fullplot": "Czechoslovakia, 1963. Jan Dte is released from prison after serving 15 years. He goes into semi exile in a deserted village near the German border. In flashbacks, he tells his story: he's a small, clever and quick-witted young man, stubbornly nave, a vendor at a train station. Thanks to a patron, he becomes a waiter at upscale hotels and restaurants. We see him discover how the wealthy tick and how to please women. He strives to be a millionaire with his own hotel. Before the war, he meets Lza, a German woman in Prague. Is this his ticket to wealth or his undoing? Meanwhile, we see Jan putting a life together after prison: why was he sentenced, and who will he become?",
#         "genres": ["Comedy", "Drama", "Romance"],
#     }
# )

[print(doc["rank"], doc["title"]) for doc in docs]
