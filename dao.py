from pymongo import MongoClient
from models import AgregarParada, AgregarRuta, ModificarRuta, ParadaOut, Horarios
import datetime
from bson import ObjectId

class Conection():
    def __init__(self):
        self.client = MongoClient()
        self.bd=self.client.zambus

    def obtener_siguiente_id(self):
        max_id = self.bd.rutas.find_one(sort=[("_id", -1)])["_id"]
        return max_id + 1

    def obtener_siguiente_id_parada(self, id_ruta):
        idRutaInt = int(id_ruta)
        ruta = self.bd.rutas.find_one({"_id": idRutaInt})
        if ruta is None:
            return 1
        max_id = 0
        for parada in ruta.get("paradas", []):
            if parada["idParada"] > max_id:
                max_id = parada["idParada"]
        return max_id + 1

    def close(self):
        self.client.close()

    def insertarRuta(self, ruta: AgregarRuta):
        respuesta = {"estatus": "", "mensaje": ""}
        if self.bd.rutas.find_one({"nombre": ruta.nombre}):
            respuesta["estatus"] = "error"
            respuesta["mensaje"] = "El nombre de la ruta ya está registrado en la base de datos."
        elif ruta.tiempoEstimadoViaje < 0:
            respuesta["estatus"] = "error"
            respuesta["mensaje"] = "El tiempo estimado de viaje debe ser un valor positivo."
        else:
            parada_dict = ruta.dict()
            parada_dict["_id"] = self.obtener_siguiente_id()
            self.bd.rutas.insert_one(parada_dict)
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
        parada_dict = ruta.dict()
        result = self.bd.rutas.update_one({"_id": id_int}, {"$set": parada_dict})
        return self.obtenerRuta(id_int)
    
    def eliminarRuta(self,id):
        id_int=int(id)
        resultado=self.bd.rutas.delete_one({"_id": id_int})
        if resultado.deleted_count == 1:
            return {"mensaje": "La ruta ha sido eliminada exitosamente."}
        else:
            return {"mensaje": "No se encontró una ruta con el ID proporcionado."}


    def insertarParada(self, idRuta, parada:AgregarParada):
        idRutaInt = int(idRuta)
        parada_dict = parada.dict()
        parada_dict["idParada"] = self.obtener_siguiente_id_parada()
        for horario in parada_dict["horarios"]:
            horario["horaSalida"] = str(horario["horaSalida"])
            horario["horaEstimado"] = str(horario["horaEstimado"])
        result = self.bd.rutas.update_one({"_id": idRutaInt}, {"$push": {"paradas": parada_dict}})
        if result.modified_count == 1:
            return {"estatus": "éxito", "mensaje": "La parada ha sido agregada exitosamente a la ruta."}
        else:
            return {"estatus": "error", "mensaje": "No se encontró una ruta con el ID proporcionado."}
        
    def eliminarParada(self, idRuta, idParada):
        idRutaInt=int(idRuta)
        idParadaInt=int(idParada)
        resultado=self.bd.rutas.update_one({"_id":idRutaInt},{"$pull":{"paradas":{"idParada":idParadaInt}}})
        if resultado.modified_count == 1:
            return  {"estatus": "exito","mesaje":"La parada a sido eliminada de forma exitosa"}
        else:
            return {"estatus": "error", "mensaje": "No se encontró una ruta con el ID proporcionado o la parada no existe en la ruta."}
        
    def modificarParada(self, idRuta, idParada, parada:ParadaOut):
        idRutaInt = int(idRuta)
        idParadaInt = int(idParada)
        parada_dict = parada.dict()
        for horario in parada_dict["horarios"]:
            horario["horaSalida"] = str(horario["horaSalida"])
            horario["horaEstimado"] = str(horario["horaEstimado"])
        result = self.bd.rutas.update_one({"_id": idRutaInt, "paradas.idParada": idParadaInt}, {"$set": {"paradas.$": parada_dict}})
        if result.modified_count == 1:
            return {"estatus": "éxito", "mensaje": "La parada ha sido modificada exitosamente en la ruta."}
        else:
            return {"estatus": "error", "mensaje": "No se encontró una ruta con el ID proporcionado o la parada no existe en la ruta."}
        
    def obtenerParadas(self, idRuta):
        idRutaInt = int(idRuta)
        ruta=self.bd.rutas.find_one({"_id":idRutaInt})
        if ruta is None:
            return {"estatus": "error", "mensaje": "No se encontró una ruta con el ID proporcionado."}
        return ruta.get("paradas", [])

    def obtenerParadaEspecifica(self, idRuta, idParada):
        idRutaInt=int(idRuta)
        idParadaInt=int(idParada)
        ruta = self.bd.rutas.find_one({"_id": idRutaInt})
        if ruta is None:
            return {"estatus": "error", "mensaje": "No se encontró una ruta con el ID proporcionado."}
        for parada in ruta.get("paradas", []):
            if parada["idParada"] == idParadaInt:
                return parada
        return {"estatus": "error", "mensaje": "No se encontró una parada con el ID proporcionado en la ruta."}
    
    def insertarHorario(self, idRuta, idParada, horario:Horarios):
        idRutaInt=int(idRuta)
        idParadaInt=int(idParada)
        horario_dict = horario.dict()
        horario_dict["horaSalida"] = str(horario_dict["horaSalida"])
        horario_dict["horaEstimado"] = str(horario_dict["horaEstimado"])
        result = self.bd.rutas.update_one({"_id": idRutaInt, "paradas.idParada": idParadaInt}, {"$push": {"paradas.$.horarios": horario_dict}})
        if result.modified_count == 1:
            return {"estatus": "éxito", "mensaje": "El horario ha sido agregado exitosamente a la parada."}
        else:
            return {"estatus": "error", "mensaje": "No se encontró una ruta con el ID proporcionado o la parada no existe en la ruta."}
        
    def eliminarHorario(self, idRuta, idParada, num_corrida):
        idRutaInt = int(idRuta)
        idParadaInt = int(idParada)
        result = self.bd.rutas.update_one({"_id": idRutaInt, "paradas.idParada": idParadaInt}, {"$pull": {"paradas.$.horarios": {"numCorrida": num_corrida}}})
        if result.modified_count == 1:
            return {"estatus": "éxito", "mensaje": "El horario ha sido eliminado exitosamente de la parada."}
        else:
            return {"estatus": "error", "mensaje": "No se encontró una ruta con el ID proporcionado, la parada no existe en la ruta, o el horario no existe en la parada."}
        
    def obtenerHorarios(self, idRuta, idParada):
        idRutaInt = int(idRuta)
        idParadaInt = int(idParada)
        ruta = self.bd.rutas.find_one({"_id": idRutaInt})
        if ruta is None:
            return {"estatus": "error", "mensaje": "No se encontró una ruta con el ID proporcionado."}
        for parada in ruta.get("paradas", []):
            if parada["idParada"] == idParadaInt:
                return parada.get("horarios", [])
        return {"estatus": "error", "mensaje": "No se encontró una parada con el ID proporcionado en la ruta."}
    
    def obtenerHorarioEspecifico(self, idRuta, idParada, num_corrida):
        idRutaInt = int(idRuta)
        idParadaInt = int(idParada)
        numcorridaInt = int(num_corrida)
        ruta = self.bd.rutas.find_one({"_id": idRutaInt})
        if ruta is None:
            return {"estatus": "error", "mensaje": "No se encontró una ruta con el ID proporcionado."}
        for parada in ruta.get("paradas", []):
            if parada["idParada"] == idParadaInt:
                for horario in parada.get("horarios", []):
                    if horario["numCorrida"] == numcorridaInt:
                        return horario
                return {"estatus": "error", "mensaje": "No se encontró un horario con el número de corrida proporcionado en la parada."}
        return {"estatus": "error", "mensaje": "No se encontró una parada con el ID proporcionado en la ruta."}

