# Módulo para la interfaz de usuario (prompts) y validaciones de input

from os import name as SO, system
import questionary as q
from art import tprint
from datetime import datetime
from interfaz_sql import *

def limpiar_pantalla() -> None:
    '''Función para limpiar la consola'''
    if SO == "nt":
        system("cls")
    else:
        system("clear")

def menu_principal() -> str:
    '''Función que despliega el menú principal'''
    # Lista de opciones de menú
    lista_opciones = ["Buscar películas por título",
                    "Buscar películas por fecha de estreno",
                    "Mostrar sinopsis de película (ID)",
                    "Busar películas por calificación",
                    "Buscar director",
                    "Buscar películas por director",
                    "Agregar película",
                    "Borrar película (ID)",
                    "Borrar director (ID)",
                    "Limpiar pantalla",
                    "Salir"]
    try: 
        tprint("CineBase", font="tarty7")
    except:
        q.print(">>> CineBase <<<",style="fg:ansiyellow bold")
    finally:
        total_películas = contar_titulos()
        qprint(f"{total_películas} películas actualmente en la base de datos.",style="fg:ansiyellow italic") 
    
    opcion_elegida = q.select("Elija una opcion del menú", instruction="(utilice las flechas del teclado para navegar y enter para seleccionar)",
                    choices=lista_opciones, qmark="", pointer=">>").ask()
    return opcion_elegida
    
def validar_cadena(cadena: str):
    '''Función para validar una cadena de texto. Toma 'cadena' <str> como argumento y chequea que no esté vacía'''
    if cadena == "":
        return "Error! Debe ingresar el dato solicitado"
    else:
        return True

def validar_int(entero: int):
    '''Función para validar un entero. Toma 'entero' <int> como argumento y chequea que sea
    un número entero y sea mayor a 0'''
    try:
        val = int(entero)
    except ValueError: # Si no se agrega un número entero
        return "Debe ingresar un ID válido"
    else:
        if val < 0: # No puede ser un número negativo:
            return "Debe ingresar un ID válido (> 0)"
        else: # Es un int no < 0
            return True

def validar_fecha(fecha: str):
    '''Función para validar la fecha con formato AAAA-MM-DD. Toma como argumento 'fecha' y chequea
    que cumpla con el formato específico'''
    try:
        val_fecha = datetime.strptime(fecha, '%Y-%m-%d')
    except ValueError:
        return "Error!, debe ingresar una fecha con el formato 'AAAA-MM-DD'"
    else:
        return True

def validar_calificacion(calificacion: float):
    '''Función para validar un flotante. Toma 'calificacion' <float> como argumento y 
    valida que la entrada sea correcta'''
    try:
        calificacion = float(calificacion)
    except ValueError:
        return "Error! Debe ingresar un dato válido (ej. 7 / 6.5)"
    else:
        return True

def validar_respuesta(respuesta: str):
    '''Función para validar una respuesta de Si o No (S/N). Toma 'respuesta' <str> como argumento
    y valida que la entrada sea correcta'''
    respuesta = respuesta.upper()
    
    if respuesta == "S" or respuesta == "N":
        return True
    else:
        return "Debe ingresar S o N según corresponda."

def buscar_titulo():
    '''Función del prompt para la búsqueda de título'''
    pelicula = q.text("Ingrese el título a buscar:\n> ", 
        qmark=">>", validate=validar_cadena).ask()
    buscar_pelicula_por_titulo(pelicula)
    q.press_any_key_to_continue("Presione cualquier tecla para volver al menú...").ask()

def buscar_fecha():
    '''Función del prompt para la búsqueda de título por fecha'''
    fecha = q.text("Ingrese la fecha a buscar (debe tener el formato AAAA-MM-DD)\n> ",
        qmark=">>", validate=validar_fecha).ask()
    buscar_pelicula_por_fecha(fecha)
    q.press_any_key_to_continue("Presione cualquier tecla para volver al menú...").ask()

