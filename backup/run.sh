#!/bin/bash

# 随机点单系统启动脚本

echo "正在启动随机点单系统..."

# 检查Python3
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到Python3，请先安装Python3"
    exit 1
fi

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "激活虚拟环境..."
source venv/bin/activate

# 安装依赖
echo "安装依赖..."
pip install -r requirements.txt

# 创建数据目录
mkdir -p data/backups

# 启动应用
echo "启动Flask应用..."
echo "访问地址: http://服务器IP:5000"
python3 app.py