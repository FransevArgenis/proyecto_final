**Proyecto_Final:** Árboles
integrantes:
Parra Urias Fransev Argenis
Aguilar Millan Ramon Alfonso

 **Descripción del proyecto:**

Objetivo: que cada equipo (dos integrantes) implemente en consola una mini‐suite que permita crear, mover, renombrar y eliminar nodos en una jerarquía (carpetas/archivos), buscar títulos por prefijo con autocompletado (Trie) y exportar recorridos (preorden). El proyecto refuerza conceptos de árboles, recorridos y estructuras auxiliares para índices..

## 🚀 Funcionalidades
- **Árbol General:** Gestión de jerarquías (carpetas dentro de carpetas).
- **Trie:** Autocompletado de nombres de archivos y carpetas.
- **Persistencia:** Guarda y carga automáticamente los datos en un archivo JSON.
- **Papelera:** Los archivos eliminados se pueden restaurar o borrar definitivamente.
- **Exportación:** Genera un archivo de texto con el recorrido en preorden del árbol.

## 🛠️ Requisitos
- **Python 3.x** instalado(ejecutado en el preyecto).
- **Visual Studio Code**(usado en el proyecto).


Estructura del Proyecto
* `modelo.py`: Define la estructura del Nodo.
* `arbol.py`: Contiene la lógica del Árbol General y persistencia JSON.
* `trie.py`: Implementación del algoritmo Trie para búsqueda por prefijo.
* `main.py`: Interfaz de consola interactiva.
* `test_parte2.py` / `pruebas_finales.py`: Scripts de validación.


## 💻 Instrucciones de Uso

Para iniciar el programa, ejecuta en tu terminal:
```bash
python3 main.py


Comando        Descripción                                Ejemplo
----------------------------------------------------------------------------
ls             Lista el contenido de la carpeta actual    ls
mkdir          Crea una nueva carpeta                     mkdir Documentos
touch          Crea un archivo nuevo                      touch nota.txt
cd             Cambia de directorio (.. para volver)      cd Documentos
rm             Mueve un elemento a la papelera            rm nota.txt
mv             Mueve un objeto a otra carpeta             mv nota.txt Carpeta2
search         Busca por prefijo (autocompletado)         search doc
export         Exporta el árbol a un archivo .txt         export
papelera       Gestiona elementos borrados                papelera ver
exit           Guarda cambios y sale                      exit



Pruebas y Demo
Para verificar el funcionamiento automático y casos de prueba masivos, puedes usar:
- python3 demo_proyecto.py (Muestra todas las funciones paso a paso)
- python3 pruebas_finales.py (Prueba de rendimiento y casos límite)

