import uuid
from datetime import datetime
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from contextlib import asynccontextmanager

from schemas import RecommendationRequest, RecommendationResponse, ErrorResponse
from recsys.recsys import RecommendationSystem
from config import RecSysConfig, ReRankConfig
from recsys.mongo import db

resources = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_dotenv()

    resources["client"] = RecommendationSystem(
        config=RecSysConfig(), rerank_config=ReRankConfig()
    )
    yield
    resources.clear()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Set this to the appropriate list of origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# TODO: Need to add a response cache to store user conversation history


@app.get("/api/v1/status")
def status():
    return {"status": "running"}


@app.post(
    "/api/v1/recommend",
    response_model=RecommendationResponse,
    responses={422: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
)
def predict(request: Request, body: RecommendationRequest):
    try:
        result = resources["client"].recommend(body.query, show_structured_json=False)
        response_data = {
            "search_id": body.id,
            "response_id": str(uuid.uuid4()),
            "search_query": body.query,
            "search_results": {"num_result": len(result), "result": result},
        }
        return response_data
    except Exception as e:
        import traceback
        traceback_str = traceback.format_exc()
        error_detail = f"Error occurred: {str(e)}"

        raise HTTPException(status_code=500, detail=error_detail+"\n"+traceback_str)


# endpoint to fetch all movies in a paginated manner for home page
@app.get("/api/v1/movies")
async def get_movies(
    page: int = Query(default=1, ge=1), page_size: int = Query(default=100, le=500)
):
    skip = (page - 1) * page_size
    movies_cursor = (
        db.get_collection("movies")
        .find(
            {},
            {
                "_id": 1,
                "title": 1,
                "poster": 1,
                "year": 1,
                "fullplot": 1,
                "cast": 1,
                "directors": 1,
                "genres": 1,
            },
        )
        .sort([("imdb.id", -1), ("year", -1)])
        .skip(skip)
        .limit(page_size)
    )
    movies_list = []
    for movie in movies_cursor:
        movie["_id"] = str(movie["_id"])
        movies_list.append(movie)
    return movies_list


# fetch all details for a specific movie as well as insert in watch history collection
@app.get("/api/v1/movie/{movie_id}")
async def get_movie(movie_id: str):
    query = {"_id": movie_id}
    movie = db.get_collection("movies").find_one(query)
    db.get_collection("watch-history").update_one(
        {"movieId": movie_id}, {"$set": {"timestamp": datetime.now()}}, upsert=True
    )
    if movie:
        return movie
    else:
        raise HTTPException(status_code=404, detail="Movie not found")


# endpoint for fetching docs from the user's watch history  that are also similar.
@app.post(
    "/api/v1/watch_history_recommend",
    response_model=RecommendationResponse,
    responses={422: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
)
def rec_similar(request: Request, body: RecommendationRequest):
    try:
        result = resources["client"].recommend(body.text, flag="watch_history")
        return {
            "search_id": body.id,
            "response_id": str(uuid.uuid4()),
            "search_query": body.text,
            "search_results": result,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
