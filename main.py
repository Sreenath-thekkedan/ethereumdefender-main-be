from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from http import HTTPStatus
from models.request_models import VerifyRequest
from models.response_models import VerifyResponse
from services.service import verify_block
from models.exceptions import BlockNotFoundException
from requests.exceptions import RequestException

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    response = Response(content="", status_code=HTTPStatus.NO_CONTENT)
    return response

@app.post("/verify", response_model=VerifyResponse)
async def verify_hash(request_data: VerifyRequest):
    # Get the hash from the request
    input_hash = request_data.hash
    try:
        is_phished = verify_block(input_hash)
        return {"is_phished": is_phished}
    except BlockNotFoundException:
        raise HTTPException(status_code=404, detail="Block not found")
    except RequestException:
        raise HTTPException(status_code=512, detail="Could not connect to network")