setlocal
cd /d %~dp0
SET PATH = ./pyexe
cd pyproj
py electron_backend.py