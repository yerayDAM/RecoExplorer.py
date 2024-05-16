import sys
import os

# Agrega la ruta al directorio que contiene tu script
script_dir = os.path.dirname(os.path.abspath(__file__))
funciones_dir = os.path.join(script_dir, '..\\')

# Agrega 'funciones' al sys.path
sys.path.append(funciones_dir)

# Ahora puedes importar la función directamente
from subd import subDomain, obtener_imagen_dns_dumpster
from db.insertarDatos import conectar_db_test, cerrar_db, insertar_ultimas_ejecuciones, insertar_informacion_dominios
from db.consultas import consultar_ultimas_ejecuciones, consultar_ultimas_ejecuciones_valor, consultar_ultimas_ejecuciones_where_tipo, consultar_ultimas_ejecuciones_where_tipo_valor, consultar_informacion_dominios, consultar_informacion_dominios_valor

#valor esperado un dominio de segundo nivel "intelequia.com"
dominio = "marca.com"
dominioMalformado = "https://marca.com"
ipNoAceptada = "8.8.8.8"

resultDominio = subDomain(dominio)
rutaImagen = obtener_imagen_dns_dumpster(dominio)
print(resultDominio)
print(rutaImagen)

resultDominioMalformado = subDomain(dominioMalformado)
rutaImagenMalformado = obtener_imagen_dns_dumpster(dominioMalformado)
print(resultDominioMalformado)
print(rutaImagenMalformado)

resultipNoAceptada = subDomain(ipNoAceptada)
rutaImagenIpNoAceptada = obtener_imagen_dns_dumpster(resultipNoAceptada)
print(resultipNoAceptada)
print(rutaImagenIpNoAceptada)

conexion = conectar_db_test()
insertar_ultimas_ejecuciones(conexion, "Dominio", dominio)
insertar_informacion_dominios(conexion, dominio, rutaImagen, str(resultDominio))

resultados_dominios = consultar_informacion_dominios(conexion)
print("Todos los resultado:")
for resultado in resultados_dominios:
    print(resultado)

resultados_dominios_valor = consultar_informacion_dominios_valor(conexion,dominio)
print("resultado por valor:")
for resultado in resultados_dominios_valor:
    print(resultado)

cerrar_db(conexion)

