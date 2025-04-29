from fastapi import APIRouter, HTTPException, Path, Response, status
from model import ResponseError, RecommendedMovies
from httpx import AsyncClient
from util import to_json
from logger import log
import asyncio
import time

'''
Microservice system with async requests
'''

router = APIRouter(tags=["microservices"], prefix="/micro")

no_recommendations = HTTPException(detail="No recommendations", status_code=status.HTTP_404_NOT_FOUND)

async_client = AsyncClient()

FAVOURITE_USER_MOVIE_URL = "http://kv:8000/kv"
SIMILAR_CONTENTS_URL     = "http://predict:8000/title"
SEARCH_MOVIE_URL         = "http://tmdb:8000/search"

HEADERS = {"accept": "application/json"}

@router.get('/user/{client_id}', description="Recommend similar movies to the favourite movie of the client, with metadata from TMDB",
        responses={
            status.HTTP_200_OK: {"description": "Favourite movie and similar movies recommended", "model": RecommendedMovies}, 
            status.HTTP_404_NOT_FOUND: {"description": "Client not found", "model": ResponseError},
            status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal Server Error", "model": ResponseError}            
        })
async def recommend_user_movies(client_id: str = Path(description="Client id", min_length=3, example="Rick")):    
    favourite_movie_list = await asyncio.gather(request_get_favourite(client_id))
    favoutire_movie = favourite_movie_list[0]  
    log.info(f"Favourite movie: {favoutire_movie}")    
    similar_contents_list = await asyncio.gather(request_get_similar_contents(favoutire_movie))             
    log.info(f"Similar movies: {similar_contents_list[0]}")    
    similar_contents = to_json(similar_contents_list[0])    
    movies_search_list = await search_titles(similar_contents)            
    result_search = [to_json(m)[0] for m in movies_search_list]
    log.info(f"result_search size {len(result_search)}")
    return {"favourite": favourite_movie_list[0], "recommended": result_search}


async def request_get_favourite(client_id: str):
    log.info(f"request_get_favourite client {client_id}")
    response = await async_client.get(url = f"{FAVOURITE_USER_MOVIE_URL}/{client_id}", headers={"accept": "application/json", "x-apikey": "supersecretkey"})
    check_response(response, "response_get_favourite")        
    return response.text


async def request_get_similar_contents(movie: str):
    log.info(f"request_get_similar_contents movie {movie}")
    response = await async_client.get(url = f"{SIMILAR_CONTENTS_URL}/{movie}", headers=HEADERS)
    check_response(response, "response_get_similar_contents")    
    return response.text


async def search_titles(list_titles: list):
    log.info(f"search_titles: {list_titles}")
    tasks = [request_search_title(movie_title) for movie_title in list_titles]
    responses = await asyncio.gather(*tasks)    
    log.info(f"search_titles responses: {len(responses)}") 
    if len(responses) == 0:
        raise no_recommendations
    return responses                  
    
    
async def request_search_title(movie_title):
    response = await async_client.get(url = f"{SEARCH_MOVIE_URL}/{movie_title}")    
    check_response(response, "response_search_title")        
    return response.text

def check_response(response: Response, type: str):
    if response.status_code != 200:
        raise no_recommendations    
    log.info(f"{type} [{response.text}]")
    

# NEVER DO THIS!!    
# Blocking call in async route
# Async routes run on the main thread and are expected to never block for any significant period of time.
# sleep() is blocking, so the main thread will stall.
@router.get('/wait-async-block', include_in_schema=False)
async def test():    
    time.sleep(1)
    
# Blocking calls on sync route
# Sync routes are run in a separate thread from a threadpool, so any blocking will not affect the main thread.
@router.get('/wait-block', include_in_schema=False)
def test():    
    time.sleep(1)
    
# Awaiting coroutines on async routes
# Awaiting an async function causes it to yield the main thread while it's waiting for an operation to complete, so it's not blocking the thread.
# asyncio.sleep(), unlike time.sleep(), is an async function, so it can be awaited.
@router.get('/wait-async-no-block', include_in_schema=False)
async def test():    
    await asyncio.sleep(1)

