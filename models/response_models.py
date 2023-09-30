from pydantic import BaseModel

# Response model for the verify request
class VerifyResponse(BaseModel):
    is_phished: bool