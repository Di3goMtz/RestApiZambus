from fastapi import FastAPI, Body, HTTPException
from models import AgregarParada, AgregarRuta, ModificarRuta, ParadaOut, Horarios, Tarifas, VigenciaTarifa, EmpleadoInsert, Supervision, PuntoRevision, ModificarPuntoRevision, ModificarSupervision
from dao import Conection, Conexion
import uvicorn
from bson import ObjectId
from pydantic import BaseModel
from typing import List, Optional
from datetime import date

app = FastAPI()

@app.on_event('startup')
def startup():
    app.cn=Conection()
    print("inicio conexion")

@app.on_event('shutdown')
def shutdown():
    app.cn.close()
    print("fin conexion")

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/rutas/Agregar")
def AgregarRuta(ruta:AgregarRuta):
    salida=app.cn.insertarRuta(ruta)
    return salida

@app.get("/rutas/Consultar")
def obtenerRutas():
    rutas = app.cn.obtenerRutas()
    return rutas

@app.get("/rutas/Consultar/{id:int}")
def obtenerRuta(id:int):
    ruta = app.cn.obtenerRuta(id)
    return ruta

@app.put("/rutas/Modificar/{id:int}")
def modificarRuta(id:int, ruta:ModificarRuta):
    ruta_modificada = app.cn.modificarRuta(id, ruta)
    return ruta_modificada

@app.delete("/rutas/Eliminar/{id:int}")
def eliminarRuta(id:int):
    mensaje = app.cn.eliminarRuta(id)
    return mensaje

@app.put("/rutas/Agregar/Parada")
def AgregarParada(id:int, parada:AgregarParada):
    salida=app.cn.insertarParada(id, parada)
    return salida

@app.put("/rutas/Eliminar/Parada/{idRuta:int}/{idParada:int}")
def eliminarParada(idRuta:int, idParada:int):
    mensaje = app.cn.eliminarParada(idRuta, idParada)
    return mensaje

@app.put("/rutas/Modifica/Parada/{idRuta:int}/{idParada:int}")
def modificarParada(idRuta:int, idParada:int, parada:ParadaOut):
    paradaModificar = app.cn.modificarParada(idRuta, idParada, parada)
    return paradaModificar

@app.get("/rutas/Paradas/{idRuta:int}")
def obtenerParadas(idRuta:int):
    paradas=app.cn.obtenerParadas(idRuta)
    return paradas

@app.get("/rutas/Paradas/{idRuta:int}/{idParada:int}")
def obtenerParada(idRuta:int, idParada:int):
    paradas=app.cn.obtenerParadaEspecifica(idRuta, idParada)
    return paradas

@app.put("/rutas/Paradas/AgregarHorario/{idRuta:int}/{idParada:int}")
def agregarHorario(idRuta:int, idParada:int, horario:Horarios):
    salida=app.cn.insertarHorario(idRuta, idParada, horario)
    return salida

@app.put("/rutas/Paradas/QuitarHorario/{idRuta:int}/{idParada:int}/{numCorrida:int}")
def quitarHorario(idRuta:int, idParada:int, numCorrida:int):
    salida=app.cn.eliminarHorario(idRuta, idParada, numCorrida)
    return salida

@app.get("/rutas/Paradas/Horario/{idRuta:int}/{idParada:int}")
def obtenerHorario(idRuta:int, idParada:int):
    horarios=app.cn.obtenerHorarios(idRuta, idParada)
    return horarios

@app.get("/rutas/Paradas/Horario/{idRuta:int}/{idParada:int}/{numCorrida:int}")
def obtenerHorario(idRuta:int, idParada:int, numCorrida:int):
    horarios=app.cn.obtenerHorarioEspecifico(idRuta, idParada, numCorrida)
    return horarios

@app.put("/rutas/Agregar/Tarifa")
def agregarTarifa(id:int, tarifas:Tarifas):
    salida=app.cn.insertarTarifa(id, tarifas)
    return salida

@app.put("/rutas/Modificar/Tarifas/{idRuta:int}/{idTarifas:int}")
def modificarTarifa(idRuta:int, idTarifas:int, tarifa:Tarifas):
    salida=app.cn.modificarTarifa(idRuta, idTarifas, tarifa)
    return salida

