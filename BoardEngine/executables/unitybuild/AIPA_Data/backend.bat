setlocal
cd /d %~dp0
cd ../
cd ../
SET PATH = ./pyexe
cd pyproj
py backend_launcher.py

pause