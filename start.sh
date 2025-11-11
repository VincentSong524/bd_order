#!/bin/bash

echo "=== BD Order System 启动 ==="

# 进入脚本所在目录
cd "$(dirname "$0")"

# 检查虚拟环境是否存在
if [ ! -d "bd_order_venv" ]; then
    echo "错误: 虚拟环境 bd_order_venv 不存在"
    echo "请运行: python3 -m venv bd_order_venv"
    exit 1
fi

# 激活虚拟环境
echo "激活虚拟环境 bd_order_venv..."
source bd_order_venv/bin/activate

# 检查并安装依赖
if [ -f "requirements.txt" ]; then
    echo "安装依赖..."
    pip install -r requirements.txt
fi

# 启动应用
echo "启动 BD Order System..."
echo "======================================"
echo "应用地址: http://0.0.0.0:5000"
echo "外部访问: http://你的服务器IP:5000"
echo "按 Ctrl+C 停止应用"
echo "======================================"

python app.py
