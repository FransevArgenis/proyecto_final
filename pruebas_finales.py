import time
from arbol import ArbolArchivos

def test_casos_limite():
    print("=== INICIANDO PRUEBAS DE INTEGRACIÓN (DÍAS 10-11) ===")
    sistema = ArbolArchivos()
    raiz_id = sistema.raiz.id

    # 1. Prueba de Volumen (Performance)
    print("\n1. Creando 1000 nodos para probar rendimiento...")
    inicio = time.time()
    for i in range(1000):
        sistema.insertar(raiz_id, f"archivo_{i}", "archivo")
    fin = time.time()
    print(f"Éxito: 1000 nodos creados en {fin - inicio:.4f} segundos.")

    # 2. Prueba de Consistencia tras Movimientos
    print("\n2. Probando movimientos masivos...")
    carpeta_destino = sistema.insertar(raiz_id, "Destino_Final", "carpeta")
    nodo_a_mover = sistema.buscar_por_nombre(sistema.raiz, "archivo_500")
    
    if sistema.mover(nodo_a_mover.id, carpeta_destino.id):
        # Verificar si el nodo realmente cambió de padre
        padre_nuevo = sistema._buscar_padre(sistema.raiz, nodo_a_mover.id)
        if padre_nuevo.nombre == "Destino_Final":
            print("Consistencia confirmada: El nodo cambió de padre correctamente.")

    # 3. Prueba de Casos Límite (Errores controlados)
    print("\n3. Probando casos de error:")
    # Intentar mover una carpeta a un archivo (debe fallar)
    archivo_falso = sistema.insertar(raiz_id, "no_soy_carpeta.txt", "archivo")
    carpeta_test = sistema.insertar(raiz_id, "carpeta_test", "carpeta")
    
    print("Intento mover carpeta a un archivo:")
    sistema.mover(carpeta_test.id, archivo_falso.id) 

    # 4. Prueba de Autocompletado con nombres similares
    print("\n4. Probando Trie con nombres similares:")
    sistema.insertar(raiz_id, "foto_vacaciones_1.jpg", "archivo")
    sistema.insertar(raiz_id, "foto_vacaciones_2.jpg", "archivo")
    sistema.insertar(raiz_id, "foto_trabajo.png", "archivo")
    
    res = sistema.trie.buscar_prefijo("foto_v")
    print(f"Búsqueda 'foto_v': {res}")

if __name__ == "__main__":
    test_casos_limite()