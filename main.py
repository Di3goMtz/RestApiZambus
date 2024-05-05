from fastapi import FastAPI
from models import AgregarParada, AgregarRuta
from dao import Conection
import uvicorn

app = FastAPI()

@app.on_event('startup')
def startup():
    app.cn=Conection()
    print("inicio conexion")

@app.on_event('shutdowm')
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


@app.put("/Parada")
def AgregarParada(parada:AgregarParada):
    salida=app.cn.insertarParada(parada)
    return salida

if __name__== '__main__':
    uvicorn.run("main:app",  port=8000,reload=True)