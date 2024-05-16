import sys
import os

# Agrega la ruta al directorio que contiene tu script
script_dir = os.path.dirname(os.path.abspath(__file__))
funciones_dir = os.path.join(script_dir, '..\\')

# Agrega 'funciones' al sys.path
sys.path.append(funciones_dir)

# Ahora puedes importar la función directamente
from db.insertarDatos import conectar_db_test, cerrar_db, insertar_ultimas_ejecuciones, insertar_informacion_direcciones_ip, insertar_informacion_dominios, insertar_informacion_web_crawling, insertar_informacion_escaneo_directorios
from db.consultas import consultar_ultimas_ejecuciones, consultar_ultimas_ejecuciones_valor, consultar_ultimas_ejecuciones_where_tipo, consultar_ultimas_ejecuciones_where_tipo_valor, consultar_informacion_direcciones_ip, consultar_informacion_direcciones_ip_valor, consultar_informacion_dominios, consultar_informacion_dominios_valor, consultar_informacion_escaneo_directorios, consultar_informacion_escaneo_directorios_valor, consultar_informacion_web_crawling, consultar_informacion_web_crawling_valor


#//////////////////////////////////////////
# Start Consultas direciones ip         //
#////////////////////////////////////////
conexion = conectar_db_test()

insertar_ultimas_ejecuciones(conexion, "DireccionIP", "1.1.1.1")
insertar_informacion_direcciones_ip(conexion, "1.1.1.1", "", "")

resultados_ultima_ejecucion = consultar_ultimas_ejecuciones(conexion)
print("resultados_ultima_ejecucion:")
for resultado in resultados_ultima_ejecucion:
    print(resultado)

resultados_ultima_ejecucion_valor = consultar_ultimas_ejecuciones_valor(conexion,"1.1.1.1")
print("resultados_ultima_ejecucion_valor:")
for resultado in resultados_ultima_ejecucion_valor:
    print(resultado)

resultado_ultimas_ejecuciones_where_tipo = consultar_ultimas_ejecuciones_where_tipo(conexion, "DireccionIP")
print("resultado_ultimas_ejecuciones_where_tipo:")
for resultado in resultado_ultimas_ejecuciones_where_tipo:
    print(resultado)

resultados_ultimas_ejecuciones_where_tipo_valor = consultar_ultimas_ejecuciones_where_tipo_valor(conexion, "DireccionIP", "1.1.1.1")
print("resultados_ultimas_ejecuciones_where_tipo_valor:")
for resultado in resultados_ultimas_ejecuciones_where_tipo_valor:
    print(resultado)

resultados_informacion_direcciones_ip = consultar_informacion_direcciones_ip(conexion)
print("resultados_informacion_direcciones_ip:")
for resultado in resultados_informacion_direcciones_ip:
    print(resultado)

resultados_informacion_direcciones_ip_valor = consultar_informacion_direcciones_ip_valor(conexion, "1.1.1.1")
print("resultados_informacion_direcciones_ip_valor:")
for resultado in resultados_informacion_direcciones_ip_valor:
    print(resultado)

#//////////////////////////////////////////
# End Consultas direciones ip           //
#////////////////////////////////////////

#//////////////////////////////////////////
# Start Consultas Sub dominios          //
#////////////////////////////////////////

insertar_ultimas_ejecuciones(conexion, "Dominio", "yeraytest.com")
insertar_informacion_dominios(conexion, "yeraytest.com", "", "")

resultados_ultima_ejecucion = consultar_ultimas_ejecuciones(conexion)
print("resultados_ultima_ejecucion:")
for resultado in resultados_ultima_ejecucion:
    print(resultado)

resultados_ultima_ejecucion_valor = consultar_ultimas_ejecuciones_valor(conexion,"yeraytest.com")
print("resultados_ultima_ejecucion_valor:")
for resultado in resultados_ultima_ejecucion_valor:
    print(resultado)

resultado_ultimas_ejecuciones_where_tipo = consultar_ultimas_ejecuciones_where_tipo(conexion, "Dominio")
print("resultado_ultimas_ejecuciones_where_tipo:")
for resultado in resultado_ultimas_ejecuciones_where_tipo:
    print(resultado)

resultados_ultimas_ejecuciones_where_tipo_valor = consultar_ultimas_ejecuciones_where_tipo_valor(conexion, "Dominio", "yeraytest.com")
print("resultados_ultimas_ejecuciones_where_tipo_valor:")
for resultado in resultados_ultimas_ejecuciones_where_tipo_valor:
    print(resultado)

