import json
import os
from modelo import Nodo
from trie import Trie

class ArbolArchivos:
    def __init__(self):
        self.raiz = Nodo("root", "carpeta")
        self.trie = Trie() 
        self.papelera = [] # Lista temporal para la papelera (Día 7)

    def buscar_nodo(self, nodo_actual, id_objetivo):
        # Busca recursivamente por ID
        if nodo_actual.id == id_objetivo:
            return nodo_actual
        
        for hijo in nodo_actual.hijos:
            encontrado = self.buscar_nodo(hijo, id_objetivo)
            if encontrado:
                return encontrado
        return None

    def buscar_por_nombre(self, nodo_padre, nombre_buscado):
        # Ayuda a encontrar un hijo específico por nombre (para comandos cd, rm)
        for hijo in nodo_padre.hijos:
            if hijo.nombre == nombre_buscado:
                return hijo
        return None

    def insertar(self, id_padre, nombre, tipo, contenido=None):
        padre = self.buscar_nodo(self.raiz, id_padre)
        if padre:
            if padre.tipo != "carpeta":
                print(f"Error: '{padre.nombre}' es un archivo, no se puede agregar contenido.")
                return False
            
            # Verificar duplicados en el mismo nivel
            if self.buscar_por_nombre(padre, nombre):
                print(f"Error: Ya existe '{nombre}' en esta carpeta.")
                return False

            nuevo_nodo = Nodo(nombre, tipo, contenido)
            padre.hijos.append(nuevo_nodo)
            self.trie.insertar(nombre) # Agregamos al autocompletado
            return nuevo_nodo
        return False

    def eliminar(self, id_nodo):
        # Mueve el nodo a la papelera en lugar de borrarlo (Soft Delete)
        if id_nodo == self.raiz.id:
            print("Error: No puedes borrar la raíz.")
            return False
        
        padre = self._buscar_padre(self.raiz, id_nodo)
        if padre:
            nodo_a_borrar = None
            for h in padre.hijos:
                if h.id == id_nodo:
                    nodo_a_borrar = h
                    break
            
            if nodo_a_borrar:
                # 1. Sacar del árbol
                padre.hijos = [h for h in padre.hijos if h.id != id_nodo]
                # 2. Sacar del Trie (búsqueda)
                self.trie.eliminar(nodo_a_borrar.nombre)
                # 3. Meter a papelera
                self.papelera.append(nodo_a_borrar)
                print(f"Nota: '{nodo_a_borrar.nombre}' movido a la papelera.")
                return True
        return False

    def vaciar_papelera(self):
        cantidad = len(self.papelera)
        self.papelera = [] # Se borran definitivamente
        print(f"Papelera vaciada. {cantidad} elementos eliminados.")

    def restaurar_de_papelera(self, nombre_nodo):
        # Busca en la papelera y lo devuelve a la raíz (simplificado)
        for i, nodo in enumerate(self.papelera):
            if nodo.nombre == nombre_nodo:
                # Lo sacamos de la papelera
                recuperado = self.papelera.pop(i)
                # Lo ponemos en la raíz
                self.raiz.hijos.append(recuperado)
                # Lo agregamos al Trie de nuevo
                self.trie.insertar(recuperado.nombre)
                print(f"Restaurado '{recuperado.nombre}' en la carpeta raíz.")
                return True
        print("No se encontró ese nombre en la papelera.")
        return False

    def mover(self, id_nodo, id_nuevo_padre):
        # Mueve un nodo de una carpeta a otra
        if id_nodo == self.raiz.id:
            return False
        
        # Verificar que no intentemos mover una carpeta dentro de sí misma
        if id_nodo == id_nuevo_padre:
            print("Error: No puedes mover una carpeta dentro de sí misma.")
            return False

        nodo = self.buscar_nodo(self.raiz, id_nodo)
        nuevo_padre = self.buscar_nodo(self.raiz, id_nuevo_padre)
        antiguo_padre = self._buscar_padre(self.raiz, id_nodo)

        if nodo and nuevo_padre and antiguo_padre:
            if nuevo_padre.tipo != "carpeta":
                print("Error: El destino debe ser una carpeta.")
                return False
            
            # Realizamos el movimiento
            antiguo_padre.hijos.remove(nodo)
            nuevo_padre.hijos.append(nodo)
            print(f"Movido '{nodo.nombre}' a '{nuevo_padre.nombre}'.")
            return True
        return False

    def renombrar(self, id_nodo, nuevo_nombre):
        nodo = self.buscar_nodo(self.raiz, id_nodo)
        if nodo:
            self.trie.eliminar(nodo.nombre)
            nodo.nombre = nuevo_nombre
            self.trie.insertar(nuevo_nombre)
            return True
        return False

    def exportar_preorden(self, nombre_archivo="recorrido_preorden.txt"):
        # [cite_start]Genera un archivo de texto con el recorrido preorden [cite: 9, 10]
        lineas = []
        self._preorden_rec(self.raiz, lineas, 0)
        
        try:
            with open(nombre_archivo, "w") as f:
                f.write("\n".join(lineas))
            print(f"Exportado exitosamente a '{nombre_archivo}'")
        except Exception as e:
            print(f"Error al exportar: {e}")

    def _preorden_rec(self, nodo, lista, nivel):
        # Preorden: Raíz -> Hijos
        indent = "--" * nivel
        info = f"{indent}> {nodo.nombre} ({nodo.tipo})"
        lista.append(info)
        for hijo in nodo.hijos:
            self._preorden_rec(hijo, lista, nivel + 1)

    def _buscar_padre(self, nodo_actual, id_hijo):
        for hijo in nodo_actual.hijos:
            if hijo.id == id_hijo:
                return nodo_actual
            res = self._buscar_padre(hijo, id_hijo)
            if res:
                return res
        return None

    # Persistencia (igual que parte 2)
    def guardar_arbol(self, nombre_archivo="datos_arbol.json"):
        datos = self.raiz.to_dict()
        try:
            with open(nombre_archivo, 'w') as f:
                json.dump(datos, f, indent=4)
            print("Sistema guardado.")
        except Exception as e:
            print(f"Error guardando: {e}")

    def cargar_arbol(self, nombre_archivo="datos_arbol.json"):
        if not os.path.exists(nombre_archivo):
            return
        try:
            with open(nombre_archivo, 'r') as f:
                datos = json.load(f)
            self.raiz = Nodo.from_dict(datos)
            self.trie = Trie()
            self._reconstruir_trie(self.raiz)
            print("Sistema cargado.")
        except Exception as e:
            print(f"Error cargando: {e}")

    def _reconstruir_trie(self, nodo):
        if nodo.nombre != "root":
            self.trie.insertar(nodo.nombre)
        for hijo in nodo.hijos:
            self._reconstruir_trie(hijo)