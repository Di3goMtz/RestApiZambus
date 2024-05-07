from pymongo import MongoClient
from models import AgregarParada, AgregarRuta, ModificarRuta, ParadaOut, Horarios, Tarifas, VigenciaTarifa, Autobus, AutobusConsulta,AgregarAutobus,ModificarAutobus,Asignacion,ModificarAsignacion
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
        

    #Servicio Rest Autobus


    def consultarAutobus(self,id):
        id_int = int(id)
        Autobus = self.bd.autobus.find_one({"_id":id_int})
        if Autobus is None:
            return {"estatus": 404, "mensaje": "Autobus no encontrado"}
        return Autobus
    
    def consultarAutobuses(self):
        Autobuses = list(self.bd.autobus.find())
        if Autobuses is None:
            return {"estatus": 404, "mensaje": "Autobuses no encontrado"}
        return Autobuses
    #agregar autobus
    def agregarAutobus(self, autobus: AgregarAutobus):
        
        respuesta = {"estatus": "", "mensaje": ""}

        if autobus.capacidad <= 0:
            return {"estatus": 400, "mensaje": "La capacidad del vehículo debe ser un valor positivo"}

        else:
            autobus_dict = autobus.dict()
            autobus_dict["_id"] = self.obtener_siguiente_id()
            self.bd.autobus.insert_one(autobus_dict)
            respuesta["estatus"] = "éxito"
            respuesta["mensaje"] = "El vehículo ha sido agregado exitosamente."
        return respuesta
            
    
    def modificarAutobus(self, id: int, autobus: ModificarAutobus):
        respuesta = {"estatus": "", "mensaje": ""}
        id_int = int(id)
        autobus_dict = autobus.dict()
        result = self.bd.autobus.update_one({"_id": id_int}, {"$set": autobus_dict})
        return self.consultarAutobus(id)  # Asegúrate de devolver la consulta del autobús modificado

    def eliminarAutobus(self, idAutobus: int):
        res = self.bd.autobus.delete_one({"_id": idAutobus})
        if res.deleted_count > 0:
            return {"estatus": 200, "mensaje": "Autobus eliminado con éxito"}
        else:
            return {"estatus": 404, "mensaje": "Autobus no encontrado"}

        
    #asignaciones

    def consultarAsignacion(self,id):
        id_int = int(id)
        Asignacion = self.bd.asignaciones.find_one({"_id":id_int})
        if Asignacion is None:
            return {"estatus": 404, "mensaje": "Autobus no encontrado"}
        return Asignacion
    
    def consultarAsignaciones(self):
        asignaciones = list(self.bd.asignaciones.find())
        if not asignaciones:
            return {"estatus": 404, "mensaje": "Asignaciones no encontradas"}
        return asignaciones

    def agregarAsignacion(self, asignacion: Asignacion):
        respuesta = {"estatus": "", "mensaje": ""}
        asignacion_dict = asignacion.dict()
        asignacion_dict["fechaInicio"] = datetime.datetime.combine(asignacion.fechaInicio, datetime.datetime.min.time())
        asignacion_dict["fechaFin"] = datetime.datetime.combine(asignacion.fechaFin, datetime.datetime.min.time())
        asignacion_dict["_id"] = self.obtener_siguiente_id_asignaciones()
        self.bd.asignaciones.insert_one(asignacion_dict)
        respuesta["estatus"] = "éxito"
        respuesta["mensaje"] = "La asignación ha sido agregada exitosamente."
        return respuesta
    
    async def modificarAsignacion(self, id: int, asignacion: ModificarAsignacion):
        respuesta = {"estatus": "", "mensaje": ""}
        try:
            id_int = int(id)
            asignacion_dict = asignacion.dict()
            result = await self.bd.asignaciones.update_one({"_id": id_int}, {"$set": asignacion_dict})
            if result.modified_count > 0:
            # Si se modifica al menos un documento
                return await self.consultarAsignacion(id_int)
            else:
            # Si no se modifica ningún documento, la asignación no se encontró
                respuesta["estatus"] = "error"
                respuesta["mensaje"] = "La asignación no pudo ser modificada. Verifica el ID proporcionado."
            return respuesta
        except Exception as e:
        # Manejo de excepciones
            respuesta["estatus"] = "error"
            respuesta["mensaje"] = f"Error al modificar la asignación: {str(e)}"
            return respuesta



    def eliminarAsignacion(self, idAsignacion: int):
        res = self.bd.asignaciones.delete_one({"_id": idAsignacion})
        if res.deleted_count > 0:
            return {"estatus": 200, "mensaje": "Asignación eliminada con éxito"}
        else:
            return {"estatus": 404, "mensaje": "Asignación no encontrada"}