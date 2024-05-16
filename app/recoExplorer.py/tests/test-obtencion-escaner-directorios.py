import sys
import os

# Agrega la ruta al directorio que contiene tu script
script_dir = os.path.dirname(os.path.abspath(__file__))
funciones_dir = os.path.join(script_dir, '..\\')

# Agrega 'funciones' al sys.path
sys.path.append(funciones_dir)

# Ahora puedes importar la función directamente
from directoryListingFunction import check_wordlist_for_domain
from db.insertarDatos import conectar_db_test, cerrar_db, insertar_ultimas_ejecuciones, insertar_informacion_escaneo_directorios
from db.consultas import consultar_ultimas_ejecuciones, consultar_ultimas_ejecuciones_valor, consultar_ultimas_ejecuciones_where_tipo, consultar_ultimas_ejecuciones_where_tipo_valor, consultar_informacion_escaneo_directorios, consultar_informacion_escaneo_directorios_valor

#valor esperado una url que no temina en barra "https://marca.com/es/test"
url = "https://marca.com"
urlMalformada = "htpa://marca.com"
urlSinProtocolo = "marca.com/"

resultado = check_wordlist_for_domain(url)
print(resultado)

resultadoUrlMalformada = check_wordlist_for_domain(urlMalformada)
print(resultadoUrlMalformada)

resultadoUrlSinProtocolo = check_wordlist_for_domain(urlSinProtocolo)
print(resultadoUrlSinProtocolo)

conexion = conectar_db_test()
insertar_ultimas_ejecuciones(conexion, "RutaEscaneo", url)
insertar_informacion_escaneo_directorios(conexion, url, str(resultado))


resultados_ultima_ejecucion = consultar_ultimas_ejecuciones_valor(conexion,url)
print("resultado ultima ejecucion:")
for resultado in resultados_ultima_ejecucion:
    print(resultado)

resultados_escaneo_directorios = consultar_informacion_escaneo_directorios(conexion)
print("Todos los resultado:")
for resultado in resultados_escaneo_directorios:
    print(resultado)

resultados_escaneo_directorios_valor = consultar_informacion_escaneo_directorios_valor(conexion,url)
print("resultado por valor:")
for resultado in resultados_escaneo_directorios_valor:
    print(resultado)

cerrar_db(conexion)






