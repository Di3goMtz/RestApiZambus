from pymongo import MongoClient
from models import AgregarParada, AgregarRuta, ModificarRuta
import datetime
from bson import ObjectId

def obtener_siguiente_id(self):
    max_id = self.bd.rutas.find_one(sort=[("_id", -1)])["_id"]
    return max_id + 1

class Conection():
    def __init__(self):
        self.client = MongoClient()
        self.bd=self.client.zambus

    def obtener_siguiente_id(self):
        max_id = self.bd.rutas.find_one(sort=[("_id", -1)])["_id"]
        return max_id + 1

    def close(self):
        self.client.close()

    def insertarRuta(self, ruta: AgregarRuta):
        respuesta = {"estatus": "", "mensaje": ""}
        # Aquí puedes agregar las validaciones necesarias
        if self.bd.rutas.find_one({"nombre": ruta.nombre}):
            respuesta["estatus"] = "error"
            respuesta["mensaje"] = "El nombre de la ruta ya está registrado en la base de datos."
        elif ruta.tiempoEstimadoViaje < 0:
            respuesta["estatus"] = "error"
            respuesta["mensaje"] = "El tiempo estimado de viaje debe ser un valor positivo."
        else:
            # Si todas las validaciones son exitosas, inserta la ruta en la base de datos
            ruta_dict = ruta.dict()
            ruta_dict["_id"] = self.obtener_siguiente_id()
            self.bd.rutas.insert_one(ruta_dict)
            respuesta["estatus"] = "éxito"
            respuesta["mensaje"] = "La ruta ha sido agregada exitosamente."
        return respuesta

    def obtenerRutas(self):
        rutas=self.bd.rutas.find()
        return list(rutas)
    
    def obtenerRuta(self, id):
        id_int = int(id)
        ruta = self.bd.rutas.find_one({"_id": id_int})
        if ruta is None:
            return {"error": "No se encontró una ruta con el ID proporcionado"}
        return ruta

    def modificarRuta(self, id, ruta: ModificarRuta):
        id_int = int(id)
        ruta_dict = ruta.dict()
        result = self.bd.rutas.update_one({"_id": id_int}, {"$set": ruta_dict})
        return self.obtenerRuta(id_int)
    
    def eliminarRuta(self,id):
        id_int=int(id)
        resultado=self.bd.rutas.delete_one({"_id": id_int})
        if resultado.deleted_count == 1:
            return {"mensaje": "La ruta ha sido eliminada exitosamente."}
        else:
            return {"mensaje": "No se encontró una ruta con el ID proporcionado."}

    def insertarParada(self, parada:AgregarParada):
        respuesta={"estatus":"","mensaje":""}
        pass