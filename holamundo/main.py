import uvicorn
from fastapi import Path, Query, Response, status, FastAPI
from enum import Enum

descripcion = "Ingeniería de Datos: API HolaMundo"
    
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
    }
)

@app.get(path="/hola", summary="Método GET que dice Hola", tags=["hola"])
def hola():
    return {"msg": "Hola Mundo!"}


@app.get(path="/hola/todos", summary="Método GET que dice Hola a todos", tags=["hola"])
def hola():
    return "OK" 


@app.get(path="/hola/error", summary="Método GET que produce un error interno")
def hola(edad: int):
    edad_infinita = edad / 0
    return "OK"


class ColorEnum(str, Enum):
    rubio = "rubio"
    moreno = "moreno"
    pelirrojo = "pelirrojo"


@app.get(path="/hola/color/{color}", summary="Método GET que dice Hola a un color de pelo")
def hola(color: ColorEnum = Path(description="Tipo de pelo")):
    return {"msg": f"Hola {color.name}!"}


@app.get(
    path="/hola/hola-si-hay-alguien",
    summary="Método GET que dice Hola si hay alguien",
    response_description="Se responde porque hay alguien",
    responses={
        status.HTTP_200_OK: {"description": "Respuesta OK porque hay alguien"},
        status.HTTP_404_NOT_FOUND: {"description": "No hay nadie"},
    },
)
def hola(response: Response, alguien: bool = Query(description="Indicador de si hay alguien", examples=["true"], default=False)):
    if alguien:
        return {"msg": f"Hola, porque hay alguien!"}
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"msg": "No hay nadie"}
    

@app.get(path="/hola/{edad}", summary="Método GET que dice hola según la edad")
def hola(nombre: str, edad: int):
    if edad <= 42:
        return {"msg": f"Hola jovencito {nombre}!"}
    else:
        return {"msg": f"Hola no tan joven Sr. {nombre}"}
    

if __name__ == "__main__":
    uvicorn.run("main:app", port=8080, reload=True)