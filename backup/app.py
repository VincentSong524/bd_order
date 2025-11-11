from flask import Flask, render_template, request, jsonify, send_file
import json
import os
from datetime import datetime
import logging

app = Flask(__name__)

# 配置
DATA_FILE = 'data/menu.json'
BACKUP_DIR = 'data/backups'

# 确保目录存在
os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
os.makedirs(BACKUP_DIR, exist_ok=True)

def load_menu():
    """加载菜单数据"""
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)['menu']
        else:
            # 初始化默认菜单
            default_menu = [
                "宫保鸡丁", "麻婆豆腐", "水煮鱼", "回锅肉",
                "鱼香肉丝", "糖醋里脊", "清炒时蔬", "酸辣汤",
                "红烧肉", "京酱肉丝"
            ]
            save_menu(default_menu)
            return default_menu
    except Exception as e:
        logging.error(f"加载菜单失败: {e}")
        return []

def save_menu(menu):
    """保存菜单数据"""
    try:
        # 创建备份
        backup_menu()
        
        data = {
            'menu': menu,
            'last_updated': datetime.now().isoformat(),
            'total_dishes': len(menu)
        }
        
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        logging.error(f"保存菜单失败: {e}")
        return False

def backup_menu():
    """备份菜单数据"""
    try:
        if os.path.exists(DATA_FILE):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = os.path.join(BACKUP_DIR, f'menu_backup_{timestamp}.json')
            with open(DATA_FILE, 'r', encoding='utf-8') as source:
                with open(backup_file, 'w', encoding='utf-8') as target:
                    target.write(source.read())
    except Exception as e:
        logging.error(f"备份菜单失败: {e}")

@app.route('/')
def index():
    """主页"""
    menu = load_menu()
    return render_template('index.html', menu_count=len(menu))

@app.route('/api/menu', methods=['GET'])
def get_menu():
    """获取菜单API"""
    menu = load_menu()
    return jsonify({
        'success': True,
        'data': menu,
        'count': len(menu)
    })

@app.route('/api/menu', methods=['POST'])
def add_dish():
    """添加菜品API"""
    data = request.get_json()
    dish_name = data.get('name', '').strip()
    
    if not dish_name:
        return jsonify({'success': False, 'message': '菜品名称不能为空'})
    
    menu = load_menu()
    
    if dish_name in menu:
        return jsonify({'success': False, 'message': '菜品已存在'})
    
    menu.append(dish_name)
    if save_menu(menu):
        return jsonify({'success': True, 'message': '添加成功', 'data': menu})
    else:
        return jsonify({'success': False, 'message': '保存失败'})

@app.route('/api/menu/<dish_name>', methods=['DELETE'])
def delete_dish(dish_name):
    """删除菜品API"""
    menu = load_menu()
    
    if dish_name not in menu:
        return jsonify({'success': False, 'message': '菜品不存在'})
    
    menu.remove(dish_name)
    if save_menu(menu):
        return jsonify({'success': True, 'message': '删除成功', 'data': menu})
    else:
        return jsonify({'success': False, 'message': '保存失败'})

@app.route('/api/menu/<old_name>', methods=['PUT'])
def update_dish(old_name):
    """更新菜品API"""
    data = request.get_json()
    new_name = data.get('name', '').strip()
    
    if not new_name:
        return jsonify({'success': False, 'message': '菜品名称不能为空'})
    
    menu = load_menu()
    
    if old_name not in menu:
        return jsonify({'success': False, 'message': '原菜品不存在'})
    
    if new_name in menu and new_name != old_name:
        return jsonify({'success': False, 'message': '新菜品名称已存在'})
    
    index = menu.index(old_name)
    menu[index] = new_name
    
    if save_menu(menu):
        return jsonify({'success': True, 'message': '更新成功', 'data': menu})
    else:
        return jsonify({'success': False, 'message': '保存失败'})

@app.route('/api/random', methods=['POST'])
def random_order():
    """随机点单API"""
    data = request.get_json()
    count = data.get('count', 1)
    
    try:
        count = int(count)
        if count < 1:
            count = 1
    except:
        count = 1
    
    menu = load_menu()
    
    if not menu:
        return jsonify({'success': False, 'message': '菜单为空'})
    
    if count > len(menu):
        count = len(menu)
    
    import random
    selected = random.sample(menu, count)
    
    return jsonify({
        'success': True,
        'data': selected,
        'count': count,
        'total_price': f'选择了 {count} 道菜'
    })

@app.route('/api/backup', methods=['GET'])
def download_backup():
    """下载数据备份"""
    try:
        return send_file(DATA_FILE, as_attachment=True, download_name='menu_data.json')
    except Exception as e:
        return jsonify({'success': False, 'message': f'下载失败: {str(e)}'})

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """获取统计信息"""
    menu = load_menu()
    return jsonify({
        'success': True,
        'data': {
            'total_dishes': len(menu),
            'last_updated': get_last_updated(),
            'backup_count': count_backups()
        }
    })

def get_last_updated():
    """获取最后更新时间"""
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('last_updated', '未知')
    except:
        return '未知'

def count_backups():
    """计算备份文件数量"""
    try:
        return len([f for f in os.listdir(BACKUP_DIR) if f.endswith('.json')])
    except:
        return 0

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)