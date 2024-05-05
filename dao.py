from pymongo import MongoClient
from models import AgregarParada, AgregarRuta
import datetime
from bson import ObjectId

class Conection():
    def __init__(self):
        self.client = MongoClient()
        self.bd=self.client.zambus

    def close(self):
        self.client.close()

    def insertarRuta(self, ruta:AgregarRuta):
        espuesta={"estatus":"","mensaje":""}
        if(ruta.nombre != ruta.nombre):
            if(ruta.tiempoEstimadoViaje >=0):
                pass
        pass

    def insertarParada(self, parada:AgregarParada):
        respuesta={"estatus":"","mensaje":""}
        pass