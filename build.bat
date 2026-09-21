@echo off
title Rebuilding DataTransfer Executable...
echo ========================================================
echo   Force stopping running instances of DataTransfer...
echo ========================================================
taskkill /F /IM DataTransfer.exe 2>nul

echo.
echo ========================================================
echo   Building executable with PyInstaller...
echo ========================================================
python -m PyInstaller --onefile --noconsole --icon=app_icon.ico --hidden-import=webview --hidden-import=pystray --hidden-import=PIL --add-data "index.html;." --add-data "upload.html;." --add-data "app_icon.jpg;." --add-data "app_icon.ico;." app.py --name DataTransfer

echo.
echo ========================================================
echo   Build finished! Executable saved to dist\DataTransfer.exe
echo ========================================================
pause