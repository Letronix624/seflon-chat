@echo off
color 02
title pov: you are hacking
python -m pip install --upgrade pip
python -m pip install pygame
python -m pip install pyinstaller
python -m pip install Pillow
python -m PyInstaller -F --windowed -n Seflonchat --hidden-import PIL --hidden-import PIL._imagingtk --hidden-import PIL._tkinter_finder --add-data "tkdnd2.9.2;tkdnd2.9.2/"   Seflonchat.py
title AAAAAAAAAH
