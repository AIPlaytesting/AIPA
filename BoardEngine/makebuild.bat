Rem remove py cache files
python -Bc "for p in __import__('pathlib').Path('.').rglob('*.py[co]'): p.unlink()"
python -Bc "for p in __import__('pathlib').Path('.').rglob('__pycache__'): p.rmdir()"

Rem copy python codes

Rem change config, redirect python

Rem build electron
npm run make

pause