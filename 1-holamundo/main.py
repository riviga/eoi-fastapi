import uvicorn
from routers import holamundo
from fastapi import FastAPI 

descripcion = "Ingeniería de Datos: API HolaMundo con FastAPI"
    
app = FastAPI(
    description=descripcion,
    version="0.1.0",
    title="Máster EOI - API HolaMundo",
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
                        "description": "Introducción a métodos y parámetros con FastAPI"
                    }
                ]
)

app.include_router(holamundo.router)


if __name__ == "__main__":
    uvicorn.run("main:app", port=8080, reload=True)