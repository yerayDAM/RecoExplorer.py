import sys
import os

# Agrega la ruta al directorio que contiene tu script
script_dir = os.path.dirname(os.path.abspath(__file__))
funciones_dir = os.path.join(script_dir, '..\\')

# Agrega 'funciones' al sys.path
sys.path.append(funciones_dir)

# Ahora puedes importar la función directamente
from webCrawlingv2 import obtener_contenido_html
from db.insertarDatos import conectar_db_test, cerrar_db, insertar_ultimas_ejecuciones, insertar_informacion_web_crawling
from db.consultas import consultar_ultimas_ejecuciones, consultar_ultimas_ejecuciones_valor, consultar_ultimas_ejecuciones_where_tipo, consultar_ultimas_ejecuciones_where_tipo_valor, consultar_informacion_web_crawling, consultar_informacion_web_crawling_valor

url = "https://intelequia.com/ciberseguridad"
urlMalformada = "haaps://intelequia.com/ciberseguridad"
urlSinProtocolo = "intelequia.com/ciberseguridad"

resultado = obtener_contenido_html(url)
print(resultado)

resultadoUrlMalformada = obtener_contenido_html(urlMalformada)
print(resultadoUrlMalformada)

resultadoUrlSinProtocolo = obtener_contenido_html(urlSinProtocolo)
print(resultadoUrlSinProtocolo)

conexion = conectar_db_test()
insertar_ultimas_ejecuciones(conexion, "URL", url)
insertar_informacion_web_crawling(conexion, url, str(resultado))

resultados_ultima_ejecucion = consultar_ultimas_ejecuciones_valor(conexion,url)
print("resultado ultima ejecucion:")
for resultado in resultados_ultima_ejecucion:
    print(resultado)

resultados_webcrawling = consultar_informacion_web_crawling(conexion)
print("Todos los resultado:")
for resultado in resultados_webcrawling:
    print(resultado)

resultados_webcrawling_valor = consultar_informacion_web_crawling_valor(conexion,url)
print("resultado por valor:")
for resultado in resultados_webcrawling_valor:
    print(resultado)

cerrar_db(conexion)