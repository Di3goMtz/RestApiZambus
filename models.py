from pydantic import BaseModel, Field
from datetime import datetime, time 

class Horarios(BaseModel):
    numCorrida:int
    horaSalida:time
    horaEstimado:time

class AgregarParada(BaseModel):
    nombre:str
    ubicacionLatitud:float
    ubicacionLongitud:float
    horarios:list[Horarios]

class Parada(BaseModel):
    idParada:int
    nombre:str
    ubicacionLatitud:float
    ubicacionLongitud:float
    horarios:list[Horarios]

class VigenciaTarifa(BaseModel):
    fechaInicio:datetime
    fechaFin:datetime

class Tarifas(BaseModel):
    idTarifa:int
    precioTarifa:int
    nombreTarifa:str
    reglaAplicabilidad:str
    vigenciaTarifa:list[VigenciaTarifa]

class AgregarRuta(BaseModel):
    nombre:str
    tiempoEstimadoViaje:int
    inicioRuta:str
    finRuta:str
    idAutobus:int
    tarifas:list[Tarifas]
    paradas:list[Parada]
    idChecador:int