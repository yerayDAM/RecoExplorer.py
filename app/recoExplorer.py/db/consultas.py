import sqlite3
import os

# Función para conectar a la base de datos
def conectar_db():
    directorio_actual = os.getcwd()

    # Construir la ruta completa al archivo de la base de datos
    ruta_base_datos = os.path.join(directorio_actual, 'db/database.db')
    conexion = sqlite3.connect(ruta_base_datos)
    return conexion

# Función para cerrar la conexión a la base de datos
def cerrar_db(conexion):
    conexion.close()

def consultar_ultimas_ejecuciones(conexion):
    print("adiooooooos")
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM UltimasEjecuciones")
    resultados = cursor.fetchall()
    return resultados
    
def consultar_ultimas_ejecuciones_valor(conexion,valor):
    print("adiooooooos")
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM UltimasEjecuciones WHERE Valor LIKE ?", ('%' + valor + '%',))
    resultados = cursor.fetchall()
    return resultados

def consultar_ultimas_ejecuciones_where_tipo(conexion, tipo):
    print("holaaaaaaaaa")
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM UltimasEjecuciones WHERE Tipo = ?", (tipo,))
    resultados = cursor.fetchall()
    return resultados

def consultar_ultimas_ejecuciones_where_tipo_valor(conexion, tipo, valor):
    print("holaaaaaaaaa")
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM UltimasEjecuciones WHERE Tipo = ? AND Valor LIKE ?", (tipo, '%' + valor + '%',))
    resultados = cursor.fetchall()
    return resultados

def consultar_informacion_direcciones_ip(conexion):
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM InformacionDireccionesIP")
    resultados = cursor.fetchall()
    return resultados

def consultar_informacion_direcciones_ip_valor(conexion,valor):
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM InformacionDireccionesIP WHERE DireccionIP LIKE ?", (valor,))
    resultados = cursor.fetchall()
    return resultados

def consultar_informacion_dominios(conexion):
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM InformacionDominios")
    resultados = cursor.fetchall()
    return resultados

def consultar_informacion_dominios_valor(conexion,valor):
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM InformacionDominios WHERE Dominio LIKE ?", (valor,))
    resultados = cursor.fetchall()
    return resultados

def consultar_informacion_escaneo_directorios(conexion):
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM InformacionEscaneoDirectorios")
    resultados = cursor.fetchall()
    return resultados

def consultar_informacion_escaneo_directorios_valor(conexion,valor):
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM InformacionEscaneoDirectorios WHERE DirectorioDominio LIKE ?", (valor,))
    resultados = cursor.fetchall()
    return resultados

def consultar_informacion_web_crawling(conexion):
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM InformacionWebCrawling")
    resultados = cursor.fetchall()
    return resultados

def consultar_informacion_web_crawling_valor(conexion,valor):
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM InformacionWebCrawling WHERE URL LIKE ?", (valor,))
    resultados = cursor.fetchall()
    return resultados

# Ejemplo de uso:
#conexion = conectar_db()

# Consultar todos los registros de la tabla de Últimas Ejecuciones
#resultados_ultimas_ejecuciones = consultar_ultimas_ejecuciones(conexion)
#print("Últimas Ejecuciones:")
#for resultado in resultados_ultimas_ejecuciones:
#    print(resultado)

# Consultar registros de la tabla de Últimas Ejecuciones filtrados por tipo
#tipo_a_consultar = "DireccionIP"
#resultados_ultimas_ejecuciones_tipo = consultar_ultimas_ejecuciones_where_valor(conexion, tipo_a_consultar)
#print(f"\nÚltimas Ejecuciones de tipo '{tipo_a_consultar}':")
#for resultado in resultados_ultimas_ejecuciones_tipo:
#    print(resultado)

#cerrar_db(conexion)