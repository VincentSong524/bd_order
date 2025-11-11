#!/usr/bin/env python3
import sys
import flask

print("=== 虚拟环境测试 ===")
print(f"Python路径: {sys.executable}")
print(f"Python版本: {sys.version}")
print(f"Flask版本: {flask.__version__}")
print("虚拟环境运行正常！")