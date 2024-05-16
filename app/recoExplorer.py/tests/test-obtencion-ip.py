import sys
import os

# Agrega la ruta al directorio que contiene tu script
script_dir = os.path.dirname(os.path.abspath(__file__))
funciones_dir = os.path.join(script_dir, '..\\')

# Agrega 'funciones' al sys.path
sys.path.append(funciones_dir)

# Ahora puedes importar la función directamente
from portScanv2 import scan_ip
from FuncVirusTotalApi import consultar_ip, obtener_apikey
from db.insertarDatos import conectar_db_test, cerrar_db, insertar_ultimas_ejecuciones, insertar_informacion_direcciones_ip
from db.consultas import consultar_informacion_direcciones_ip_valor,consultar_informacion_direcciones_ip, consultar_ultimas_ejecuciones_where_tipo_valor, consultar_ultimas_ejecuciones_where_tipo, consultar_ultimas_ejecuciones,consultar_ultimas_ejecuciones_valor

#valor esperado una dirección ip valida "8.8.8.8" tambien se podria llegar a usar con dominios pero no es su proposito
ipEscaneoPuertos = "127.0.0.1"
ipMalformada = "657.65.87.8"
ipMalformadaLetras = "657.65.87das.8"
ipPublica = "5.24.22.243"
tipo = "DireccionIP"
# Función para conectar a la base de datos

conexion = conectar_db_test()

#Func test escaneo de puertos NMAP
escaneoCorrecto = scan_ip(ipEscaneoPuertos)
print(escaneoCorrecto)

escaneoMalformado = scan_ip(ipMalformada)
print(escaneoMalformado)

escaneoMalformadoLetra = scan_ip(ipMalformada)
print(escaneoMalformadoLetra)


#Func test Api Virustotal
api = obtener_apikey()
print(api)

virustotalCorrecto = consultar_ip(ipPublica)
print(virustotalCorrecto)

virustotalMalformado = consultar_ip(ipMalformada)
print(virustotalMalformado)


#Test inserción 
ipTest = "8.8.8.8"
escaneoInsercion = scan_ip(ipTest)
virustotalInsercion = consultar_ip(ipTest)
insertar_ultimas_ejecuciones(conexion, tipo, ipTest)
insertar_informacion_direcciones_ip(conexion, ipTest, str(virustotalInsercion), str(escaneoInsercion))

#Test Consulta 
consultar_ultimas_ejecuciones(conexion)
    
consultar_ultimas_ejecuciones_valor(conexion,ipTest)

consultar_ultimas_ejecuciones_where_tipo(conexion, tipo)
    
consultar_ultimas_ejecuciones_where_tipo_valor(conexion, tipo, ipTest)

consultar_informacion_direcciones_ip(conexion)

consultar_informacion_direcciones_ip_valor(conexion, ipTest)

cerrar_db(conexion)

