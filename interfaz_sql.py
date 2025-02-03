# Módulo que maneja la lógica de búsqueda e ingreso de datos en la base.

import sqlite3
from prettytable.colortable import ColorTable, Themes
from questionary import print as qprint
from art import tprint
from pathlib import Path

BD = Path.cwd() / 'peliculas.db'

def buscar_pelicula_por_titulo(pelicula: str):
    '''Función para buscar un título en la base de datos. Toma como argumento el nombre de
    la película y realiza una búsqueda aproximada <SQLITE:LIKE>'''
    with sqlite3.connect(BD) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT peliculas.id, peliculas.titulo, peliculas.fecha_estreno, peliculas.calificacion, directores.Nombre AS nombre_director
            FROM peliculas
            JOIN directores ON peliculas.id_director = directores.id
            WHERE peliculas.titulo LIKE ?""", (f"{pelicula}%",))
        res = cursor.fetchall()
        
        # Chequeamos si hay resultados
        if not res: # Si no hay resultados
            qprint("No se encontraron películas con ese título.", style="bold fg:darkred")
            return
       
        tabla_res = ColorTable(theme=Themes.OCEAN_DEEP)
        # Seteamos el nombre de las columnas
        tabla_res.field_names=["ID", "Titulo", "Fecha estreno", "Calificación", "Director"]
        # Agregamos los datos a la tabla
        for fila in res:
            tabla_res.add_row(fila)
        print(tabla_res)
        
def buscar_descripcion_id(id: str):
    '''Función para buscar la descripción (sinopsis) en la BD. Toma como argumento el ID de
    la película'''
    with sqlite3.connect(BD) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT descripcion FROM peliculas WHERE id = ?", (id,))
        res = cursor.fetchone()
        
        # Chequeamos si hay resultados
        if not res: # Si no hay resultados
            qprint("No se encontraron películas con ese ID.", style="bold fg:darkred")
            return
        
        tprint("Sinopsis", font="tarty2")
        qprint(res[0], style="italic fg:green")

def buscar_pelicula_por_fecha(fecha: str):
    '''Función para buscar un título en la base de datos a partir de una fecha. Toma como argumento 
    una fecha con el formato <AAAA-MM-DD>'''
    with sqlite3.connect(BD) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT peliculas.id, peliculas.titulo, peliculas.fecha_estreno, peliculas.calificacion, directores.Nombre AS nombre_director
            FROM peliculas
            JOIN directores ON peliculas.id_director = directores.id
            WHERE fecha_estreno = ?""",(fecha,))
        res = cursor.fetchall()
        
        # Chequeamos si hay resultados
        if not res: # Si no hay resultados
            qprint("No se encontraron películas con esa fecha de estreno.", style="bold fg:darkred")
            return
       
        tabla_res = ColorTable(theme=Themes.OCEAN_DEEP)
        # Seteamos el nombre de las columnas
        tabla_res.field_names=["ID", "Titulo", "Fecha estreno", "Calificación", "Director"]
        # Agregamos los datos a la tabla
        for fila in res:
            tabla_res.add_row(fila)
        print(tabla_res)

