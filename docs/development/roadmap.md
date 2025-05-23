# Cursor Auto Free 开发路线图

## 1. 项目概述

Cursor Auto Free 是一个 Cursor 编辑器的自动化工具，主要功能包括机器码管理、邮箱验证和自动化操作。

### 核心功能
- 机器码管理（获取、重置、补丁）
- 邮箱验证系统（临时邮箱、IMAP）
- 自动化操作（浏览器自动化、程序保活）
- 图形用户界面（GUI）
- 多账号管理
- 多平台支持（Windows/Mac）

### 项目结构
```
cursor-auto-free/
├── src/                    # 源代码目录
│   ├── main.py            # 程序入口文件
│   ├── config.py          # 配置文件管理
│   ├── machine_manager.py # 机器码管理模块
│   ├── email_manager.py   # 邮箱验证模块
│   ├── browser_manager.py # 浏览器自动化模块
│   └── account_manager.py # 账号管理模块
│
├── gui/                   # 图形界面相关文件
│   ├── main_window.py     # 主窗口实现
│   ├── account_widget.py  # 账号管理界面
│   └── status_widget.py   # 状态显示界面
│
├── tests/                 # 测试文件目录
│   ├── test_machine.py    # 机器码模块测试
│   ├── test_email.py      # 邮箱模块测试
│   └── test_browser.py    # 浏览器模块测试
│
├── docs/                  # 文档目录
│   ├── api/              # API 文档
│   ├── user_guide/       # 用户指南
│   └── development/      # 开发文档
│
├── assets/               # 资源文件目录
│   ├── icons/           # 图标资源
│   └── styles/          # 样式文件
│
├── build/               # 构建相关文件
│   ├── windows.spec    # Windows 打包配置
│   └── mac.spec        # Mac 打包配置
│
├── venv/               # Python 虚拟环境
├── requirements.txt    # 项目依赖
├── README.md          # 项目说明
└── .env               # 环境变量配置
```

### 目录说明

- `src/`: 包含所有核心功能模块的源代码
  - `main.py`: 程序入口点，负责初始化应用程序
  - `config.py`: 管理配置文件和环境变量
  - `machine_manager.py`: 处理机器码的获取和重置
  - `email_manager.py`: 管理邮箱验证相关功能
  - `browser_manager.py`: 控制浏览器自动化操作
  - `account_manager.py`: 处理多账号管理功能

- `gui/`: 图形用户界面相关代码
  - `main_window.py`: 主窗口的实现
  - `account_widget.py`: 账号管理界面的组件
  - `status_widget.py`: 状态显示界面的组件

- `tests/`: 包含所有单元测试和集成测试
  - 每个模块都有对应的测试文件
  - 使用 pytest 框架进行测试

- `docs/`: 项目文档
  - `api/`: API 接口文档
  - `user_guide/`: 用户使用指南
  - `development/`: 开发相关文档

- `assets/`: 静态资源文件
  - `icons/`: 程序使用的图标
  - `styles/`: GUI 样式文件

- `build/`: 构建和打包相关文件
  - 包含不同平台的打包配置文件
  - 用于生成可执行文件

- `venv/`: Python 虚拟环境
  - 隔离项目依赖
  - 确保环境一致性

- `requirements.txt`: 项目依赖列表
  - 记录所有必要的 Python 包
  - 包含版本信息

- `README.md`: 项目说明文档
  - 项目介绍
  - 安装说明
  - 使用指南

- `.env`: 环境变量配置文件
  - 存储敏感信息
  - 配置参数

## 2. 开发阶段

### 第一阶段：基础架构搭建

#### 1.1 项目初始化
```bash
# 创建项目目录
mkdir cursor-auto-free
cd cursor-auto-free

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
.\venv\Scripts\activate  # Windows

# 创建基础文件结构
mkdir src
mkdir tests
mkdir docs
mkdir gui
touch requirements.txt
touch README.md
```

