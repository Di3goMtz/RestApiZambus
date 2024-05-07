from pydantic import BaseModel, Field
from datetime import datetime, time, date 
from typing import List, Optional

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

#Servicio REST Empleados
class EmpleadoInsert(BaseModel):
    nombre: str
    apellidos: str
    correo: str
    contraseña: str
    noTelefono: str
    estatus: str
    domicilio: str
    tipoEmpleado: str
    horarioInicio: str
    horarioFin: str
    numeroLicencia: str

class EmpleadoConsulta(BaseModel):
    id: int
    nombre: str
    apellidos: str
    correo: str
    noTelefono: str
    estatus: str
    domicilio: str
    tipoEmpleado: str
    horarioInicio: str
    horarioFin: str
    numeroLicencia: str


#Servicio REST Supervisiones
class Supervision(BaseModel):
    id_ruta: int
    id_checador: int
    fecha_supervision: datetime
    puntos_revision: List[Optional[dict]] = []

class PuntoRevision(BaseModel):
    id_parada: int
    num_corrida: int
    hora_real_llegada: str
    comentario: str

class ModificarSupervision(BaseModel):
    idRuta: int
    idChecador: int
    fechaSupervicion: date

class ModificarPuntoRevision(BaseModel):
    PuntosRevision: List[PuntoRevision]