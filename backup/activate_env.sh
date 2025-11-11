#!/bin/bash
cd "$(dirname "$0")"
source bd_order_venv/bin/activate
echo "虚拟环境 bd_order_venv 已激活"
echo "当前Python: $(which python)"
echo "Python版本: $(python --version)"