resultados_informacion_dominios = consultar_informacion_dominios(conexion)
print("resultados_informacion_dominios:")
for resultado in resultados_informacion_dominios:
    print(resultado)

resultados_informacion_dominios_valor = consultar_informacion_dominios_valor(conexion, "yeraytest.com")
print("resultados_informacion_dominios_valor:")
for resultado in resultados_informacion_dominios_valor:
    print(resultado)

#//////////////////////////////////////////
# End Consultas Sub dominios            //
#////////////////////////////////////////


#//////////////////////////////////////////
# Start Consultas Escaner directorios   //
#////////////////////////////////////////

insertar_ultimas_ejecuciones(conexion, "RutaEscaneo", "https://yeraytest.com")
insertar_informacion_escaneo_directorios(conexion, "https://yeraytest.com", "")

resultados_ultima_ejecucion = consultar_ultimas_ejecuciones(conexion)
print("resultados_ultima_ejecucion:")
for resultado in resultados_ultima_ejecucion:
    print(resultado)

resultados_ultima_ejecucion_valor = consultar_ultimas_ejecuciones_valor(conexion,"https://yeraytest.com")
print("resultados_ultima_ejecucion_valor:")
for resultado in resultados_ultima_ejecucion_valor:
    print(resultado)

resultado_ultimas_ejecuciones_where_tipo = consultar_ultimas_ejecuciones_where_tipo(conexion, "RutaEscaneo")
print("resultado_ultimas_ejecuciones_where_tipo:")
for resultado in resultado_ultimas_ejecuciones_where_tipo:
    print(resultado)

resultados_ultimas_ejecuciones_where_tipo_valor = consultar_ultimas_ejecuciones_where_tipo_valor(conexion, "RutaEscaneo", "https://yeraytest.com")
print("resultados_ultimas_ejecuciones_where_tipo_valor:")
for resultado in resultados_ultimas_ejecuciones_where_tipo_valor:
    print(resultado)

resultados_informacion_escaneo_directorios = consultar_informacion_escaneo_directorios(conexion)
print("resultados_informacion_escaneo_directorios:")
for resultado in resultados_informacion_escaneo_directorios:
    print(resultado)

resultados_informacion_escaneo_directorios_valor = consultar_informacion_escaneo_directorios_valor(conexion, "https://yeraytest.com")
print("resultados_informacion_escaneo_directorios_valor:")
for resultado in resultados_informacion_escaneo_directorios_valor:
    print(resultado)

#//////////////////////////////////////////
# End Consultas Escaner directorios     //
#////////////////////////////////////////

#//////////////////////////////////////////
# Start Consultas webcrawling           //
#////////////////////////////////////////

insertar_ultimas_ejecuciones(conexion, "URL", "https://yeraytest.com")
insertar_informacion_web_crawling(conexion, "https://yeraytest.com", "")

resultados_ultima_ejecucion = consultar_ultimas_ejecuciones(conexion)
print("resultados_ultima_ejecucion:")
for resultado in resultados_ultima_ejecucion:
    print(resultado)

resultados_ultima_ejecucion_valor = consultar_ultimas_ejecuciones_valor(conexion,"https://yeraytest.com")
print("resultados_ultima_ejecucion_valor:")
for resultado in resultados_ultima_ejecucion_valor:
    print(resultado)

resultado_ultimas_ejecuciones_where_tipo = consultar_ultimas_ejecuciones_where_tipo(conexion, "URL")
print("resultado_ultimas_ejecuciones_where_tipo:")
for resultado in resultado_ultimas_ejecuciones_where_tipo:
    print(resultado)

resultados_ultimas_ejecuciones_where_tipo_valor = consultar_ultimas_ejecuciones_where_tipo_valor(conexion, "URL", "https://yeraytest.com")
print("resultados_ultimas_ejecuciones_where_tipo_valor:")
for resultado in resultados_ultimas_ejecuciones_where_tipo_valor:
    print(resultado)

resultados_informacion_web_crawling = consultar_informacion_web_crawling(conexion)
print("resultados_informacion_web_crawling:")
for resultado in resultados_informacion_web_crawling:
    print(resultado)

resultados_informacion_web_crawling_valor = consultar_informacion_web_crawling_valor(conexion, "https://yeraytest.com")
print("resultados_informacion_web_crawling_valor:")
for resultado in resultados_informacion_web_crawling_valor:
    print(resultado)

#//////////////////////////////////////////
# End Consultas webcrawling             //
#////////////////////////////////////////