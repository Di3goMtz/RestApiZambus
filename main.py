from fastapi import FastAPI, Body
from models import AgregarParada, AgregarRuta, ModificarRuta, ParadaOut, Horarios, Tarifas, VigenciaTarifa, Autobus, AutobusConsulta, AgregarAutobus,ModificarAutobus,Asignacion,ModificarAsignacion
from dao import Conection
import uvicorn

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

if __name__== '__main__':
    uvicorn.run("main:app",  port=8000,reload=True)