@echo off

REM Comprobar si python o python3 está disponible
where python >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=python
) else (
    where python3 >nul 2>&1
    if %errorlevel% equ 0 (
        set PYTHON_CMD=python3
    ) else (
        echo No se encontró python ni python3 en el PATH
        exit /b 1
    )
)

REM Ejecutar el script de Python en segundo plano sin abrir una nueva ventana
start /B %PYTHON_CMD% main.py

REM Obtener el ID del proceso de Python
for /f "tokens=2" %%I in ('tasklist /fi "imagename eq %PYTHON_CMD%.exe" /fo table /nh') do (
    set "PID=%%I"
)

REM Cerrar este script de lote cuando se cierre el proceso de Python
taskkill /pid %PID%
