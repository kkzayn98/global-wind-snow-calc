# Windows build script (PowerShell)
# Run: powershell -ExecutionPolicy Bypass -File build.ps1
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

$AppExeZh = "全球风压雪压计算评估工具.exe"

Write-Host "Building Global Wind/Snow Calculator..." -ForegroundColor Cyan
python --version
if ($LASTEXITCODE -ne 0) { throw "python not found" }

foreach ($f in @("app.py", "WindSnowCalc.spec", "index.html", "assets/app.ico")) {
    if (-not (Test-Path $f)) { throw "Missing file: $f" }
}

if (Test-Path "scripts/make_icon.py") {
    python scripts/make_icon.py
}

python -m pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) { throw "pip install failed" }

if (Test-Path build) { Remove-Item build -Recurse -Force }
if (Test-Path dist) { Remove-Item dist -Recurse -Force }

python -m PyInstaller --noconfirm --clean WindSnowCalc.spec
if ($LASTEXITCODE -ne 0) { throw "PyInstaller failed" }

$exe = Join-Path dist "WindSnowCalc.exe"
if (-not (Test-Path $exe)) { throw "dist\WindSnowCalc.exe not created" }

$zh = Join-Path dist $AppExeZh
Copy-Item -LiteralPath $exe -Destination $zh -Force
Write-Host "SUCCESS:" -ForegroundColor Green
Write-Host "  $exe"
Write-Host "  $zh"
