from pydantic import BaseModel, EmailStr, Field

class HTTPExceptionModel(BaseModel):
    detail: str = Field(description="Error message", example="Client id not found")
