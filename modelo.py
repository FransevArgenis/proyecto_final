import uuid
import datetime

class Nodo:
    def __init__(self, nombre, tipo, contenido=None, id_nodo=None, fecha=None):
        # Si ya traemos ID (al cargar json), lo usamos. Si no, creamos uno nuevo.
        self.id = id_nodo if id_nodo else str(uuid.uuid4())
        self.nombre = nombre
        self.tipo = tipo  # "carpeta" o "archivo"
        self.contenido = contenido
        self.hijos = [] 
        # Si ya traemos fecha, la usamos. Si no, la actual.
        self.fecha_creacion = fecha if fecha else datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        # Convierte el nodo a diccionario para guardar en JSON
        return {
            "id": self.id,
            "nombre": self.nombre,
            "tipo": self.tipo,
            "contenido": self.contenido,
            "hijos": [hijo.to_dict() for hijo in self.hijos],
            "fecha_creacion": self.fecha_creacion
        }

    @staticmethod
    def from_dict(data):
        # Crea un objeto Nodo a partir de un diccionario (para cargar JSON)
        nodo = Nodo(
            nombre=data["nombre"],
            tipo=data["tipo"],
            contenido=data["contenido"],
            id_nodo=data["id"],
            fecha=data["fecha_creacion"]
        )
        # Recursivamente creamos los hijos
        for hijo_data in data["hijos"]:
            nodo.hijos.append(Nodo.from_dict(hijo_data))
        return nodo