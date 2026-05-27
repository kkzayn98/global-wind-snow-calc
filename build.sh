#!/bin/bash
# macOS/Linux local test build (Windows .exe 请在 Windows 上运行 build.bat)
set -e
echo "编制：浙江中南新能源有限公司技术部 董子凌"
pip install -r requirements.txt
rm -rf build dist
pyinstaller --noconfirm --clean --onefile --windowed \
  --name "wind-snow-calc" \
  --add-data "index.html:." \
  --add-data "data/cities.js:data" \
  --add-data "data/global.js:data" \
  --add-data "data/meta.js:data" \
  --add-data "data/world-map.svg:data" \
  --add-data "js/app.js:js" \
  app.py
echo "Build complete: dist/wind-snow-calc (macOS/Linux test binary)"
echo "Windows 正式包请使用 build.bat"
