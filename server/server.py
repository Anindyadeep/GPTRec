import os 
import uuid 
import json
from premai import Prem
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException,Query
from fastapi.requests import Request
from fastapi.responses import StreamingResponse
from datetime import datetime
from schemas import RecommendationRequest, RecommendationResponse, ChatRequest, ErrorResponse
from utils import dummy_recommend, prepare_input
from contextlib import asynccontextmanager
from RecommendationSystem import RecommendationSystem as recsys
from mongo import db
from fastapi.middleware.cors import CORSMiddleware

resources = {}
rerank_config = {
    "release_year_fuzzy_value": 5,
    "total_recommendations_required": 10,
    "device": "cuda",
    "lance_db_path": "data/movies-data",
}
mongo_connection_uri = os.environ.get("MONGO_CONNECTION_URI")

rs = recsys(rerank_config=rerank_config)

@asynccontextmanager
async def lifespan(app: FastAPI):
    load_dotenv()
    premai_api_key, premai_project_id = os.environ.get("PREMAI_API_KEY"), os.environ.get("PREMAI_PROJECT_ID")
    resources["client"] = Prem(api_key=premai_api_key)
    resources["project_id"] = premai_project_id
    print(resources)
    yield
    resources.clear()


app = FastAPI(lifespan=lifespan)

# TODO: Need to add a response cache to store user conversation history

@app.get("/api/v1/status")
def status():
    return {"status": "running"}
@app.get("/api/v1/movies")
async def get_movies(page: int = Query(default=1, ge=1), page_size: int = Query(default=100, le=500)):
    skip = (page - 1) * page_size
    movies_cursor = db.get_collection("movies").find({}, {"_id": 1, "title": 1, "poster": 1,"year":1,"fullplot":1,"cast":1,"directors":1,"genres":1}).sort([("imdb.id", -1), ("year", -1)]).skip(skip).limit(page_size) 
    movies_list = []
    for movie in movies_cursor:
        movie['_id'] = str(movie['_id']) 
        movies_list.append(movie)
    return movies_list

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

@app.post(
    "/api/v1/recommend",
    response_model=RecommendationResponse,
    responses={422: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
)
def predict(request: Request, body: RecommendationRequest):
    try:
        result = rs.recommend(body.text,True)
        return {
            "search_id": body.id,
            "response_id": str(uuid.uuid4()),
            "search_query": body.text,
            "search_results": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/vi/watch_history_recommend")
def rec_similar(request:Request,body: RecommendationRequest):
    try:
        result = rs.recommend(body.text,flag="watch_history")
        return {
            "search_id": body.id,
            "response_id": str(uuid.uuid4()),
            "search_query": body.text,
            "search_results": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# TODO: Need to add a response cache to store user conversation history
# TODO: We need to have a better system prompt

@app.post("/api/v1/chat")
async def stream(request: Request, body: ChatRequest):
    
    system_prompt, input_prompt = prepare_input(text=body.query, recommend_results=None)
    messages = [{"role": "user", "content": input_prompt}]
    
    async def _stream():
        response = resources["client"].chat.completions.create(
            project_id=resources["project_id"],
            messages=messages,
            temperature=body.temperature,
            max_length=body.max_length,
            system_prompt=system_prompt,
            stream=True
        )
        for chunk in response:
            if text:= chunk.choices[0].delta["content"]:
                data = {"request_id":body.id, "response_id": str(uuid.uuid4()), "text": text}
                yield json.dumps(data) + "\n"
    return StreamingResponse(_stream(), media_type="text/event-stream")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Set this to the appropriate list of origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == '__main__':
    import uvicorn 
    uvicorn.run(app, host="0.0.0.0", port=8000)