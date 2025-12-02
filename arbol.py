from modelo import Nodo

class ArbolArchivos:
    def __init__(self):
        # Nodo raíz siempre es una carpeta llamada 'root' o '/'
        self.raiz = Nodo("root", "carpeta")

    def buscar_nodo(self, nodo_actual, id_objetivo):
        # Busca un nodo por su ID de forma recursiva
        if nodo_actual.id == id_objetivo:
            return nodo_actual
        
        for hijo in nodo_actual.hijos:
            encontrado = self.buscar_nodo(hijo, id_objetivo)
            if encontrado:
                return encontrado
        return None

    def insertar(self, id_padre, nombre, tipo, contenido=None):
        # Busca al padre y añade el hijo
        padre = self.buscar_nodo(self.raiz, id_padre)
        if padre:
            if padre.tipo != "carpeta":
                print(f"Error: No se puede agregar dentro de un archivo ({padre.nombre})")
                return False
            
            nuevo_nodo = Nodo(nombre, tipo, contenido)
            padre.hijos.append(nuevo_nodo)
            print(f"Éxito: '{nombre}' creado dentro de '{padre.nombre}'")
            return nuevo_nodo
        else:
            print("Error: ID padre no encontrado.")
            return False

    def eliminar(self, id_nodo):
        # Elimina un nodo buscando a su padre (operación recursiva implícita) [cite: 16]
        if id_nodo == self.raiz.id:
            print("Error: No se puede eliminar la raíz.")
            return False
        
        padre = self._buscar_padre(self.raiz, id_nodo)
        if padre:
            # Filtramos la lista de hijos para sacar el nodo a eliminar
            original_len = len(padre.hijos)
            padre.hijos = [h for h in padre.hijos if h.id != id_nodo]
            
            if len(padre.hijos) < original_len:
                print("Éxito: Nodo eliminado.")
                return True
        print("Error: Nodo no encontrado.")
        return False

    def renombrar(self, id_nodo, nuevo_nombre):
        nodo = self.buscar_nodo(self.raiz, id_nodo)
        if nodo:
            nodo.nombre = nuevo_nombre
            print(f"Éxito: Renombrado a '{nuevo_nombre}'")
            return True
        return False

    def _buscar_padre(self, nodo_actual, id_hijo):
        # Función auxiliar para encontrar al padre de un nodo
        for hijo in nodo_actual.hijos:
            if hijo.id == id_hijo:
                return nodo_actual
            res = self._buscar_padre(hijo, id_hijo)
            if res:
                return res
        return None

    def mostrar_arbol(self, nodo=None, nivel=0):
        # Visualización simple en consola para verificar estructura
        if not nodo:
            nodo = self.raiz
        indent = "  " * nivel
        icono = "📁" if nodo.tipo == "carpeta" else "📄"
        print(f"{indent}{icono} {nodo.nombre} (ID: {nodo.id})")
        for hijo in nodo.hijos:
            self.mostrar_arbol(hijo, nivel + 1)