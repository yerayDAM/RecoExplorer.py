@echo off

REM Ejecutar el script de Python en segundo plano sin abrir una nueva ventana
start /B python3 main.py



REM Obtener el ID del proceso de Python
for /f "tokens=2" %%I in ('tasklist /fi "imagename eq python3.exe" /fo table /nh') do (
    set "PID=%%I"
)

REM Cerrar este script de lote cuando se cierre el proceso de Python
taskkill /pid %PID%
