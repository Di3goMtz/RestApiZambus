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

class ParadaOut(BaseModel):
    nombre:str
    ubicacionLatitud:float
    ubicacionLongitud:float
    horarios:list[Horarios]

class Parada(BaseModel):
    nombre:str
    ubicacionLatitud:float
    ubicacionLongitud:float
    horarios:list[Horarios]

class VigenciaTarifa(BaseModel):
    idVigencia:int
    fechaInicio:datetime
    fechaFin:datetime

class Tarifas(BaseModel):
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
    idChecador:int

class ModificarRuta(BaseModel):
    nombre:str
    tiempoEstimadoViaje:int
    inicioRuta:str
    finRuta:str
    idAutobus:int
    idChecador:int