import uuid
from datetime import datetime
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from contextlib import asynccontextmanager
import uvicorn
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

# endpoint to fetch all movies in a paginated manner for home page
@app.get("/api/v1/movies")
async def get_movies(page: int = Query(default=1, ge=1), page_size: int = Query(default=100, le=500)):
    skip = (page - 1) * page_size
    # movies_cursor = db.get_collection("movies").find({}, {"_id": 1, "title": 1, "poster": 1,"year":1,"fullplot":1,"cast":1,"directors":1,"genres":1}).sort([("imdb.id", -1), ("year", -1)]).skip(skip).limit(page_size) 
    pipeline = [
        {
            "$project": {
                "_id": 1,
                "title": 1,
                "poster": 1,
                "year": 1,
                "fullplot": 1,
                "cast": 1,
                "directors": 1,
                "genres": 1,
                "countries": 1,
                "rating": "$imdb.rating",
            }
        },
        {
            "$sort": {"rating": -1, "year": -1}
        },
        {
            "$skip": skip
        },
        {
            "$limit": page_size
        }
    ]

    movies_cursor = db.get_collection("movies").aggregate(pipeline)
    movies_list = []
    for movie in movies_cursor:
        movie['_id'] = str(movie['_id']) 
        movies_list.append(movie)
    return movies_list

#fetch all details for a specific movie as well as insert in watch history collection
@app.get("/api/v1/movie/{movie_id}")
async def get_movie(movie_id: str):
    query = {"_id": movie_id}
    movie = db.get_collection("movies").find_one(query)
    db.get_collection("watch-history").update_one(
    {"movieId": movie_id},
    {"$set": {"timestamp": datetime.now()}},
    upsert=True
    )
    if movie:
        return movie
    else:
        raise HTTPException(status_code=404, detail="Movie not found")

#endpoint to fetch all similar movies either based on text input (eg: show me movies about old men who can do magic) or json based input as a list similar to the input in the test script
@app.post(
    "/api/v1/recommend",
    response_model=RecommendationResponse,
    responses={422: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
)
def predict(request: Request, body: RecommendationRequest):
    try:
        if body.objs:
            query = body.objs[0]
        else:
            query=body.text
        result = resources["client"].recommend(body.query, show_structured_json=False)
        return {
            "search_id": body.id,
            "response_id": str(uuid.uuid4()),
            "search_query": str(query),
            "search_results": {"num_result": len(result), "result": result},
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# #endpoint for fetching docs from the user's watch history  that are also similar.
@app.post("/api/v1/watch_history_recommend", response_model=RecommendationResponse,
    responses={422: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
)
def rec_similar(request:Request,body: RecommendationRequest):
    try:
        if body.objs:
            query = body.objs[0]
        else:
            query=body.text
        result = resources["client"].recommend(body.text, flag="watch_history")
        return {
            "search_id": body.id,
            "response_id": str(uuid.uuid4()),
            "search_query": str(query),
             "search_results": {"num_result": len(result), "result": result},

        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# # TODO: Need to add a response cache to store user conversation history
# # TODO: We need to have a better system prompt

# @app.post("/api/v1/chat")
# async def stream(request: Request, body: ChatRequest):
    
#     system_prompt, input_prompt = prepare_input(text=body.query, recommend_results=None)
#     messages = [{"role": "user", "content": input_prompt}]
    
#     async def _stream():
#         response = resources["client"].chat.completions.create(
#             project_id=resources["project_id"],
#             messages=messages,
#             temperature=body.temperature,
#             max_length=body.max_length,
#             system_prompt=system_prompt,
#             stream=True
#         )
#         for chunk in response: 
#             if text:= chunk.choices[0].delta["content"]:
#                 data = {"request_id":body.id, "response_id": str(uuid.uuid4()), "text": text}
#                 yield json.dumps(data) + "\n"
#     return StreamingResponse(_stream(), media_type="text/event-stream")

if __name__ == '_main_':
    uvicorn.run(app, host="0.0.0.0", port=8000)