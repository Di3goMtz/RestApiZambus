from pymongo import MongoClient
from models import AgregarParada
import datetime
from bson import ObjectId

class Conection():
    def __init__(self):
        self.client = MongoClient()
        self.bd=self.client.zambus

    def close(self):
        self.client.close()

    def insertarParada(self, parada:AgregarParada):
        respuesta={"estatus":"","mensaje":""}
        pass