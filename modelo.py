import uuid
import datetime

class Nodo:
    def __init__(self, nombre, tipo, contenido=None):
        # Generamos un ID único y fecha de creación
        self.id = str(uuid.uuid4())
        self.nombre = nombre
        self.tipo = tipo  # "carpeta" o "archivo"
        self.contenido = contenido
        self.hijos = [] # Lista de hijos para el árbol general 
        self.fecha_creacion = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        # Convierte el nodo a diccionario para facilitar el futuro JSON (Día 4)
        return {
            "id": self.id,
            "nombre": self.nombre,
            "tipo": self.tipo,
            "contenido": self.contenido,
            "hijos": [hijo.to_dict() for hijo in self.hijos],
            "fecha_creacion": self.fecha_creacion
        }