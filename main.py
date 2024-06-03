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

@app.post("/Empleado/Agregar", tags=["empleadosREST"])
def agregar_empleado(empleado: EmpleadoInsert):
    salida=app.cn.agregarEmpleado(empleado)
    return salida

@app.put("/Empleado/Modificar/{_id}", tags=["empleadosREST"])
def modificar_empleado(id: int, empleado: EmpleadoInsert):
    salida=app.cn.modificarEmpleado(id,empleado)
    return salida

@app.get("/Empleado/Consultar/{_id}", tags=["empleadosREST"])
def consultar_empleado(id: int):
    salida=app.cn.consultarEmpleado(id)
    if salida:
        return salida
    else:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")

@app.get("/Empleado/Consultar", tags=["empleadosREST"])
def consultar_empleados():
    salida=app.cn.consultarEmpleados()
    return salida

@app.delete("/Empleado/Eliminar/{_id}", tags=["empleadosREST"])
def eliminar_empleado(id: int):
    salida=app.cn.eliminarEmpleado(id)
    return salida

#Servicio REST Supervisiones
# Agregar supervisión
@app.post("/supervisiones/agregar", tags=["supervisionesREST"])
def agregar_supervision(supervision: Supervision):
    try:
        # Validar idRuta e idChecador
        if not app.cn.validar_ruta(supervision.id_ruta):
            raise HTTPException(status_code=400, detail="idRuta no existe")
        if not app.cn.validar_checador(supervision.id_checador):
            raise HTTPException(status_code=400, detail="idChecador no existe")
        
        return app.cn.agregar_supervision(supervision.id_ruta, supervision.id_checador, supervision.fecha_supervision)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Modificar supervisión
@app.put("/supervisiones/{id_supervision}/modificar", tags=["supervisionesREST"])
def modificar_supervision(id_supervision: str, datos: ModificarSupervision):
    try:
        # Validar idRuta e idChecador
        if not app.cn.validar_ruta(datos.idRuta):
            raise HTTPException(status_code=400, detail="idRuta no existe")
        if not app.cn.validar_checador(datos.idChecador):
            raise HTTPException(status_code=400, detail="idChecador no existe")
        
        return app.cn.modificar_supervision(id_supervision, datos.idRuta, datos.idChecador, datos.fechaSupervicion)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

# Eliminar supervisión
@app.delete("/supervisiones/eliminar/{id_supervision}", tags=["supervisionesREST"])
def eliminar_supervision(id_supervision: str):
    try:
        return app.cn.quitar_supervision(id_supervision)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

# Consultar supervisión
@app.get("/supervisiones/{id_supervision}", tags=["supervisionesREST"])
def consultar_supervision(id_supervision: str):
    try:
        supervision = app.cn.consultar_supervision(id_supervision)
        if supervision:
            id_checador = supervision.get("idChecador")
            checador = app.cn.obtener_nombre_checador(id_checador)
            if checador:
                supervision["nombreChecador"] = checador.get("nombre")
            return supervision
        else:
            raise HTTPException(status_code=404, detail="Supervisión no encontrada")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Agregar punto de revisión
@app.post("/supervisiones/{id_supervision}/puntos/agregar", tags=["supervisionesREST"])
def agregar_punto_revision(id_supervision: str, punto_revision: PuntoRevision):
    try:
        if app.cn.punto_revision_existe(id_supervision, punto_revision.id_parada):
            raise HTTPException(status_code=400, detail="El punto de revisión ya existe")
        
        return app.cn.agregar_punto_revision(id_supervision, punto_revision)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

# Eliminar punto de revisión
@app.delete("/supervisiones/punto/eliminar/{id_supervision}/{id_punto_revision}", tags=["supervisionesREST"])
def eliminar_punto_revision(id_supervision: str, id_punto_revision: int):
    try:
        return app.cn.eliminar_punto_revision(id_supervision, id_punto_revision)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

# Modificar punto de revisión
@app.put("/supervisiones/punto/modificar/{id_supervision}/{id_punto_revision}", tags=["supervisionesREST"])
def modificar_punto_revision(id_supervision: str, id_punto_revision: int, modificar_punto_revision: ModificarPuntoRevision):
    try:
        comentario = modificar_punto_revision.comentario
        return conexion.modificar_punto_revision(id_supervision, id_punto_revision, comentario)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

if __name__== '__main__':
    uvicorn.run("main:app",  port=8000,reload=True)