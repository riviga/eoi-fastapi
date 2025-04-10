from fastapi import APIRouter, Path, Query, Response, status
from enum import Enum

'''
Simple API methods and parameters
'''

router = APIRouter(tags=["holamundo"], prefix="/hola")

@router.get(path="/sencillo", summary="Método GET que dice Hola")
def hola():
    return {"msg": "Hola Mundo!"}


@router.get(path="/todos", summary="Método GET que dice Hola a todos")
def hola():
    return "OK" 

@router.get(path="/error", summary="Método GET que produce un error interno")
def hola(edad: int):
    edad_infinita = edad / 0
    return "OK"


class ColorEnum(str, Enum):
    rubio = "rubio"
    moreno = "moreno"
    pelirrojo = "pelirrojo"


@router.get(path="/color/{color}", summary="Método GET que dice Hola a un color de pelo")
def hola(color: ColorEnum = Path(description="Tipo de pelo")):
    return {"msg": f"Hola {color.name}!"}


@router.get(
    path="/hola-si-hay-alguien",
    summary="Método GET que dice Hola si hay alguien",
    response_description="Se responde porque hay alguien",
    responses={
        status.HTTP_200_OK: {"description": "Respuesta OK porque hay alguien"},
        status.HTTP_404_NOT_FOUND: {"description": "No hay nadie"},
    },
)
def hola(response: Response, alguien: bool = Query(description="Indicador de si hay alguien", example="true", default=False)):
    if alguien:
        return {"msg": f"Hola, porque hay alguien!"}
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"msg": "No hay nadie"}
    

@router.get(path="/{edad}", summary="Método GET que dice hola según la edad")
def hola(nombre: str, edad: int):
    if edad <= 42:
        return {"msg": f"Hola jovencito {nombre}!"}
    else:
        return {"msg": f"Hola no tan joven Sr. {nombre}"}
    