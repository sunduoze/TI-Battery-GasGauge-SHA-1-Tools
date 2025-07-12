#!/bin/bash
set -e

# 安装依赖
pip install -r requirements.txt pyinstaller

# 平台特定的构建
if [[ "$RUNNER_OS" == "Windows" ]]; then
    pyinstaller --onefile --name myapp-windows source/main.py
    cd dist
    zip -r myapp-windows.zip myapp-windows.exe
elif [[ "$RUNNER_OS" == "macOS" ]]; then
    pyinstaller --onefile --name myapp-macos source/main.py
    cd dist
    zip -r myapp-macos.zip myapp-macos
else  # Linux
    pyinstaller --onefile --name myapp-linux source/main.py
    cd dist
    zip -r myapp-linux.zip myapp-linux
fi