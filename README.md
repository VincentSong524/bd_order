# 🍽️ 随机点单系统 (Random Order System)

一个基于Flask的智能随机点单系统，支持菜单管理和随机点菜功能，专为餐厅、家庭或团队聚餐设计。

![Flask](https://img.shields.io/badge/Flask-2.3.3-green)
![Python](https://img.shields.io/badge/Python-3.6+-blue)
![Responsive](https://img.shields.io/badge/Design-Responsive-orange)

## ✨ 功能特性

### 🎯 核心功能
- **📋 菜单管理** - 完整的菜品增删改查功能
- **🎲 智能随机点单** - 指定数量随机选择菜品
- **📱 完全响应式** - 完美适配手机、平板、桌面设备
- **💾 数据持久化** - 使用JSON文件存储数据

### 🚀 特色功能
- **移动端优先设计** - 专为移动设备优化
- **实时交互反馈** - 流畅的动画和状态提示
- **数据备份机制** - 自动备份防止数据丢失
- **触摸友好界面** - 优化的移动端交互体验

## 🛠️ 技术栈

### 后端技术
- **Flask 2.3.3** - Python轻量级Web框架
- **RESTful API** - 前后端分离架构
- **JSON数据存储** - 简单高效的数据持久化

### 前端技术
- **原生JavaScript** - 纯JS实现，无外部依赖
- **CSS3 Grid & Flexbox** - 现代布局方案
- **移动端响应式** - 适配各种屏幕尺寸
- **CSS变量** - 统一的主题和色彩管理

## 📦 项目结构

```
bd_order/
├── app.py                 # Flask主应用
├── requirements.txt       # Python依赖列表
├── start.sh              # 应用启动脚本
├── bd_order_venv/        # Python虚拟环境
├── templates/
│   └── index.html        # 主页面模板
├── static/
│   ├── style.css         # 响应式样式文件
│   └── script.js         # 前端交互逻辑
├── data/
│   ├── menu.json         # 菜单数据文件
│   └── backups/          # 数据备份目录
└── README.md             # 项目说明文档
```

## 🚀 快速开始

### 环境要求
- Python 3.6 或更高版本
- pip 包管理工具

### 安装部署

#### 1. 克隆项目
```bash
git clone <项目地址>
cd bd_order
```

#### 2. 创建虚拟环境
```bash
python3 -m venv bd_order_venv
```

#### 3. 激活虚拟环境
```bash
source bd_order_venv/bin/activate
```

#### 4. 安装依赖
```bash
pip install -r requirements.txt
```

#### 5. 启动应用
```bash
# 使用启动脚本（推荐）
./start.sh

# 或手动启动
source bd_order_venv/bin/activate
python app.py
```

#### 6. 访问应用
打开浏览器访问：`http://你的服务器IP:5000`

### 生产环境部署

#### 使用 systemd 服务
```bash
# 创建服务文件
sudo nano /etc/systemd/system/bd-order.service
```

服务文件内容：
```ini
[Unit]
Description=BD Order System
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/developer/bd_order
ExecStart=/root/developer/bd_order/bd_order_venv/bin/python app.py
Restart=always
Environment=PYTHONPATH=/root/developer/bd_order

[Install]
WantedBy=multi-user.target
```

启用服务：
```bash
sudo systemctl daemon-reload
sudo systemctl enable bd-order
sudo systemctl start bd-order
```

#### 使用 Gunicorn（推荐生产环境）
```bash
# 安装gunicorn
pip install gunicorn

# 使用gunicorn启动
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 📖 使用指南

### 菜单管理
1. **添加菜品** - 在输入框中输入菜品名称，点击"添加菜品"
2. **编辑菜品** - 点击菜品旁的"编辑"按钮修改名称
3. **删除菜品** - 点击"删除"按钮移除菜品
4. **查看菜单** - 实时显示所有菜品列表

### 随机点单
1. **设置数量** - 在点菜数量输入框中输入需要的菜品数量
2. **开始随机** - 点击"开始随机点单"按钮
3. **查看结果** - 系统会随机选择指定数量的菜品并显示

### 移动端使用
- 系统自动适配手机屏幕
- 触摸友好的按钮和交互
- 优化的输入体验

## 🔧 API接口文档

### 菜单管理接口
| 方法 | 端点 | 描述 | 参数 |
|------|------|------|------|
| `GET` | `/api/menu` | 获取菜单列表 | 无 |
| `POST` | `/api/menu` | 添加菜品 | `{"name": "菜品名称"}` |
| `DELETE` | `/api/menu/<dish_name>` | 删除菜品 | 无 |
| `POST` | `/api/random` | 随机点单 | `{"count": 数量}` |

### 请求示例
```javascript
// 添加菜品
fetch('/api/menu', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({name: '宫保鸡丁'})
})

// 随机点单
fetch('/api/random', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({count: 3})
})
```

## 🌐 网络配置

### 服务器防火墙
```bash
# 开放5000端口
sudo ufw allow 5000
sudo ufw reload
```

### 云服务器安全组
- **协议**: TCP
- **端口**: 5000
- **来源**: 0.0.0.0/0

## 🎨 自定义配置

### 修改主题色彩
在 `static/style.css` 中修改变量：
```css
:root {
    --primary-color: #你的主色;
    --accent-color: #你的强调色;
    /* 更多颜色变量... */
}
```

### 修改默认菜单
编辑 `data/menu.json` 文件：
```json
{
    "menu": ["你的默认菜品1", "你的默认菜品2"],
    "last_updated": "2024-01-01T00:00:00",
    "total_dishes": 2
}
```

## 🐛 故障排除

### 常见问题

1. **端口无法访问**
   ```bash
   # 检查服务状态
   ps aux | grep python
   netstat -tlnp | grep 5000
   
   # 检查防火墙
   sudo ufw status
   ```

2. **依赖安装失败**
   ```bash
   # 清理并重新安装
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. **移动端显示异常**
   - 检查 viewport meta 标签
   - 验证 CSS 媒体查询
   - 测试不同设备尺寸

### 日志查看
```bash
# 查看应用日志
tail -f app.log

# 查看系统日志
journalctl -u bd-order.service
```

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request 来改进这个项目！

1. Fork 本项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- 感谢 Flask 团队提供的优秀Web框架
- 感谢所有贡献者和用户的支持

## 📞 支持

如果你遇到任何问题或有建议，请通过以下方式联系：

- 提交 [Issue](https://github.com/your-repo/issues)
- 发送邮件至: your-email@example.com

---

**享受智能点单的乐趣！** 🎉