@app.put("/rutas/Eliminar/Tarifas/{idRuta:int}/{idTarifas:int}")
def eliminarTarifa(idRuta:int, idTarifas:int):
    salida=app.cn.eliminarTarifa(idRuta, idTarifas)
    return salida

@app.get("/rutas/Tarifas/{idRuta:int}")
def consultarTarifas(idRuta:int):
    salida=app.cn.obtenerTarifas(idRuta)
    return salida

@app.put("/rutas/Agregar/VigenciaTarifa/{idRuta:int}/{idTarifas:int}")
def agregarVigencia(idRuta:int, idTarifas:int, vigencia:VigenciaTarifa):
    salida=app.cn.insertarVigenciaTarifa(idRuta, idTarifas, vigencia)
    return salida

@app.put("/rutas/Eliminar/VigenciaTarifa/{idRuta:int}/{idTarifas:int}/{idVigencia:int}")
def eliminarVigencia(idRuta:int, idTarifas:int, idVigencia:int):
    salida=app.cn.eliminarVigenciaTarifa(idRuta, idTarifas, idVigencia)
    return salida

#Servicio REST Empleados
conexion = Conexion()

@app.post("/Empleado/Agregar")
def agregar_empleado(empleado: EmpleadoInsert):
    salida=app.cn.agregarEmpleado(empleado)
    return salida

@app.put("/Empleado/Modificar/{_id}")
def modificar_empleado(id: int, empleado: EmpleadoInsert):
    salida=app.cn.modificarEmpleado(id,empleado)
    return salida

@app.get("/Empleado/Consultar/{_id}")
def consultar_empleado(id: int):
    salida=app.cn.consultarEmpleado(id)
    if salida:
        return salida
    else:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")

@app.get("/Empleado/Consultar")
def consultar_empleados():
    salida=app.cn.consultarEmpleados()
    return salida

@app.delete("/Empleado/Eliminar/{_id}")
def eliminar_empleado(id: int):
    salida=app.cn.eliminarEmpleado(id)
    return salida

#Servicio REST Supervisiones
@app.post("/supervisiones/agregar")
def agregar_supervision(supervision: Supervision):
    try:
        id_ruta = supervision.id_ruta
        id_checador = supervision.id_checador
        fecha_supervision = supervision.fecha_supervision
        return app.cn.agregar_supervision(id_ruta, id_checador, fecha_supervision)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/supervisiones/{id_supervision}/modificar")
def modificar_supervision(id_supervision: str, datos: ModificarSupervision):
    try:
        id_ruta = datos.idRuta
        id_checador = datos.idChecador
        fecha_supervision = datos.fechaSupervicion
        return conexion.modificar_supervision(id_supervision, id_ruta, id_checador, fecha_supervision)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.delete("/supervisiones/eliminar/{id_supervision}")
def eliminar_supervision(id_supervision: str):
    try:
        return app.cn.quitar_supervision(id_supervision)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/supervisiones/{id_supervision}")
def consultar_supervision(id_supervision: str):
    try:
        return app.cn.consultar_supervision(id_supervision)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.post("/supervisiones/{id_supervision}/puntos/agregar")
def agregar_punto_revision(id_supervision: str, puntos_revision: List[PuntoRevision]):
    try:
        puntos_revision_dict = [p.dict() for p in puntos_revision]
        return conexion.agregar_punto_revision(id_supervision, puntos_revision_dict)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@app.delete("/supervisiones/punto/eliminar/{id_supervision}/{id_punto_revision}")
def eliminar_punto_revision(id_supervision: str, id_punto_revision: int):
    try:
        return app.cn.eliminar_punto_revision(id_supervision, id_punto_revision)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.put("/supervisiones/punto/modificar/{id_supervision}")
def modificar_punto_revision(id_supervision: str, modificar_punto_revision: ModificarPuntoRevision):
    try:
        puntos_revision = modificar_punto_revision.PuntosRevision
        return {"mensaje": "Puntos de revisión modificados correctamente"}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

if __name__== '__main__':
    uvicorn.run("main:app",  port=8000,reload=True)