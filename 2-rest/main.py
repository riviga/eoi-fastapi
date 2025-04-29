from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from routers import holamundo, movies
from logger import log

descripcion = "Ingeniería de Datos: API REST"
    
app = FastAPI(
    description=descripcion,
    version="0.1.0",
    title="Máster EOI - FastAPI API REST",
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
                        "name": "holamundo",
                        "description": "Operaciones para saludar"
                    },
                                     {
                        "name": "movies",
                        "description": "Operaciones CRUD sobre películas"
                    }                   
                ]
)

app.include_router(holamundo.router)
app.include_router(movies.router)

@app.get("/", include_in_schema=False)
def redirigir():
    log.info("Petición a /, redirigiendo a /docs...")
    return RedirectResponse(url="/docs")

app.add_middleware(CORSMiddleware, allow_origins="http://localhost:3000", allow_methods=["*"], allow_headers=["*"])

if __name__ == "__main__":
    uvicorn.run("main:app", port=8080, reload=True)
