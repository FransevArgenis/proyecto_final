from arbol import ArbolArchivos

def limpiar_pantalla():
    # Comando simple para limpiar consola (funciona en mac/linux y windows)
    import os
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    sistema = ArbolArchivos()
    # Intentamos cargar datos previos
    sistema.cargar_arbol()
    
    # Controlamos en qué carpeta estamos actualmente (navegación)
    nodo_actual = sistema.raiz
    
    print("\n=== MINI FILE SYSTEM SHELL ===")
    print("Comandos disponibles: mkdir, touch, ls, cd, rm, mv, search, export, papelera, exit")
    
    while True:
        # Mostramos la ruta actual estilo shell, ej: root/documentos $
        ruta = f"{nodo_actual.nombre} $ "
        entrada = input(ruta).strip().split()
        
        if not entrada:
            continue
            
        comando = entrada[0].lower()
        args = entrada[1:]
        
        if comando == "exit":
            sistema.guardar_arbol()
            print("Saliendo y guardando cambios...")
            break
            
        elif comando == "ls":
            # Listar hijos
            print(f"Contenido de '{nodo_actual.nombre}':")
            if not nodo_actual.hijos:
                print("  (vacío)")
            for hijo in nodo_actual.hijos:
                icono = "📁" if hijo.tipo == "carpeta" else "📄"
                print(f"  {icono} {hijo.nombre}")
                
        elif comando == "mkdir":
            # Crear carpeta: mkdir nombre
            if args:
                sistema.insertar(nodo_actual.id, args[0], "carpeta")
            else:
                print("Uso: mkdir <nombre_carpeta>")
                
        elif comando == "touch":
            # Crear archivo: touch nombre [contenido]
            if args:
                nombre = args[0]
                texto = args[1] if len(args) > 1 else "vacío"
                sistema.insertar(nodo_actual.id, nombre, "archivo", texto)
            else:
                print("Uso: touch <nombre_archivo> [contenido]")
                
        elif comando == "cd":
            # Navegar: cd nombre
            if args:
                nombre_destino = args[0]
                if nombre_destino == "..":
                    # Ir al padre (buscamos quien es el padre del actual)
                    if nodo_actual.id == sistema.raiz.id:
                        print("Ya estás en la raíz.")
                    else:
                        padre = sistema._buscar_padre(sistema.raiz, nodo_actual.id)
                        if padre:
                            nodo_actual = padre
                else:
                    # Ir a un hijo
                    destino = sistema.buscar_por_nombre(nodo_actual, nombre_destino)
                    if destino and destino.tipo == "carpeta":
                        nodo_actual = destino
                    else:
                        print(f"No existe la carpeta '{nombre_destino}' aquí.")
            else:
                # Si solo pone 'cd', vuelve a root
                nodo_actual = sistema.raiz

        elif comando == "rm":
            # Eliminar (enviar a papelera): rm nombre
            if args:
                target = sistema.buscar_por_nombre(nodo_actual, args[0])
                if target:
                    sistema.eliminar(target.id)
                else:
                    print("Archivo/Carpeta no encontrado.")
            else:
                print("Uso: rm <nombre>")

        elif comando == "mv":
            # Mover: mv nombre_origen nombre_carpeta_destino
            # Nota: Simplificado para mover cosas desde la carpeta actual a una hija
            if len(args) >= 2:
                origen = sistema.buscar_por_nombre(nodo_actual, args[0])
                destino = sistema.buscar_por_nombre(nodo_actual, args[1])
                
                if origen and destino:
                    sistema.mover(origen.id, destino.id)
                else:
                    print("Origen o destino no encontrados en esta ruta.")
            else:
                print("Uso: mv <objeto> <carpeta_destino_aqui>")

        elif comando == "search":
            # Buscar por prefijo: search pro
            if args:
                resultados = sistema.trie.buscar_prefijo(args[0])
                print(f"Resultados autocompletado para '{args[0]}': {resultados}")
            else:
                print("Uso: search <prefijo>")

        elif comando == "export":
            # [cite_start]Exportar preorden [cite: 9, 10]
            sistema.exportar_preorden()

        elif comando == "papelera":
            # Gestión papelera
            if args and args[0] == "ver":
                print(f"Papelera ({len(sistema.papelera)}): {[n.nombre for n in sistema.papelera]}")
            elif args and args[0] == "vaciar":
                sistema.vaciar_papelera()
            elif args and args[0] == "restore" and len(args) > 1:
                sistema.restaurar_de_papelera(args[1])
            else:
                print("Uso: papelera [ver | vaciar | restore <nombre>]")

        elif comando == "help":
            print("Ayuda: mkdir <n>, touch <n>, cd <n>, rm <n>, mv <org> <dest>, search <txt>, export, papelera ver")

        else:
            print("Comando no reconocido. Escribe 'help'.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nSaliendo forzosamente...")