#### 1.2 基础依赖
```bash
# 基础依赖
pip install python-dotenv
pip install requests
pip install colorama
pip install DrissionPage

# GUI 依赖
pip install PyQt6  # 或 tkinter
pip install qdarkstyle  # 深色主题支持

# 打包依赖
pip install pyinstaller
pip install auto-py-to-exe  # Windows 打包工具
```

#### 1.3 配置文件设计
创建 `config.py`：
```python
from dotenv import load_dotenv
import os
import json

class Config:
    def __init__(self):
        load_dotenv()
        self.domain = os.getenv('DOMAIN')
        self.temp_mail = os.getenv('TEMP_MAIL')
        # ... 其他配置项
        
    def save_accounts(self, accounts):
        """保存账号信息到配置文件"""
        with open('accounts.json', 'w') as f:
            json.dump(accounts, f)
            
    def load_accounts(self):
        """从配置文件加载账号信息"""
        try:
            with open('accounts.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
```

### 第二阶段：核心功能开发

#### 2.1 机器码管理模块
```python
# src/machine_manager.py
class MachineManager:
    def get_machine_id(self):
        # 获取机器码逻辑
        pass
    
    def reset_machine_id(self):
        # 重置机器码逻辑
        pass
```

#### 2.2 邮箱验证模块
```python
# src/email_manager.py
class EmailManager:
    def __init__(self, config):
        self.config = config
        
    def get_verification_code(self):
        # 获取验证码逻辑
        pass
```

#### 2.3 浏览器自动化模块
```python
# src/browser_manager.py
class BrowserManager:
    def __init__(self, config):
        self.config = config
        
    def automate_browser(self):
        # 浏览器自动化逻辑
        pass
```

#### 2.4 账号管理模块
```python
# src/account_manager.py
class AccountManager:
    def __init__(self, config):
        self.config = config
        self.accounts = self.config.load_accounts()
        
    def add_account(self, account_info):
        # 添加新账号
        pass
        
    def remove_account(self, account_id):
        # 删除账号
        pass
        
    def get_account_info(self, account_id):
        # 获取账号信息
        pass
        
    def update_account(self, account_id, new_info):
        # 更新账号信息
        pass
```

### 第三阶段：GUI 开发

#### 3.1 主界面设计
```python
# gui/main_window.py
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cursor Auto Free")
        self.setMinimumSize(800, 600)
        
        # 创建主窗口部件
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # 创建布局
        layout = QVBoxLayout()
        main_widget.setLayout(layout)
        
        # 添加账号管理区域
        self.account_widget = AccountWidget()
        layout.addWidget(self.account_widget)
        
        # 添加状态显示区域
        self.status_widget = StatusWidget()
        layout.addWidget(self.status_widget)
```

#### 3.2 账号管理界面
```python
# gui/account_widget.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget

class AccountWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # 创建账号表格
        self.account_table = QTableWidget()
        self.account_table.setColumnCount(4)
        self.account_table.setHorizontalHeaderLabels([
            "账号ID", "邮箱", "状态", "操作"
        ])
        layout.addWidget(self.account_table)
```

#### 3.3 状态显示界面
```python
# gui/status_widget.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

class StatusWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # 创建状态标签
        self.quota_label = QLabel("剩余额度: 0")
        self.status_label = QLabel("状态: 空闲")
        layout.addWidget(self.quota_label)
        layout.addWidget(self.status_label)
```

### 第四阶段：多平台打包

#### 4.1 Windows 打包配置
```python
# build/windows.spec
a = Analysis(
    ['src/main.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('gui/*.ui', 'gui'),
        ('assets/*', 'assets')
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
```

#### 4.2 Mac 打包配置
```python
# build/mac.spec
a = Analysis(
    ['src/main.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('gui/*.ui', 'gui'),
        ('assets/*', 'assets')
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    cipher=block_cipher,
    noarchive=False,
)
```

#### 4.3 打包脚本
```bash
# build/build.sh
#!/bin/bash

# 清理旧的构建文件
rm -rf build dist

# 构建 Windows 版本
pyinstaller build/windows.spec

# 构建 Mac 版本
pyinstaller build/mac.spec

# 创建发布包
mkdir -p release
cp -r dist/windows/* release/windows/
cp -r dist/mac/* release/mac/
```

