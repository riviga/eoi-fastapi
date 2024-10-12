from fastapi import APIRouter, HTTPException, Path, status
from model import MovieTMDB
from model import ResponseError, MovieTMDB
from logger import log
from httpx import AsyncClient
from settings import settings
import requests

'''
Public API wrapper with blocking requests
'''

router = APIRouter(tags=["the-movie-database"])

URL = "https://api.themoviedb.org/3"
HEADERS = {"accept": "application/json"}

async_client = AsyncClient()

http_500 = HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Internal Server Error')
    
fields = ["id", "title", "vote_average", "original_title", "release_date"]
        
@router.get('/search/{title}', description="Search movies by title using TMDB Public API",
        responses={
            status.HTTP_200_OK: {"description": "List of movies maching name", "model": list[MovieTMDB]}, 
            status.HTTP_401_UNAUTHORIZED: {"description": "You need to send credentials", "model": ResponseError},
            status.HTTP_404_NOT_FOUND: {"description": "Movie not found", "model": ResponseError},
            status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal Server Error", "model": ResponseError}            
        })
async def search_movie_title(title: str = Path(description="Movie title", min_length=1, example="Back to the future")):
    try:
        title_url_encoded = title.replace(' ', "%20")        
        search_url = f"{URL}/search/movie?api_key={settings.api_key}&include_adult=false&language=es-ES&page=1&query={title_url_encoded}"
        response_json = await send_get_request(search_url)                      
        return [MovieTMDB(**{key:result[key] for key in fields}) for result in response_json["results"]]             
    except Exception as ex:
        log.error(f"Exception search_movie_title {title} - {ex}")
        raise http_500    
    
    
@router.get('/movie/{movie_id}', description="Get movie info from TMDB Public API",
        responses={
            status.HTTP_200_OK: {"description": "Movie info"}, 
            status.HTTP_401_UNAUTHORIZED: {"description": "You need to send credentials", "model": ResponseError},
            status.HTTP_404_NOT_FOUND: {"description": "Movie not found", "model": ResponseError},
            status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal Server Error", "model": ResponseError}            
        })
async def get_movie_info(movie_id: int = Path(description="Movie id in TMDB", min=1, example=165)):
    try:
        get_url = f"{URL}/movie/{movie_id}?api_key={settings.api_key}"
        return await send_get_request(get_url)
    except Exception as ex:
        log.error(f"Exception get_movie_info {movie_id} - {ex}")
        raise http_500   

    
async def send_get_request(url: str):
    log.info(f"GET {url}")
    # response = requests.get(url, headers=HEADERS)            
    response = await async_client.get(url, headers=HEADERS)    
    check_response_status(response.status_code)        
    response_json = response.json()                
    log.info(response_json)
    return response_json


def check_response_status(status_code: status):
    if status_code == status.HTTP_401_UNAUTHORIZED:
        raise HTTPException(detail="You need to send credentials", status_code=status.HTTP_401_UNAUTHORIZED)         
    if status_code == status.HTTP_404_NOT_FOUND:
        raise HTTPException(detail="Movie not found", status_code=status.HTTP_404_NOT_FOUND)         
    if status_code != status.HTTP_200_OK:
        raise HTTPException(detail="Error invocando TMDB", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)       