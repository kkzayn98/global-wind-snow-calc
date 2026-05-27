#!/usr/bin/env python3
"""Create release zip with runtime + source files for Windows build."""
import os
import shutil
import zipfile
from datetime import datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
RELEASE_DIR = os.path.join(ROOT, "release")
VERSION = "1.0.0"
APP_NAME = "全球风压雪压计算评估工具"
AUTHOR = "浙江中南新能源有限公司技术部 董子凌"

RUNTIME = [
    "app.py",
    "index.html",
    "js/app.js",
    "data/cities.js",
    "data/global.js",
    "data/meta.js",
    "data/world-map.svg",
    "assets/app.ico",
]

SOURCE = RUNTIME + [
    "serve.py",
    "requirements.txt",
    "build.bat",
    "build.ps1",
    "build_installer.bat",
    "build.sh",
    "version_info.txt",
    "WindSnowCalc.spec",
    "installer.iss",
    "README.md",
    "scripts/build_global_data.py",
    "scripts/build_world_map.mjs",
    "scripts/make_icon.py",
    "scripts/parse_gb50009.py",
    "scripts/data/countries-110m.json",
]


def add_to_zip(zf: zipfile.ZipFile, rel_path: str) -> None:
    full = os.path.join(ROOT, rel_path)
    if os.path.isfile(full):
        zf.write(full, os.path.join(APP_NAME, rel_path.replace("\\", "/")))
    elif os.path.isdir(full):
        for dirpath, _, filenames in os.walk(full):
            for name in filenames:
                fp = os.path.join(dirpath, name)
                arc = os.path.join(APP_NAME, os.path.relpath(fp, ROOT).replace("\\", "/"))
                zf.write(fp, arc)


def main() -> None:
    os.makedirs(RELEASE_DIR, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d")
    zip_name = os.path.join(RELEASE_DIR, f"{APP_NAME}_v{VERSION}_{stamp}.zip")

    with zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED) as zf:
        for rel in SOURCE:
            add_to_zip(zf, rel)
        readme = (
            f"{APP_NAME} v{VERSION}\r\n"
            f"编制单位：{AUTHOR}\r\n\r\n"
            "Windows 打包：\r\n"
            "  1. 安装 Python 3.9+\r\n"
            "  2. 双击 build.bat 或 powershell -File build.ps1\r\n"
            "  3. 输出 dist\\全球风压雪压计算评估工具.exe\r\n\r\n"
            "开发调试（浏览器）：python serve.py\r\n"
            "桌面运行：python app.py\r\n"
        )
        zf.writestr(f"{APP_NAME}/使用说明.txt", readme.encode("utf-8-sig"))

    exe_zh = os.path.join(ROOT, "dist", f"{APP_NAME}.exe")
    if os.path.isfile(exe_zh):
        shutil.copy2(exe_zh, os.path.join(RELEASE_DIR, f"{APP_NAME}_v{VERSION}.exe"))

    print(f"Release zip: {zip_name}")


if __name__ == "__main__":
    main()
