from arbol import ArbolArchivos

# Script para simular las pruebas del Día 2-3
def ejecutar_pruebas():
    print("--- INICIANDO PRUEBAS PARTE 1 ---")
    
    arbol = ArbolArchivos()
    id_raiz = arbol.raiz.id
    
    print("\n1. Prueba de Inserción:")
    # Crear carpetas y archivos
    carpeta1 = arbol.insertar(id_raiz, "Documentos", "carpeta")
    archivo1 = arbol.insertar(carpeta1.id, "tarea.txt", "archivo", "Contenido de tarea")
    arbol.insertar(id_raiz, "Fotos", "carpeta")
    
    arbol.mostrar_arbol()

    print("\n2. Prueba de Renombrado:")
    if carpeta1:
        arbol.renombrar(carpeta1.id, "Mis Documentos")
    
    # Verificamos cambio
    nodo_modificado = arbol.buscar_nodo(arbol.raiz, carpeta1.id)
    print(f"Nuevo nombre: {nodo_modificado.nombre}")

    print("\n3. Prueba de Eliminación:")
    # Eliminamos el archivo tarea.txt
    if archivo1:
        arbol.eliminar(archivo1.id)
    
    print("Estado final del árbol:")
    arbol.mostrar_arbol()

if __name__ == "__main__":
    ejecutar_pruebas()