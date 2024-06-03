from pymongo import MongoClient
from models import AgregarParada, AgregarRuta, ModificarRuta, ParadaOut, Horarios, Tarifas, VigenciaTarifa, EmpleadoInsert, Supervision, PuntoRevision,ModificarPuntoRevision
import datetime
from typing import List
from bson import ObjectId
from datetime import date

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
    
    def obtener_siguiente_id_tarifa(self):
        max_id = 0
        for ruta in self.bd.rutas.find():
            for tarifa in ruta.get("tarifas", []):
                if tarifa["idTarifas"] > max_id:
                    max_id = tarifa["idTarifas"]
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

    def insertarTarifa(self, idRuta, tarifa:Tarifas):
        idRutaInt = int(idRuta)
        tarifa_dict = tarifa.dict()
        tarifa_dict["idTarifas"] = self.obtener_siguiente_id_tarifa()
        resultado = self.bd.rutas.update_one({"_id": idRutaInt}, {"$push": {"tarifas": tarifa_dict}})
        if resultado.modified_count == 1:
            return {"estatus": "éxito", "mensaje": "La tarifa ha sido agregada exitosamente a la ruta."}
        else:
            return {"estatus": "error", "mensaje": "No se encontró una ruta con el ID proporcionado."}
        
    def modificarTarifa(self, idRuta, idTarifas, tarifa:Tarifas):
        idRutaint = int(idRuta)
        idTarifasInt = int(idTarifas)
        tarifa_dict = tarifa.dict()
        tarifa_dict["idTarifas"] = idTarifasInt
        result = self.bd.rutas.update_one({"_id": idRutaint, "tarifas.idTarifas": idTarifasInt}, {"$set": {"tarifas.$": tarifa_dict}})
        if result.modified_count == 1:
            return {"estatus": "éxito", "mensaje": "La tarifa ha sido modificada exitosamente en la ruta."}
        else:
            return {"estatus": "error", "mensaje": "No se encontró una ruta con el ID proporcionado o la tarifa no existe en la ruta."}
    
    def eliminarTarifa(self, idRuta, idTarifas):
        idRutaInt = int(idRuta)
        idTarifasInt = int(idTarifas)
        result = self.bd.rutas.update_one({"_id": idRutaInt}, {"$pull": {"tarifas": {"idTarifas": idTarifasInt}}})
        if result.modified_count == 1:
            return {"estatus": "éxito", "mensaje": "La tarifa ha sido eliminada exitosamente de la ruta."}
        else:
            return {"estatus": "error", "mensaje": "No se encontró una ruta con el ID proporcionado o la tarifa no existe en la ruta."}
        
    def obtenerTarifas(self, idRuta):
        idRutaInt = int(idRuta)
        ruta = self.bd.rutas.find_one({"_id": idRutaInt})
        if ruta is None:
            return {"estatus": "error", "mensaje": "No se encontró una ruta con el ID proporcionado."}
        return ruta.get("tarifas", [])
    
    def insertarVigenciaTarifa(self, idRuta, idTarifas, vigencia:VigenciaTarifa):
        idRutaInt = int(idRuta)
        idTarifasInt = int(idTarifas)
        vigencia_dict = vigencia.dict()
        resultado = self.bd.rutas.update_one({"_id": idRutaInt, "tarifas.idTarifas": idTarifasInt}, {"$push": {"tarifas.$.VigenciaTarifa": vigencia_dict}})
        if resultado.modified_count == 1:
            return {"estatus": "éxito", "mensaje": "La vigencia de tarifa ha sido agregada exitosamente a la tarifa."}
        else:
            return {"estatus": "error", "mensaje": "No se encontró una ruta con el ID proporcionado o la tarifa no existe en la ruta."}

    def eliminarVigenciaTarifa(self, idRuta, idTarifa, idVigencia):
        idRutaInt = int(idRuta)
        idTarifaInt = int(idTarifa)
        idVigenciaInt = int(idVigencia)
        resultado = self.bd.rutas.update_one({"_id": idRutaInt, "tarifas.idTarifas": idTarifaInt}, {"$pull": {"tarifas.$.VigenciaTarifa": {"idVigencia": idVigenciaInt}}})
        if resultado.modified_count == 1:
            return {"estatus": "éxito", "mensaje": "La vigencia de tarifa ha sido eliminada exitosamente de la tarifa."}
        else:
            return {"estatus": "error", "mensaje": "No se encontró una ruta con el ID proporcionado, la tarifa no existe en la ruta, o la vigencia de tarifa no existe en la tarifa."}

