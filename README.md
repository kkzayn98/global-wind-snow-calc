# 全球风压雪压计算评估工具

**编制单位：** 浙江中南新能源有限公司技术部  
**作者：** 董子凌

基于《建筑结构荷载规范》**GB 50009-2012** 及全球多国建筑风/雪荷载规范的查询与换算工具。支持按洲/国、大区、城市三级选择，自动计算不同设计重现期下的基本风压、雪压，并提供多单位换算。

> **交付形式：** Windows 桌面程序（`.exe` / 安装包）。浏览器访问仅用于开发调试。

## 功能特性

- **国内数据**：GB 50009-2012 附录 E.5，464 个城市/站点
- **全球数据**：77 个国家/地区、500 个代表城区
- **世界地图**：悬停/点击六大洲联动选择
- **模糊搜索**：输入城市名快速定位
- **重现期换算**：10 / 25 / 50 / 100 年
- **中英双语**界面

## 用户使用（Windows）

### 方式一：安装包（推荐）

在 Windows 上由开发人员执行 `build_installer.bat` 后，将 `release\风压雪压计算工具_安装包_v1.0.0.exe` 分发给用户。用户双击安装，从开始菜单或桌面启动。

### 方式二：绿色版 exe

运行 `build.bat` 后，将 `dist\风压雪压计算工具.exe` 直接发给用户，双击即可运行，无需安装。

## 开发与调试

### 环境要求

- Python 3.9+
- Windows（打包 exe / 安装包）

### 浏览器调试（仅开发）

```bash
python serve.py
```

浏览器打开终端提示的地址，例如 `http://127.0.0.1:8080/index.html`。

### 桌面预览

```bash
pip install -r requirements.txt
python app.py
```

### Windows 打包 exe

**双击 `build.bat`**（纯英文脚本，避免中文乱码）。若 bat 仍有问题，用 PowerShell：

```powershell
powershell -ExecutionPolicy Bypass -File build.ps1
```

成功输出：`dist\WindSnowCalc.exe`（`build.ps1` 还会复制为 `dist\全球风压雪压计算评估工具.exe`）

手动命令（你已验证可用）：

```bat
python -m pip install -r requirements.txt
python -m PyInstaller --noconfirm --clean WindSnowCalc.spec
```

### Windows 打包安装程序

需先安装 [Inno Setup 6](https://jrsoftware.org/isinfo.php)，然后：

```bat
build_installer.bat
```

输出：`release\风压雪压计算工具_安装包_v1.0.0.exe`

### 生成发布压缩包

```bash
python pack.py
```

输出：`release/风压雪压计算工具_v1.0.0_YYYYMMDD.zip`（含源码与构建脚本，供 Windows 环境打包）

## 项目结构

```
calc/
├── app.py                  # 桌面版启动（pywebview）
├── serve.py                # 浏览器调试服务（不随 exe 发布）
├── index.html              # 界面
├── js/app.js               # 交互逻辑
├── data/                   # 运行时数据
│   ├── cities.js
│   ├── global.js
│   ├── meta.js
│   └── world-map.svg
├── build.bat               # Windows exe 打包
├── build_installer.bat     # Windows 安装包打包
├── installer.iss           # Inno Setup 脚本
├── version_info.txt        # exe 版本信息
├── pack.py                 # 发布 zip
├── requirements.txt
└── scripts/                # 数据/地图维护脚本（开发用）
    ├── build_global_data.py
    ├── build_world_map.mjs
    ├── parse_gb50009.py
    └── data/countries-110m.json
```

## 免责声明

本工具仅供设计参考与方案比选，不构成正式设计依据。使用者应自行核对当地气象资料、规范条文及主管部门要求，并对工程设计结果负责。
