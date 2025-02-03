# main.py
# Toda la información en: https://thenerdyapprentice.blogspot.com/ (no está publicado aún)

# Este archivo contiene la lógica principal del programa

# Importamos los módulos a usar
import interfaz_usuario
import questionary as q
from art import art

def main() -> None:
    interfaz_usuario.limpiar_pantalla()

    while True:
        opcion_elegida = interfaz_usuario.menu_principal()

        if opcion_elegida == "Salir":
            q.print("Ha seleccionado salir del programa, adiós!", style="cyan")
            print(art("thanks"))
            break
        elif opcion_elegida == "Limpiar pantalla":
            interfaz_usuario.limpiar_pantalla()
        elif opcion_elegida == "Buscar películas por título":
            interfaz_usuario.buscar_titulo()
        elif opcion_elegida == "Buscar películas por fecha de estreno":
            interfaz_usuario.buscar_fecha()
        elif opcion_elegida == "Busar películas por calificación":
            interfaz_usuario.buscar_calificacion()
        elif opcion_elegida == "Mostrar sinopsis de película (ID)":
            interfaz_usuario.buscar_sinopsis()
        elif opcion_elegida == "Buscar director":
            interfaz_usuario.buscar_directores()
        elif opcion_elegida == "Buscar películas por director":
            interfaz_usuario.buscar_por_director()
        elif opcion_elegida == "Agregar película":
            interfaz_usuario.agregar_pelicula()
        elif opcion_elegida == "Borrar película (ID)":
            interfaz_usuario.borrar_pelicula()
        elif opcion_elegida == "Borrar director (ID)":
            interfaz_usuario.borrar_director()

if __name__ == '__main__':
    main()



