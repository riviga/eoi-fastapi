import time
from fastapi import APIRouter, HTTPException, Path, Query, status
from logger import log
from model import ResponseError
import pandas as pd
import joblib
import random
import asyncio

'''
ML prediction functionality with FastAPI
'''

router = APIRouter(tags=["recommendation"])

similarity = joblib.load('recommend/similarity') 
df = pd.read_csv('recommend/movies_dataframe.csv')[['i', 'title']]
title_list = df['title'].to_list()
        
@router.get('/titles', description="Get list of movie titles to recommend",
        responses={
            status.HTTP_200_OK: {"description": "List of movie titles", "model": list[str]},             
            status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal Server Error", "model": ResponseError}            
        })
def get_title_list(
        limit: int = Query(description="Number of results", default=None, example=10),
        shuffle: bool = Query(description="Shuflle results", default=False)):
    log.info(f"Get title list limit {limit} shuffle {shuffle}")    
    return_list = get_shuffled_list(shuffle)    
    return return_list[:limit] if limit else return_list        

def get_shuffled_list(shuffle: bool):
    if shuffle:
        return_list = title_list.copy()
        random.shuffle(return_list)
        return return_list
    return title_list       

        
@router.get('/title/{title}', description="Get the titles of 10 similar movies",
        responses={
            status.HTTP_200_OK: {"description": "List of similar movie titles", "model": list[str]}, 
            status.HTTP_404_NOT_FOUND: {"description": "Movie not found", "model": ResponseError},
            status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal Server Error", "model": ResponseError}            
        })
def get_similar_movies(title: str = Path(description="Movie title", min_length=1, example="Interstellar")):
    #await asyncio.sleep(2)
    #time.sleep(2)
    if not title in title_list:
        raise HTTPException(detail=f"Movie {title} not found", status_code=status.HTTP_404_NOT_FOUND)
    index = df[df['title'] == title].index[0]
    distances = similarity[index]
    recommendation_list = [df.iloc[i].title for i in distances[:10]]
    return recommendation_list
        
