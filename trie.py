class NodoTrie:
    def __init__(self):
        self.hijos = {} # Diccionario para las letras
        self.es_final_palabra = False # Marca si aquí termina un nombre

class Trie:
    def __init__(self):
        self.raiz = NodoTrie()

    def insertar(self, palabra):
        # Inserta una palabra letra por letra
        nodo = self.raiz
        for letra in palabra:
            if letra not in nodo.hijos:
                nodo.hijos[letra] = NodoTrie()
            nodo = nodo.hijos[letra]
        nodo.es_final_palabra = True

    def buscar_prefijo(self, prefijo):
        # Busca palabras que empiecen con el prefijo dado
        nodo = self.raiz
        for letra in prefijo:
            if letra not in nodo.hijos:
                return [] # No hay coincidencias
            nodo = nodo.hijos[letra]
        
        # Si llegamos aquí, el prefijo existe. Buscamos todas las terminaciones.
        resultados = []
        self._recolectar_palabras(nodo, prefijo, resultados)
        return resultados

    def _recolectar_palabras(self, nodo, palabra_actual, lista_resultados):
        # Función auxiliar recursiva para encontrar finales de palabra
        if nodo.es_final_palabra:
            lista_resultados.append(palabra_actual)
        
        for letra, hijo in nodo.hijos.items():
            self._recolectar_palabras(hijo, palabra_actual + letra, lista_resultados)

    def eliminar(self, palabra):
        # Borrado simple (opcional pero recomendado para mantener consistencia)
        # Nota: Por simplicidad, solo marcamos que ya no es final de palabra
        nodo = self.raiz
        for letra in palabra:
            if letra not in nodo.hijos:
                return 
            nodo = nodo.hijos[letra]
        nodo.es_final_palabra = False