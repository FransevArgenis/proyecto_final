import json
import os
from modelo import Nodo
from trie import Trie

class ArbolArchivos:
    def __init__(self):
        self.raiz = Nodo("root", "carpeta")
        self.trie = Trie() # Inicializamos el Trie para búsquedas

    def buscar_nodo(self, nodo_actual, id_objetivo):
        if nodo_actual.id == id_objetivo:
            return nodo_actual
        
        for hijo in nodo_actual.hijos:
            encontrado = self.buscar_nodo(hijo, id_objetivo)
            if encontrado:
                return encontrado
        return None

    def insertar(self, id_padre, nombre, tipo, contenido=None):
        padre = self.buscar_nodo(self.raiz, id_padre)
        if padre:
            if padre.tipo != "carpeta":
                print(f"Error: No se puede agregar dentro de un archivo ({padre.nombre})")
                return False
            
            nuevo_nodo = Nodo(nombre, tipo, contenido)
            padre.hijos.append(nuevo_nodo)
            
            # Agregamos el nombre al Trie para el autocompletado
            self.trie.insertar(nombre)
            
            print(f"Éxito: '{nombre}' creado.")
            return nuevo_nodo
        else:
            print("Error: ID padre no encontrado.")
            return False

    def eliminar(self, id_nodo):
        if id_nodo == self.raiz.id:
            print("Error: No se puede eliminar la raíz.")
            return False
        
        padre = self._buscar_padre(self.raiz, id_nodo)
        if padre:
            nodo_a_borrar = None
            # Buscamos el nodo antes de borrarlo para sacar su nombre
            for h in padre.hijos:
                if h.id == id_nodo:
                    nodo_a_borrar = h
                    break
            
            if nodo_a_borrar:
                # Lo quitamos del árbol
                padre.hijos = [h for h in padre.hijos if h.id != id_nodo]
                # Lo quitamos del Trie
                self.trie.eliminar(nodo_a_borrar.nombre)
                print("Éxito: Nodo eliminado.")
                return True
                
        print("Error: Nodo no encontrado.")
        return False

    def renombrar(self, id_nodo, nuevo_nombre):
        nodo = self.buscar_nodo(self.raiz, id_nodo)
        if nodo:
            # Actualizamos Trie: borramos el viejo e insertamos el nuevo
            self.trie.eliminar(nodo.nombre)
            nodo.nombre = nuevo_nombre
            self.trie.insertar(nuevo_nombre)
            
            print(f"Éxito: Renombrado a '{nuevo_nombre}'")
            return True
        return False

    def _buscar_padre(self, nodo_actual, id_hijo):
        for hijo in nodo_actual.hijos:
            if hijo.id == id_hijo:
                return nodo_actual
            res = self._buscar_padre(hijo, id_hijo)
            if res:
                return res
        return None

    def mostrar_arbol(self, nodo=None, nivel=0):
        if not nodo:
            nodo = self.raiz
        indent = "  " * nivel
        icono = "📁" if nodo.tipo == "carpeta" else "📄"
        print(f"{indent}{icono} {nodo.nombre}")
        for hijo in nodo.hijos:
            self.mostrar_arbol(hijo, nivel + 1)

    # --- NUEVAS FUNCIONES DE PERSISTENCIA (Día 4) ---

    def guardar_arbol(self, nombre_archivo="datos_arbol.json"):
        datos = self.raiz.to_dict()
        try:
            with open(nombre_archivo, 'w') as f:
                json.dump(datos, f, indent=4)
            print(f"Árbol guardado en '{nombre_archivo}'")
        except Exception as e:
            print(f"Error al guardar: {e}")

    def cargar_arbol(self, nombre_archivo="datos_arbol.json"):
        if not os.path.exists(nombre_archivo):
            print("No existe archivo guardado, iniciando árbol vacío.")
            return

        try:
            with open(nombre_archivo, 'r') as f:
                datos = json.load(f)
            # Reconstruimos la estructura usando el método estático
            self.raiz = Nodo.from_dict(datos)
            
            # Importante: Reconstruir el Trie con los nombres cargados
            self.trie = Trie() 
            self._reconstruir_trie_recursivo(self.raiz)
            
            print("Árbol cargado exitosamente.")
        except Exception as e:
            print(f"Error al cargar: {e}")

    def _reconstruir_trie_recursivo(self, nodo):
        # Recorre todo el árbol cargado para llenar el Trie de nuevo
        if nodo.nombre != "root":
            self.trie.insertar(nodo.nombre)
        for hijo in nodo.hijos:
            self._reconstruir_trie_recursivo(hijo)