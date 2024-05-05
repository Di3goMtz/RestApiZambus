from pydantic import BaseModel, Field
from datetime import datetime, time 

class Horarios(BaseModel):
    numCorrida:int
    horaSalida:time
    horaEstimado:time
    
class AgregarParada(BaseModel):
    idParada:int
    nombre:str
    ubicacionLatitud:float
    ubicacionLongitud:float
    horarios:list[Horarios]
