from flask import Flask, render_template, request, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)

# 配置
DATA_FILE = 'data/menu.json'

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
        print(f"加载菜单失败: {e}")
        return []

def save_menu(menu):
    """保存菜单数据"""
    try:
        data = {
            'menu': menu,
            'last_updated': datetime.now().isoformat(),
            'total_dishes': len(menu)
        }
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"保存菜单失败: {e}")
        return False

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
        'count': count
    })

if __name__ == '__main__':
    # 确保数据目录存在
    os.makedirs('data', exist_ok=True)
    app.run(host='0.0.0.0', port=5000, debug=True)