def buscar_calificacion():
    '''Función del prompt para la búsqueda de título por calificacion'''
    calificacion = q.text("Ingrese la calificación a buscar:\n> ",
        qmark=">>", validate=validar_calificacion).ask()
    buscar_pelicula_por_calificacion(calificacion)
    q.press_any_key_to_continue("Presione cualquier tecla para volver al menú...").ask()

def buscar_sinopsis():
    '''Función del prompt para la búsqueda de sinopsis'''
    id = q.text("Ingrese el ID de la película:\n ",
        qmark=">>", validate=validar_int).ask()
    buscar_descripcion_id(id)
    q.press_any_key_to_continue("Presione cualquier tecla para volver al menú...").ask()

def buscar_directores():
    '''Función del prompt para la búsqueda de director'''
    director = q.text("Ingrese el nombre del director a buscar:\n> ", 
        qmark=">>", validate=validar_cadena).ask()
    buscar_director(director)
    q.press_any_key_to_continue("Presione cualquier tecla para volver al menú...").ask()

def buscar_por_director():
    '''Función del prompt para la búsqueda de títulos por director'''
    director = q.text("Ingrese el nombre del director:\n> ", 
        qmark=">>", validate=validar_cadena).ask()
    buscar_pelicula_por_director(director)
    q.press_any_key_to_continue("Presione cualquier tecla para volver al menú...").ask()

def agregar_pelicula():
    '''Función del prompt para agregar película a la BD'''
    # Solicitamos los datos de la película
    titulo = q.text("Ingrese el nombre de la película:\n> ", 
        qmark=">>", validate=validar_cadena).ask()
    fecha = q.text("Ingrese la fecha de estreno (AAAA-MM-DD)\n> ",
        qmark=">>", validate=validar_fecha).ask()
    calificacion = q.text("Ingrese la calificación:\n> ",
        qmark=">>", validate=validar_calificacion).ask()
    sinopsis = q.text("Ingrese la sinopsis o presione 'enter' para dejar vacío:\n> ", qmark=">>").ask()
    director = q.text("Ingrese el nombre del director:\n> ", 
        qmark=">>", validate=validar_cadena).ask()
    director = director.title()

    # Obtenemos el ID del director 
    director_id = buscar_id_director(director)

    if director_id == None: # Si no existe lo agregamos a la BD
        guardar_director(director)
        q.print("Director agregado a la base de datos",style="fg:green italic")
        director_id = buscar_id_director(director) # Repetimos el búsqueda para actualizar la variable

    # Guardamos la película y la mostramos
    guardar_pelicula(titulo, fecha, calificacion, sinopsis, id_director=director_id[0])
    buscar_pelicula_por_titulo(titulo)
    q.press_any_key_to_continue("Presione cualquier tecla para volver al menú...").ask()

def borrar_pelicula():
    '''Prompt para el borrado de un título en la BD, valida que exista previamente.'''
    # Solicitamos el ID primero y mostramos la película
    id = q.text("Ingrese el ID de la película a borrar:\n ",
        qmark=">>", validate=validar_int).ask()
    
    if chequear_existencia_id_pelicula(id) == False: # Si no existe la película
        qprint("No se encontraron películas con ese ID.", style="bold fg:darkred")
        q.press_any_key_to_continue("Presione cualquier tecla para volver al menú...").ask()
        return
    else: # Si existe pedimos confirmación al usuario
        confirmacion = q.text("Está seguro de que desea borrar la película (S/N):\n ",
        qmark=">>", validate=validar_respuesta).ask()

        if confirmacion.upper() == "N": # Si el usuario responde NO
            return
        else: # Si la respuesta es afirmativa
            borrar_pelicula_bd(id)
    q.press_any_key_to_continue("Presione cualquier tecla para volver al menú...").ask()

def borrar_director():
    '''Prompt para el borrado de un director de la BD'''
    # Solicitamos el ID primero y mostramos la película
    director_id = q.text("Ingrese el ID del director a borrar:\n ",
        qmark=">>", validate=validar_int).ask()
    borrar_director_bd(director_id)
    q.press_any_key_to_continue("Presione cualquier tecla para volver al menú...").ask()