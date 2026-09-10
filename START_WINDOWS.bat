@echo off
cd /d "%~dp0"
py -3 START.py
if errorlevel 1 python START.py
pause
