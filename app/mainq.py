from fastapi import FastAPI
from fastapi.responses import Response
from http import HTTPStatus
# from models.request_models import VerifyRequest
# from models.response_models import VerifyResponse
# from services.service import verify_block
from ..models.request_models import VerifyRequest
from ..models.response_models import VerifyResponse
from ..services.service import verify_block

app = FastAPI()

@app.get("/health")
async def health_check():
    response = Response(content="", status_code=HTTPStatus.NO_CONTENT)
    return response

@app.post("/verify", response_model=VerifyResponse)
async def verify_hash(request_data: VerifyRequest):
    # Get the hash from the request
    input_hash = request_data.hash

    is_phished = verify_block(input_hash)

    return {"is_phished": is_phished}

def is_hash_valid(hash_value: str) -> bool:
    # Implement your hash verification logic here
    # Return True if the hash is valid, False otherwise
    # Example: You can perform any validation checks you need
    return True  # Placeholder for the example