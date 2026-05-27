@echo off
cd /d "%~dp0"
call build.bat
if errorlevel 1 exit /b 1

where iscc >nul 2>&1
if errorlevel 1 goto noiscc

iscc installer.iss
if errorlevel 1 exit /b 1

echo SUCCESS: release\WindSnowCalc_Setup_v1.0.0.exe
pause
exit /b 0

:noiscc
echo ERROR: Inno Setup iscc not found in PATH.
echo Install Inno Setup 6, then run: iscc installer.iss
pause
exit /b 1
