@echo off
setlocal enabledelayedexpansion
title NLP Suite - Inicializador Corporativo

echo =======================================================
echo           INICIALIZANDO ECOSSISTEMA NLP IA
echo =======================================================

:: 1. Iniciar o Backend de IA (Docker)
echo [1/3] Ligando o motor de Inteligencia Artificial (Docker)...
cd 1_Microservico_ML
docker-compose up -d --build
if %errorlevel% neq 0 (
    echo.
    echo [ERRO FATAL] Falha ao conectar com o Docker.
    echo Por favor, abra o aplicativo 'Docker Desktop' no Windows, espere a luz ficar verde e tente de novo!
    pause
    exit /b
)
cd ..

:: 2. Validar o Frontend
echo [2/3] Validando dependencias da Interface Visual...
pip install -q -r 2_Interface_Visual\requirements_ui.txt

:: 3. Iniciar o Painel Streamlit
echo [3/3] Iniciando Painel de Controle...
echo O navegador abrira automaticamente em instantes.
echo.
echo [INFO] Para encerrar, feche esta janela ou use o script 'parar_tudo.bat'.
echo =======================================================

cd 2_Interface_Visual
python -m streamlit run app_ui.py

pause