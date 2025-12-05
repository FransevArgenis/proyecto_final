from arbol import ArbolArchivos

def probar_parte2():
    print("--- INICIANDO PRUEBAS PARTE 2 (Persistencia y Trie) ---")
    
    arbol = ArbolArchivos()
    root_id = arbol.raiz.id

    print("\n1. Creando estructura...")
    # Creamos varios archivos para probar el autocompletado
    arbol.insertar(root_id, "documentos", "carpeta")
    arbol.insertar(root_id, "descargas", "carpeta")
    arbol.insertar(root_id, "proyecto_final", "archivo")
    arbol.insertar(root_id, "propuesta_tesis", "archivo")

    print("\n2. Probando Autocompletado (Trie):")
    # Buscamos cosas que empiecen con "pro"
    prefijo = "pro"
    sugerencias = arbol.trie.buscar_prefijo(prefijo)
    print(f"Buscando '{prefijo}': {sugerencias}") 
    # Debería salir proyecto_final y propuesta_tesis

    prefijo2 = "do"
    sugerencias2 = arbol.trie.buscar_prefijo(prefijo2)
    print(f"Buscando '{prefijo2}': {sugerencias2}")

    print("\n3. Probando Persistencia (Guardar):")
    arbol.guardar_arbol("mi_sistema.json")

    print("\n4. Probando Persistencia (Cargar en un árbol nuevo):")
    # Creamos una instancia nueva (vacía) para ver si carga bien
    arbol_nuevo = ArbolArchivos()
    arbol_nuevo.cargar_arbol("mi_sistema.json")
    
    print("Mostrando árbol cargado:")
    arbol_nuevo.mostrar_arbol()
    
    print("Probando Trie en el árbol cargado:")
    # Si se reconstruyó bien, el Trie debe funcionar también
    print(f"Busqueda 'desc' en nuevo árbol: {arbol_nuevo.trie.buscar_prefijo('desc')}")

if __name__ == "__main__":
    probar_parte2()