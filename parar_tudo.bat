@echo off
title NLP Suite - Encerramento Seguro

echo =======================================================
echo          ENCERRANDO SERVICOS E CONTAINERS
echo =======================================================

:: Navega até a pasta do microserviço para executar o down
cd 1_Microservico_ML

echo [INFO] Desligando motores de IA (Docker)...
docker-compose down

echo.
echo [SUCESSO] Todos os servicos foram interrompidos com seguranca.
echo =======================================================
timeout /t 5
