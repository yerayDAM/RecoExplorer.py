@echo off

REM Comprobando si Python o Python3 ya están instalados
python --version >nul 2>&1
set PYTHON_INSTALLED=%errorlevel%
python3 --version >nul 2>&1
set PYTHON3_INSTALLED=%errorlevel%

REM Cambiar al directorio desde donde se ejecutó el script
cd /d "%~dp0"

REM Ejecutar el script de Python desde el directorio actual
if %PYTHON_INSTALLED% neq 0 ( 
    python3 recoExplorer.py\mainGetApi.py
) else (
    python recoExplorer.py\mainGetApi.py
)


REM Obtener el ID del proceso de Python
for /f "tokens=2" %%I in ('tasklist /fi "imagename eq python3.exe" /fo table /nh') do (
    set "PID=%%I"
)

REM Cerrar este script de lote cuando se cierre el proceso de Python
taskkill /pid %PID%