def buscar_pelicula_por_calificacion(calificacion: float):
    '''Función para buscar titulos en la base de datos a partir de una califcación. 
    Toma como argumento 'calificacion' <float>'''
    # SQLITE puede buscar sin importar si es entero o flotante 7 = 7.0
    with sqlite3.connect(BD) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT peliculas.id, peliculas.titulo, peliculas.fecha_estreno, peliculas.calificacion, directores.Nombre AS nombre_director
            FROM peliculas
            JOIN directores ON peliculas.id_director = directores.id
            WHERE  calificacion = ?;""",(calificacion,))
        res = cursor.fetchall()
        
        # Chequeamos si hay resultados
        if not res: # Si no hay resultados
            qprint("No se encontraron películas con esa fecha de estreno.", style="bold fg:darkred")
            return
       
        tabla_res = ColorTable(theme=Themes.OCEAN_DEEP)
        # Seteamos el nombre de las columnas
        tabla_res.field_names=["ID", "Titulo", "Fecha estreno", "Calificación", "Director"]
        # Agregamos los datos a la tabla
        for fila in res:
            tabla_res.add_row(fila)
        print(tabla_res)

def buscar_director(nombre_director: str):
    '''Función para buscar el director en la base de datos. Toma como argumento 'nombre_director' <str>'''
    with sqlite3.connect(BD) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * from directores WHERE Nombre LIKE ?", (f"{nombre_director}%",))
        res = cursor.fetchall()
        
        # Chequeamos si hay resultados
        if not res: # Si no hay resultados
            qprint("No se encontró al director en la base de datos", style="bold fg:darkred")
            return
       
        tabla_res = ColorTable(theme=Themes.OCEAN_DEEP)
        # Seteamos el nombre de las columnas
        tabla_res.field_names=["Nombre", "ID"]
        # Agregamos los datos a la tabla
        for fila in res:
            tabla_res.add_row(fila)
        print(tabla_res)

def buscar_pelicula_por_director(nombre_director: str):
    '''Función para buscar titulos en la base de datos a partir del nombre del director 
    Toma como argumento 'nombre_director' <str>'''
    with sqlite3.connect(BD) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT peliculas.id, peliculas.titulo, peliculas.fecha_estreno, peliculas.calificacion, directores.Nombre AS nombre_director
            FROM peliculas
            JOIN directores ON peliculas.id_director = directores.id
            WHERE  directores.Nombre LIKE ?;""",(f"{nombre_director}%",))
        res = cursor.fetchall()
        
        # Chequeamos si hay resultados
        if not res: # Si no hay resultados
            qprint("No se encontraron películas con ese director.", style="bold fg:darkred")
            return
       
        tabla_res = ColorTable(theme=Themes.OCEAN_DEEP)
        # Seteamos el nombre de las columnas
        tabla_res.field_names=["ID", "Titulo", "Fecha estreno", "Calificación", "Director"]
        # Agregamos los datos a la tabla
        for fila in res:
            tabla_res.add_row(fila)
        print(tabla_res)

def buscar_id_director(nombre_director: str) -> str:
    '''Función para buscar el ID de un determinado director.'''
    with sqlite3.connect(BD) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM directores WHERE Nombre LIKE ?", (f"{nombre_director}%",))
        res = cursor.fetchall()
        
        # Chequeamos si hay resultados
        if not res: # Si no hay resultados
            qprint("No se encontró al director en la base de datos", style="bold fg:darkred")
            return None
        else:
            return res[0]

def guardar_pelicula(titulo: str, fecha_estreno: str, calificacion: float, descripcion: str, id_director: str) -> None:
    '''Función para guardar un nuevo título en la base de datos'''
    with sqlite3.connect(BD) as conn:
        cursor = conn.cursor()
        cursor.execute('''
                    INSERT INTO peliculas (titulo, fecha_estreno, calificacion, descripcion, id_director)
                    VALUES (?,?,?,?,?)''', (titulo, fecha_estreno, calificacion, descripcion, id_director))
        conn.commit()
        qprint("Película guardada con éxito en la base de datos",style="fg:green bold")

def guardar_director(director: str) -> None:
    '''Función para guardar un nuevo director en la base de datos'''
    with sqlite3.connect(BD) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO directores (Nombre) VALUES (?)", (director,))
        conn.commit()

def borrar_pelicula_bd(id: str) -> None:
    '''Función para borrar una película de la BD, toma como argumento el nombre de la película <titulo>'''
    with sqlite3.connect(BD) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM peliculas WHERE id = ?",(id,))
        conn.commit()
        qprint("Película borrada de la base de datos.",style="fg:green italic")

def chequear_existencia_id_pelicula(id_pelicula: str) -> bool:
    '''Función para chequear la existencia de una película. Toma como argumento el ID
    Retorna True/False'''
    with sqlite3.connect(BD) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * from peliculas WHERE id = ?",(id_pelicula,))
        res = cursor.fetchall()
        if res == []: # Si no existe
            return False
        else: # Si existe
            return True

def borrar_director_bd(id: str):
    '''Función para borrar un director de la BD, toma <ID> como argumento'''
    with sqlite3.connect(BD) as conn:
        # Primero buscamos que el ID exista
        cursor = conn.cursor()
        cursor.execute("SELECT Nombre FROM directores WHERE id = ?",(id,))
        res = cursor.fetchall()

        # Si no existe
        if res == []:
            return qprint("No se encontró el ID perteneciente a ese director en la base de datos", style="bold fg:darkred")
        else: # Si existe
            cursor.execute("DELETE FROM directores WHERE id = ?",(id,))
            conn.commit()
            qprint("Director borrado de la base de datos.",style="fg:green italic")

def contar_titulos() -> int:
    '''Función que cuenta la cantidad total de títulos en la base de datos'''
    with sqlite3.connect(BD) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT count(titulo) FROM peliculas")
        res = cursor.fetchone()
        return res[0]