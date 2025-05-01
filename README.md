# EOI Master - FastAPI 

## How to run specific API
1. Go specific API folder (ex. "/holamundo")
2. Run
    - Local app: `python main.py`. Swagger UI: http://localhost:8080/docs
    - Docker container: `docker-compose up -d`. Swagger UI: http://localhost:8000/docs
    
### To use TMDB wrapper API (/tmdb)
1. Register in TMDB for API key in https://www.themoviedb.org/settings/api
2. Create /tmdb/.env file with API_KEY_VALUE={value of TMDB apikey}

## How to run all apps in "production" mode (pulling images from DockerHub)
1. Start: `docker-compose up -d`
2. Stop: `docker-compose down`

## How to run all apps in "development" mode (local containers started from built images with volumes for code auto-reload)
1. Start: `docker compose -f .\docker-compose-dev.yml up -d --build`
2. Stop: `docker-compose -f .\docker-compose-dev.yml down`

Swagger UI: 
- HolaMundo:    http://localhost:8000/docs
- REST:         http://localhost:8001/docs
- Clave-valor:  http://localhost:8002/docs
- Prediction:   http://localhost:8003/docs
- TMDB:         http://localhost:8004/docs
- Microservices: http://localhost:8006/docs
