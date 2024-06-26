@echo off

REM Detectando arquitectura del procesador
set ARCHITECTURE=x86
if "%PROCESSOR_ARCHITECTURE%" == "AMD64" set ARCHITECTURE=amd64

REM Comprobando si Python o Python3 ya están instalados
python --version >nul 2>&1
set PYTHON_INSTALLED=%errorlevel%
python3 --version >nul 2>&1
set PYTHON3_INSTALLED=%errorlevel%

if %PYTHON_INSTALLED% neq 0 if %PYTHON3_INSTALLED% neq 0 (
    echo Descargando Python 3 para arquitectura %ARCHITECTURE%...
    curl -o python-installer.exe https://www.python.org/ftp/python/3.10.11/python-3.10.11-%ARCHITECTURE%.exe

    echo Instalando Python 3...
    python-installer.exe /quiet InstallAllUsers=1 PrependPath=1

    REM Limpiando
    del python-installer.exe
) else (
    echo Python ya está instalado.
)

REM Añadiendo Python al PATH si no está presente
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Añadiendo Python al PATH...
    setx /M PATH "%PATH%;C:\Python310"
)

REM Comprobando si Nmap ya está instalado
nmap --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Descargando Nmap...
    curl -o nmap-installer.exe https://nmap.org/dist/nmap-7.91-setup.exe

    echo Instalando Nmap...
    nmap-installer.exe

    REM Limpiando
    del nmap-installer.exe
) else (
    echo Nmap ya está instalado.
)

REM Añadiendo Nmap al PATH si no está presente
nmap --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Añadiendo Nmap al PATH...
    setx /M PATH "%PATH%;C:\Program Files (x86)\Nmap"
)

REM Descargando e instalando SQLite3
sqlite3 --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Descargando SQLite3...
    if "%ARCHITECTURE%" == "amd64" (
        curl -o sqlite3.zip https://www.sqlite.org/2024/sqlite-tools-win64-x64-3360000.zip
    ) else (
        curl -o sqlite3.zip https://www.sqlite.org/2024/sqlite-tools-win32-x86-3360000.zip
    )

    echo Descomprimiendo SQLite3...
    tar -xf sqlite3.zip

    REM Limpiando
    del sqlite3.zip
) else (
    echo SQLite3 ya está instalado.
)

REM Añadiendo SQLite3 al PATH si no está presente
sqlite3 --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Añadiendo SQLite3 al PATH...
    setx /M PATH "%PATH%;C:\SQLite"
)

REM Instalando paquetes de Python desde requirements.txt si está presente
if exist requirements.txt (
    echo Instalando paquetes de Python desde requirements.txt...
    pip install -r requirements.txt
)

REM Solicitar al usuario que ingrese su API key y guardarla en el archivo apikey-virustotal.txt
echo A continuacion se va a solicitar la API key de VirusTotal la cual se va a usar para realizar peticiones a la misma y poder obtener informacion relacionada con direcciones IP.
echo Para generar el API key basta con registarse dentro de virustotal e ir a la seccion API Key.

REM Cambiar al directorio desde donde se ejecutó el script
cd /d "%~dp0"

REM Ejecutar el script de Python desde el directorio actual
if %PYTHON_INSTALLED% neq 0 ( 
    python3 recoExplorer.py\mainGetApi.py
) else (
    python recoExplorer.py\mainGetApi.py
)

echo Instalacion completada.
pause
