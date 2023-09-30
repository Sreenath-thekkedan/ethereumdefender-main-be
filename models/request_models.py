from pydantic import BaseModel

# Request model for the verify POST request
class VerifyRequest(BaseModel):
    hash: str