#Servicio REST Empleados
    def cerrar(self):
        self.cliente.close()

    def siguenteId(self):
        max = self.bd.empleados.find_one(sort=[("_id", -1)])["_id"]
        return max + 1
        
    def agregarEmpleado(self, empleado: EmpleadoInsert):
        emp = empleado.dict()
        emp["_id"] = self.siguenteId()
        self.bd.empleados.insert_one(emp)
        return {"estatus": 200, "mensaje": "Empleado agregado con éxito"}

    def modificarEmpleado(self, id: str, empleado: EmpleadoInsert):
        res = self.bd.empleados.update_one({"_id": id}, {"$set": empleado.dict()})
        if res.modified_count > 0:
            return {"estatus": 200, "mensaje": "Empleado modificado con éxito"}
        else:
            return {"estatus": 404, "mensaje": "Empleado no encontrado"}

    def consultarEmpleado(self, id: int):
        _id = int(id)
        empleado = self.bd.empleados.find_one({"_id": _id})
        if empleado:
            return empleado
        else:
            return None

    def consultarEmpleados(self):
        empleados = list(self.bd.empleados.find())
        return empleados

        
    def eliminarEmpleado(self, id: int):
        res = self.bd.empleados.update_one(
            {"_id": id, "estatus": "A"},
            {"$set": {"estatus": "I"}}
        )
        if res.modified_count > 0:
            return {"estatus": 200, "mensaje": "Empleado eliminado con éxito"}
        else:
            return {"estatus": 404, "mensaje": "Empleado no encontrado"}

