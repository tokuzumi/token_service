from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from app.access_token import AccessToken, VideoGrant
from pydantic import BaseModel

load_dotenv()

LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY")
LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET")
LIVEKIT_WS_URL = os.getenv("LIVEKIT_WS_URL")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"^https:\/\/.*\.aivoice\.com\.br$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TokenRequest(BaseModel):
    solution: str
    clientId: str
    userId: str

@app.post("/")
async def generate_token(data: TokenRequest):
    if not (data.solution and data.clientId and data.userId):
        raise HTTPException(status_code=400, detail="solution, clientId e userId são obrigatórios")

    identity = f"{data.solution}-{data.clientId}-{data.userId}"
    room = identity

    try:
        at = AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET, identity=identity)
        at.add_grant(VideoGrant(room_join=True, room=room))
        token = at.to_jwt()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "token": token,
        "room": room,
        "identity": identity,
        "apiKey": LIVEKIT_API_KEY
    }
