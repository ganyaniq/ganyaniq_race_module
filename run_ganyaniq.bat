@echo off
cd /d %~dp0
uvicorn ganyaniq_race_module.main:app --reload --port 10000
pause
