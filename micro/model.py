from pydantic import BaseModel, Field

class HTTPExceptionModel(BaseModel):
    detail: str = Field(description="Error message", example="Client id not found")
    
    
class MovieTMDB(BaseModel):
    id: int = Field(description="Client's favourite movie", example = 165)
    title: str = Field(description="Client's favourite movie", example = "Regreso al futuro: Parte II")
    original_title: str = Field(description="Client's favourite movie", example = "Back to the Future Part II")
    vote_average: float = Field(description="Client's favourite movie", example = 7.764)
    release_date: str = Field(description="Release date", example = "1989-11-22")
    
    
class RecommendedMovies(BaseModel):
    favourite: str = Field(description="Client's favourite movie", example = "Back to the future")
    recommended: list[MovieTMDB] = Field(description="List of recommendations based on client's favourite movie")
