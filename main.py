from fastapi import FastAPI
from models import AgregarParada
from dao import Conection

app = FastAPI()

@app.on_event('startup')
def startup():
    app.cn=Conection()
    print("inicio conexio")

@app.on_event('shutdowm')
def shutdown():
    app.cn.close()
    print("fin conexio")

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/Parada")
def AgregarParada(parada:AgregarParada):
    salida=app.cn.insertarParada(parada)
    return salida

    return {"message": "Hello World"}