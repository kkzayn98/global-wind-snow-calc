@echo off
cd /d "%~dp0"

echo ========================================
echo  Global Wind/Snow Load Assessment Tool
echo  Zhejiang Zhongnan New Energy
echo  Dir: %CD%
echo ========================================
echo.

python --version >nul 2>&1
if errorlevel 1 goto nopython

if not exist app.py goto nofiles
if not exist WindSnowCalc.spec goto nofiles
if not exist assets\app.ico goto nofiles

echo [1/4] icon...
if exist scripts\make_icon.py python scripts\make_icon.py

echo [2/4] pip install...
python -m pip install -r requirements.txt
if errorlevel 1 goto fail

echo [3/4] clean...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

echo [4/4] PyInstaller...
python -m PyInstaller --noconfirm --clean WindSnowCalc.spec
if errorlevel 1 goto fail

if not exist dist\WindSnowCalc.exe goto fail

echo.
echo ========================================
echo  SUCCESS: dist\WindSnowCalc.exe
echo  Rename or run build.ps1 for Chinese filename
echo ========================================
echo.
pause
exit /b 0

:nopython
echo ERROR: python not found.
pause
exit /b 1

:nofiles
echo ERROR: required files missing in project root.
pause
exit /b 1

:fail
echo BUILD FAILED.
pause
exit /b 1
