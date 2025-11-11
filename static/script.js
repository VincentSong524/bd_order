// API基础URL
const API_BASE = '/api';

// 全局变量
let currentEditDish = '';

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    loadMenu();
    setupEventListeners();
});

function setupEventListeners() {
    // 模态框关闭事件
    const modal = document.getElementById('editModal');
    const closeBtn = document.querySelector('.close');
    
    closeBtn.onclick = function() {
        modal.style.display = 'none';
    }

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    }

    // 回车键添加菜品
    document.getElementById('dishName').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            addDish();
        }
    });
}

// API请求函数
async function apiRequest(endpoint, options = {}) {
    try {
        const response = await fetch(`${API_BASE}${endpoint}`, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });
        
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('API请求失败:', error);
        showNotification('网络请求失败，请检查服务器状态', 'error');
        return { success: false, message: '网络请求失败' };
    }
}

// 加载菜单
async function loadMenu() {
    const result = await apiRequest('/menu');
    
    if (result.success) {
        displayMenu(result.data);
    } else {
        showNotification('加载菜单失败: ' + result.message, 'error');
    }
}

// 显示菜单
function displayMenu(menu) {
    const menuList = document.getElementById('menuList');
    
    if (menu.length === 0) {
        menuList.innerHTML = '<div class="empty-state">菜单为空，请添加菜品</div>';
        return;
    }

    menuList.innerHTML = menu.map(dish => `
        <div class="dish-item">
            <div class="dish-info">${dish}</div>
            <div class="dish-actions">
                <button class="edit-btn" onclick="openEditModal('${dish}')">编辑</button>
                <button class="delete-btn" onclick="deleteDish('${dish}')">删除</button>
            </div>
        </div>
    `).join('');
}

// 添加菜品
async function addDish() {
    const dishInput = document.getElementById('dishName');
    const dishName = dishInput.value.trim();

    if (!dishName) {
        showNotification('请输入菜品名称', 'warning');
        return;
    }

    const result = await apiRequest('/menu', {
        method: 'POST',
        body: JSON.stringify({ name: dishName })
    });

    if (result.success) {
        dishInput.value = '';
        loadMenu();
        showNotification('菜品添加成功！');
    } else {
        showNotification('添加失败: ' + result.message, 'error');
    }
}

// 删除菜品
async function deleteDish(dishName) {
    if (!confirm(`确定要删除"${dishName}"吗？`)) {
        return;
    }

    const result = await apiRequest(`/menu/${encodeURIComponent(dishName)}`, {
        method: 'DELETE'
    });

    if (result.success) {
        loadMenu();
        showNotification('菜品删除成功！');
    } else {
        showNotification('删除失败: ' + result.message, 'error');
    }
}

// 打开编辑模态框
function openEditModal(dishName) {
    currentEditDish = dishName;
    document.getElementById('editDishName').value = dishName;
    document.getElementById('editModal').style.display = 'block';
}

// 更新菜品
async function updateDish() {
    const newName = document.getElementById('editDishName').value.trim();
    
    if (!newName) {
        showNotification('请输入菜品名称', 'warning');
        return;
    }

    // 由于我们使用DELETE和POST，这里需要先删除再添加
    const deleteResult = await apiRequest(`/menu/${encodeURIComponent(currentEditDish)}`, {
        method: 'DELETE'
    });

    if (deleteResult.success) {
        const addResult = await apiRequest('/menu', {
            method: 'POST',
            body: JSON.stringify({ name: newName })
        });

        if (addResult.success) {
            document.getElementById('editModal').style.display = 'none';
            loadMenu();
            showNotification('菜品更新成功！');
        } else {
            showNotification('更新失败: ' + addResult.message, 'error');
            // 恢复原菜品
            await apiRequest('/menu', {
                method: 'POST',
                body: JSON.stringify({ name: currentEditDish })
            });
        }
    } else {
        showNotification('更新失败: ' + deleteResult.message, 'error');
    }
}

// 随机点单
async function randomOrder() {
    const countInput = document.getElementById('dishCount');
    let count = parseInt(countInput.value);

    if (isNaN(count) || count < 1) {
        count = 1;
        countInput.value = 1;
    }

    const result = await apiRequest('/random', {
        method: 'POST',
        body: JSON.stringify({ count: count })
    });

    if (result.success) {
        displayResults(result.data);
    } else {
        showNotification('随机点单失败: ' + result.message, 'error');
    }
}

// 显示随机结果
function displayResults(selectedDishes) {
    const resultSection = document.getElementById('resultSection');
    const selectedDishesContainer = document.getElementById('selectedDishes');

    selectedDishesContainer.innerHTML = selectedDishes.map(dish => `
        <div class="selected-dish">${dish}</div>
    `).join('');

    resultSection.style.display = 'block';
    resultSection.scrollIntoView({ behavior: 'smooth' });
}

// 显示通知
function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    const backgroundColor = type === 'error' ? '#e74c3c' : 
                           type === 'warning' ? '#f39c12' : '#00b894';
    
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${backgroundColor};
        color: white;
        padding: 15px 20px;
        border-radius: 8px;
        z-index: 1001;
        animation: slideIn 0.3s ease;
        max-width: 300px;
    `;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// 添加CSS动画
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
`;
document.head.appendChild(style);
