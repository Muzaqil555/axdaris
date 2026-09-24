@echo off
chcp 65001 > nul
title AI Musteri Tapan - Dashboard
echo ==================================================
echo    AI Instagram Musteri Tapan - Bashlaniir...
echo ==================================================
echo.
echo  Brauzer bir saniye sonra acilacaq...
echo  Baglamaq ucun bu pencerani baglayin.
echo.
timeout /t 2 /nobreak > nul
start http://localhost:8000
py -m uvicorn server:app --host 0.0.0.0 --port 8000
pause