## 3. 开发建议

### 3.1 模块化设计
- 每个功能模块独立开发
- 使用接口定义模块间的通信
- 便于后续维护和扩展

### 3.2 错误处理
- 完善的异常处理机制
- 详细的日志记录
- 友好的错误提示

### 3.3 配置管理
- 使用环境变量管理敏感信息
- 支持多种配置方式
- 配置验证机制

### 3.4 测试驱动
- 为每个模块编写单元测试
- 使用 pytest 进行测试
- 确保代码质量

## 4. 优化方向

### 4.1 性能优化
- 异步处理邮箱验证
- 浏览器自动化优化
- 资源使用优化

### 4.2 功能扩展
- 支持更多邮箱服务
- 添加图形界面
- 增加更多自动化功能

### 4.3 安全性提升
- 加密敏感信息
- 增加身份验证
- 防止滥用机制

### 4.4 用户体验
- 详细的日志输出
- 进度显示
- 错误提示优化
- 深色/浅色主题切换
- 多语言支持

## 5. 开发工具推荐

### 5.1 代码编辑器
- VS Code
- PyCharm

### 5.2 版本控制
- Git
- GitHub/GitLab

### 5.3 测试工具
- pytest
- unittest

### 5.4 文档工具
- Sphinx
- MkDocs

### 5.5 GUI 设计工具
- Qt Designer
- PyQt6-tools

## 6. 开发注意事项

### 6.1 代码规范
- 遵循 PEP 8
- 使用类型注解
- 编写文档字符串

### 6.2 依赖管理
- 使用 requirements.txt
- 指定依赖版本
- 定期更新依赖

### 6.3 安全性
- 不硬编码敏感信息
- 使用环境变量
- 定期安全审计

### 6.4 可维护性
- 模块化设计
- 清晰的代码结构
- 完善的注释

### 6.5 跨平台兼容性
- 使用跨平台库
- 处理路径分隔符
- 测试不同平台

## 7. 开发步骤

### 7.1 模块化开发流程

每个模块的开发遵循以下流程：

1. 模块设计
   - 编写模块设计文档（`docs/development/modules/[模块名].md`）
   - 定义接口和功能点
   - 确定测试用例

2. 代码实现
   - 创建模块文件（`src/[模块名].py`）
   - 实现核心功能
   - 添加必要的注释和文档字符串

3. 单元测试
   - 编写测试文件（`tests/test_[模块名].py`）
   - 实现测试用例
   - 运行测试并修复问题

4. 文档更新
   - 更新模块文档
   - 添加使用示例
   - 记录已知问题和解决方案

5. 代码审查
   - 检查代码规范
   - 验证测试覆盖率
   - 确认文档完整性

### 7.2 模块开发顺序

1. 配置管理模块（`config.py`）
   - 实现配置加载和保存
   - 添加环境变量支持
   - 编写配置验证逻辑

2. 机器码管理模块（`machine_manager.py`）
   - 实现机器码获取
   - 添加重置功能
   - 开发补丁机制

3. 邮箱验证模块（`email_manager.py`）
   - 实现临时邮箱功能
   - 添加 IMAP 支持
   - 开发验证码处理

4. 浏览器自动化模块（`browser_manager.py`）
   - 实现浏览器控制
   - 添加自动化操作
   - 开发错误处理

5. 账号管理模块（`account_manager.py`）
   - 实现账号存储
   - 添加账号操作
   - 开发状态管理

6. GUI 模块
   - 实现主窗口
   - 开发账号管理界面
   - 添加状态显示

### 7.3 文档维护

每个模块都需要维护以下文档：

1. 设计文档（`docs/development/modules/[模块名].md`）
   - 模块概述
   - 功能说明
   - 接口定义
   - 使用示例

2. API 文档（`docs/api/[模块名].md`）
   - 类和方法说明
   - 参数说明
   - 返回值说明
   - 异常说明

3. 测试文档（`docs/tests/[模块名].md`）
   - 测试用例说明
   - 测试结果
   - 覆盖率报告 