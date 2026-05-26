@echo off
pip install -r requirements.txt
pyinstaller --noconfirm --onefile --windowed desktop_app.py
pause
