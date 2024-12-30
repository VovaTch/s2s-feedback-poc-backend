import logging
import os
from typing import Any, Callable

from fastapi import FastAPI, HTTPException, Request
from starlette.middleware.cors import CORSMiddleware
import instructor
from openai import OpenAI
import uvicorn
import dotenv

from api.prompts.feedback_request import get_feedback_request
from api.utils.prompting import create_message_openai
from api.schema.feedback import FeedbackResponse, Query
from api.prompts.system import S2S_SYSTEM_PROMPT
from api.database import SessionLocal, engine
from api.schema.lang import Base
from api.seed.data import LANGUAGES

logging.basicConfig(level=logging.INFO)

# Load dotenv
dotenv.load_dotenv(override=True)

# SQL create bases
Base.metadata.create_all(bind=engine)

# FastAPI app creation with CORS middleware
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    # allow_origins=["http://localhost:3000", "http://192.168.1.79:3000"],
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

system_prompt = S2S_SYSTEM_PROMPT


# OpenAI API
client = instructor.from_openai(OpenAI(api_key=os.getenv("OPENAI_API_KEY")))


# Get session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root() -> dict[str, Any]:
    return {"message": "Hello, World!"}


@app.post("/s2s_eval/", response_model=FeedbackResponse)
async def get_response(query: Query) -> FeedbackResponse:
    print(query)
    system_message = create_message_openai("system", system_prompt)
    language = LANGUAGES[query.lang_id]["language"]  # TODO: do it with a database
    print(f"Language: {language}")
    # language = "Spanish" # TODO; debugging
    user_message = create_message_openai(
        "user", get_feedback_request(query.eng_sentence, query.lang_sentence, language)
    )
    response: FeedbackResponse = client.chat.completions.create(
        model="gpt-4o-2024-08-06",
        messages=[system_message, user_message],  # type: ignore
        response_model=FeedbackResponse,
    )
    try:
        return response
    except:
        raise HTTPException(status_code=422, detail="Model response is not valid")

@app.middleware("http")
async def log_requests(request: Request, call_next: Callable) -> Any:
    logger = logging.getLogger("uvicorn")
    logger.info(f"Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    return response


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
