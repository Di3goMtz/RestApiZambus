from fastapi import FastAPI, Body
from models import AgregarParada, AgregarRuta, ModificarRuta
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

@app.put("/Parada")
def AgregarParada(parada:AgregarParada):
    salida=app.cn.insertarParada(parada)
    return salida

if __name__== '__main__':
    uvicorn.run("main:app",  port=8000,reload=True)
