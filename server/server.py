import os 
import uuid 
import json
from premai import Prem
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.requests import Request
from fastapi.responses import StreamingResponse

from schemas import RecommendationRequest, RecommendationResponse, ChatRequest, ErrorResponse
from utils import dummy_recommend, prepare_input
from contextlib import asynccontextmanager

resources = {}

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

@app.post(
    "/api/v1/recommend",
    response_model=RecommendationResponse,
    responses={422: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
)
def predict(request: Request, body: RecommendationRequest):
    try:
        result = dummy_recommend(search_id=body.id, query=body.query)
        return {
            "search_id": body.id,
            "response_id": str(uuid.uuid4()),
            "search_query": body.query,
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


if __name__ == '__main__':
    import uvicorn 
    uvicorn.run(app, host="0.0.0.0", port=8000)