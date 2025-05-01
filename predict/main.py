from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exception_handlers import http_exception_handler
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse, RedirectResponse
import uvicorn
from routers import recommendation
from logger import log
from elasticapm.contrib.starlette import ElasticAPM, make_apm_client

descripcion = '''
Ingeniería de Datos: Caso uso predicción modelo

Forked from [Repo](https://github.com/Vishal-Kamath/movie-recommedation-system/tree/master)
'''

@asynccontextmanager
async def lifespan(app: FastAPI):    
    log.info(f"FastAPI app started with movie title list size [{len(recommendation.title_list)}]")
    yield
    log.info("FastAPI app stopped")
    
app = FastAPI(
    description=descripcion,
    version="0.1.0",
    title="Máster EOI - FastAPI API predicción modelo",
    contact={
        "name": "Ricardo Vilchez",
        "url": "https://rickandmortyapi.com/",
        "email": "riviga77@gmail.com",
    },
    license_info={
        "name": "GPLv3",
        "url": "https://www.gnu.org/licenses/gpl-3.0.en.html", 
    }, 
    openapi_tags= [   
                    {
                        "name": "recommendation",
                        "description": "Recomendaciones de películas similares con modelo entrenado"                        
                    }
                ],
    lifespan=lifespan
)

def custom_openapi():
    if not app.openapi_schema:
        app.openapi_schema = get_openapi(
            title=app.title,
            version=app.version,
            openapi_version=app.openapi_version,
            description=app.description,
            terms_of_service=app.terms_of_service,
            contact=app.contact,
            license_info=app.license_info,
            routes=app.routes,
            tags=app.openapi_tags,
            servers=app.servers,
        )
    for _, method_item in app.openapi_schema.get('paths').items():
        for _, param in method_item.items():
            responses = param.get('responses')
            # remove 422 response, also can remove other status code
            if '422' in responses:
                del responses['422']
                
    schemas = app.openapi_schema.get('components').get('schemas')        
    # remove 422 schemas
    for schema_borrar in ["ValidationError", "HTTPValidationError"]:
        if schema_borrar in schemas.keys():                
            del schemas[schema_borrar]                                    
    app.openapi_schema['components']['schemas'] = schemas
        
    return app.openapi_schema

app.openapi = custom_openapi

app.include_router(recommendation.router)

@app.get("/", include_in_schema=False)
def redirigir():
    log.info("Petición a /, redirigiendo a /docs...")
    return RedirectResponse(url="/docs")

# APM
apm = make_apm_client({
    'SERVICE_NAME': 'fastapi-predict',
    'DEBUG': True,
    'SERVER_URL': 'https://99d3dc1c9c6a4587bceeb60ff53a396e.apm.us-central1.gcp.cloud.es.io',
    'CAPTURE_HEADERS': True,
    'CAPTURE_BODY': 'all',
    'SECRET_TOKEN': 'oEf3iQPk7wZQEMhrFU',
    'ENVIRONMENT': 'rvg-dev'
})

app.add_middleware(ElasticAPM, client=apm)

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    log.info(f"Caputando HTTPException motivo {exc.detail}")
    apm.capture_exception()
    return await http_exception_handler(request, exc)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request,exc: RequestValidationError):
    detail = "{}".format(str([i for i in exc.errors()][0]['msg']) + ": " + str([i for i in exc.errors()][0]['loc']))
    log.info(f"Caputando RequestValidationError motivo {detail}")
    apm.capture_exception()
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail": detail})


if __name__ == "__main__":
    uvicorn.run("main:app", port=8080, reload=True)
