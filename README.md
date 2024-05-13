# RecoExplorer.py
Esta herramienta esta desarrollada en python y la cual tiene como objetivo agrupar varias herramientas usadas durante las fases de reconocimiento / obtención de información en los primeros pasos de una auditoria ejecutanda por los equipos de red team dentro de una interfaz grafica. 

Se van a agrupar las siguientes herramientas:
  - Herramienta de obtención de información relacionada con direcciones IP la cual usa la api de virus total y tambien se integra un escaner de puertos.
  - Herramienta de obtención de información de sub dominios y generación de un mapa de dominios.
  - Herramienta de escaner de directorios y subdirectorios.
  - Herramienta de Webcrawling para generar un listado de enlaces pertenecientes en el contenido de una requests HTTP.

Los resultaddos generados por las herramientas mencionadas anteriormente se van a almacenar dentro de una base de datos la cual usa SQLite3 para alamacenar los datos en local y asi poder consultarlos en cualquier momento.

RecoExplorer.py es una herramienta desarrollada en python, usando el framework PyQt5 para diseñar e implementar el frontend. Por otro lado, se van a listar las librerias, aplicaciones y endpoints usados por la herramienta y el desarrollo de RecoExplorer.py:
- Librerias / Aplicaciones:
  - Qt5 Desinger: editor para el diseño frontend.
  - PyQt5: Framework usado para generar el frontend.
  - Python: Lenguaje de programación usado para el desarrollo de la aplicación.
  - python-nmap: Librería de python con la funcionalidad de interactuar con nmap.
  - urllib3: Librería de python para acceder y utilizar recursos de internet identificados por url.
  - Requests: Librería de python para hacer requests HTTP/s.
  - Beautifulsoup4: Librería de python para realizar parseos de los resultados de las requests HTTP/s.
  - Pillow: Librería de python para tratar imagenes.
  - PySide2: Librería de python que hace bindings para el framework PyQt5.
  - SQLite 3: Sistema de base de datos local.
  - CSS: Estilos para el frontend usados dentro del editor Qt5 Designer.
  - Atom / Sublime: Editores de código.
  - Lucid.app: Herramienta web para generar los diagramas.

- Endpoints  
  - Direcciones ips  
	 - https://www.virustotal.com/api/v3/ip_addresses/{ip}  
  - Subdominios  
	- https://crt.sh/?q={domain}&output=json  
	- https://api.hackertarget.com/hostsearch/?q={domain}  
	- https://rapiddns.io/subdomain/{domain}#result  
	- https://otx.alienvault.com/api/v1/indicators/domain/{domain}/passive_dns  
	- https://urlscan.io/api/v1/search/?q={domain}  
	- https://riddler.io/search/exportcsv?q=pld:{domain}  
	- https://api.threatminer.org/v2/domain.php?q={domain}&rt=5  
	- https://dnsdumpster.com/  
	- https://dnsdumpster.com/static/map/{domain}.png  
---
## Proceso de instalación
Para comenzar con el proceso de instalación se va a clonar el repositorio.

'git clone https://github.com/yerayDAM/RecoExplorer.py'

Una vez clonado el repositorio dependiendo del sistema operativo usado se va a seguir unos pasos u otros. Primero se va a mostrar el procesos de instalación en Windows.

### Sistema operativo Windows:
Para realizar el proceso de instalación se puede realizar de dos maneras, las cuales se van a detallar a continuación:

#### Proceso automatizado.
Para comenzar con el proceso automatizado ir al directorio donde se clono el repositorio y ejecutar el fichero intaladorWindows.bat con permisos de administrador. Este script va realizar la descarga, instalación y configuración de la api de Virustotal usados por la aplicación. En este caso, se van a instalar las siguientes versiones y añadirlas al PATH:
  • Python versión 3.10.2 (https://www.python.org/downloads/release/python-3102/).
  • NMAP versión 7.91 (https://nmap.org/dist/nmap-7.91-setup.exe).
  • SQLite3 (https://www.sqlite.org/2024/sqlite-tools-win32-x86-3360000.zip).
El script continuara ejecutando la actualización del modulo PIP para continuar con la instalación de las dependencias para python usando el fichero requirements.txt y para finalizar se va a abrir una ventana donde va a pedir que se ingrese la api key de Virustotal para poder usar la funcionalidad de obtención de información sobre direcciones IPs.

Una vez realizado exitosamente el proceso anterior para ejecutar la aplicación se tendria que acceder al directorio recoExplorer.py/ y ejecutar el fichero llamado RecoExplorer.bat para lanzar la aplicación.

#### Proceso manual.
Para comenzar con el proceso manual se van a tener que instalar las siguientes aplicaciones (Las versiones comentadas fueron las usadas para generar la aplicación pero se pueden instalar versiones superiores):
  • Python versión 3.10.2 (https://www.python.org/downloads/release/python-3102/).
  • NMAP versión 7.91 (https://nmap.org/dist/nmap-7.91-setup.exe).
  • SQLite3 (https://www.sqlite.org/2024/sqlite-tools-win32-x86-3360000.zip).
Una vez instaladas las aplicaciones mencionadas anteriormente procede a acceder a la una consola y dirigirte al directorio donde se clone el repositorio 

`cd {RutaDondeSeClono}/`

Al esta en la ruta donde se clono el repositorio acceder al directorio app/recoExplorer.py y ejecutar el comando comentado.

'cd app/recoExplorer.py'
'pip install -r requirements.txt' ###puede que pida permisos de adminstrador. Para ello cerrar el cmd y abrir uno nuevo con permisos.

Con las dependencias ya instaladas lo que faltaria para poder ejecutar la aplicación con todas sus funcionalidades, se tiene que añadir el valor de api key de Virustotal dentro del fichero apikey-virustotal.txt o bien ejecutar el siguiente comando para abrir la interfaz grafica y añadir desde ahi el valor de la api key.

'python main-GetApi.py'

Ya estaria listo el entorno para poder usar la apliación, solo bastaria con ejecutar el fichero RecoExplorer.bat o desde consola estando dentro de la ruta {rutaDondeSeClono}/app/recoExplorer.py ejecutar el script principal.

'python main.py'

---

### Funcionamiento de la aplicación
Dentro de este apartado se va a comentar el funcionamiento de cada una de las herramientas integradas dentro de la interfaz.

#### Vista pricipal.
En la vista pricipal se van a mostrar varios botones los cuales te moveran a la vista de las diferentes herramientas.

#### Vista de obtención de información de direcciones IPs
En esta vista se encuentran agrupadas dos funcionalidades. la primera una petición a la api de Virustotal para obtener información acerca de ip introducida y tambien la funcionalidad de realizar escaneos de puertos de los primeros 1024 puertos usando NMAP. Ambos resultados se van a almacenar dentro de la base de datos para poder ser consultados cuando sean necesarios.

#### Vista de obtención de subdominios.