#Servicio REST Supervisiones

    def validar_ruta(self, id_ruta: int) -> bool:
        return self.bd.rutas.find_one({"_id": id_ruta}) is not None

    def validar_checador(self, id_checador: int) -> bool:
        empleado = self.bd.empleados.find_one({"_id": id_checador, "tipoEmpleado": "Checador"})
        return empleado is not None

    def agregar_supervision(self, id_ruta: int, id_checador: int, fecha_supervision: date):
        nueva_supervision = {
            "idRuta": id_ruta,
            "idChecador": id_checador,
            "fechaSupervicion": fecha_supervision,
            "estatus": "A",
            "PuntosRevision": []
        }
        self.bd.supervisiones.insert_one(nueva_supervision)
        return {"estatus": 200, "mensaje": "Supervisión agregada con éxito"}

    def modificar_supervision(self, id_supervision: str, id_ruta: int, id_checador: int, fecha_supervision: date) -> dict:
        _id = ObjectId(id_supervision)
        supervision_actual = self.bd.supervisiones.find_one({"_id": _id})
        if not supervision_actual:
            return {"estatus": 404, "mensaje": "Supervisión no encontrada"}
        # Crear un diccionario con los nuevos valores que se van a actualizar
        nuevos_valores = {}
        if id_ruta is not None and self.validar_ruta(id_ruta):
            nuevos_valores["idRuta"] = id_ruta
        if id_checador is not None and self.validar_checador(id_checador):
            nuevos_valores["idChecador"] = id_checador
        if fecha_supervision is not None:
            nuevos_valores["fechaSupervicion"] = fecha_supervision.isoformat()
        # Actualizar la supervisión con los nuevos valores
        res = self.bd.supervisiones.update_one(
            {"_id": _id},
            {"$set": nuevos_valores}
        )
        if res.modified_count > 0:
            return {"estatus": 200, "mensaje": "Supervisión modificada con éxito"}
        else:
            return {"estatus": 404, "mensaje": "Supervisión no encontrada"}
            
    def quitar_supervision(self, id_supervision: str):
        _id = ObjectId(id_supervision)
        res = self.bd.supervisiones.update_one(
            {"_id": _id},
            {"$set": {"estatus": "I"}}
        )
        if res.modified_count > 0:
            return {"estatus": 200, "mensaje": "Supervisión marcada como inactiva"}
        else:
            return {"estatus": 404, "mensaje": "Supervisión no encontrada"}

    def consultar_supervision(self, id_supervision: str) -> dict:
        _id = ObjectId(id_supervision)
        supervision = self.bd.supervisiones.find_one({"_id": _id})
        if supervision:
            id_ruta = supervision.get("idRuta")
            id_checador = supervision.get("idChecador")
            ruta = self.bd.rutas.find_one({"_id": id_ruta})
            checador = self.bd.empleados.find_one({"tipoEmpleado": "Checador"})
            if ruta and checador:
                supervision["nombreRuta"] = ruta.get("nombre")
                supervision["nombreChecador"] = checador.get("nombre")
            supervision["_id"] = str(supervision["_id"])
            return supervision
        else:
            return None

    def obtener_nombre_ruta(self, id_ruta: int) -> str:
        ruta = self.bd.rutas.find_one({"_id": id_ruta})
        return ruta["nombre"] if ruta else None

    def obtener_nombre_checador(self, id_checador: int) -> str:
        checador = self.bd.checadores.find_one({"_id": id_checador})
        return checador["nombre"] if checador else None

    def agregar_punto_revision(self, id_supervision: str, punto_revision: dict) -> dict:
        _id = ObjectId(id_supervision)
        res = self.bd.supervisiones.update_one({"_id": _id}, {"$push": {"PuntosRevision": punto_revision}})
        if res.modified_count > 0:
            return {"estatus": 200, "mensaje": "Punto de revisión agregado con éxito"}
        else:
            return {"estatus": 404, "mensaje": "Supervisión no encontrada"}

    def punto_revision_existe(self, id_supervision: str, id_parada: int) -> bool:
        _id = ObjectId(id_supervision)
        supervision = self.bd.supervisiones.find_one({"_id": _id, "PuntosRevision.idParada": id_parada})
        return supervision is not None

    def eliminar_punto_revision(self, id_supervision: str, id_punto_revision: int) -> dict:
        _id = ObjectId(id_supervision)
        res = self.bd.supervisiones.update_one(
            {"_id": _id},
            {"$pull": {"PuntosRevision": {"idParada": id_punto_revision}}}
        )
        if res.modified_count > 0:
            return {"estatus": 200, "mensaje": "Punto de revisión eliminado con éxito"}
        else:
            return {"estatus": 404, "mensaje": "Punto de revisión no encontrado"}

    def modificar_punto_revision(self, id_supervision: str, id_punto_revision: int, comentario: str) -> dict:
        _id = ObjectId(id_supervision)
        # Buscar la supervisión
        supervision = self.bd.supervisiones.find_one({"_id": _id})
        if not supervision:
            return {"estatus": 404, "mensaje": "Supervisión no encontrada"}

        # Buscar el punto de revisión en la lista de puntos de revisión de la supervisión
        puntos_revision = supervision.get("PuntosRevision", [])
        punto_revision_modificado = None
        for punto in puntos_revision:
            if punto.get("id_parada") == id_punto_revision:
                punto_revision_modificado = punto
                break
        # Si se encontró el punto de revisión, actualizar el comentario
        if punto_revision_modificado:
            punto_revision_modificado["comentario"] = comentario
            # Actualizar la supervisión en la base de datos
            res = self.bd.supervisiones.update_one(
                {"_id": _id},
                {"$set": {"PuntosRevision": puntos_revision}}
            )
            if res.modified_count > 0:
                return {"estatus": 200, "mensaje": "Punto de revisión modificado con éxito"}
        return {"estatus": 404, "mensaje": "Punto de revisión no encontrado"}
