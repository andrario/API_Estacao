#!/bin/sh
echo Iniciando Scheduler py
cd /home/pi/Documents/Codigos/API_Estacao
lxterminal -e sudo ./bin/python3 flask_aps.py
exit