from pydantic import BaseModel, EmailStr, Field

class ResponseError(BaseModel):
    detail: str = Field(description="Error message", example="Client id not found")
