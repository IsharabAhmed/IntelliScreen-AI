@echo off
set VENV_PYTHON=venv\Scripts\python.exe

if exist "%VENV_PYTHON%" (
    "%VENV_PYTHON%" run.py %*
) else (
    python run.py %*
)
