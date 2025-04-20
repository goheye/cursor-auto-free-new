# 配置管理模块设计文档

## 1. 模块概述

配置管理模块（`config.py`）负责管理应用程序的配置信息，包括环境变量、配置文件、账号信息等。

## 2. 功能说明

### 2.1 核心功能
- 环境变量加载和管理
- 配置文件读写
- 账号信息管理
- 配置验证

### 2.2 主要类和方法

#### Config 类
```python
class Config:
    def __init__(self):
        """初始化配置管理器"""
        
    def load_env(self):
        """加载环境变量"""
        
    def save_accounts(self, accounts):
        """保存账号信息到配置文件"""
        
    def load_accounts(self):
        """从配置文件加载账号信息"""
        
    def validate_config(self):
        """验证配置的有效性"""
```

## 3. 接口定义

### 3.1 环境变量
- `DOMAIN`: 域名配置
- `TEMP_MAIL`: 临时邮箱配置
- `API_KEY`: API密钥

### 3.2 配置文件
- `accounts.json`: 账号信息存储
- `.env`: 环境变量配置

## 4. 使用示例

```python
from src.config import Config

# 初始化配置
config = Config()

# 加载环境变量
config.load_env()

# 保存账号信息
accounts = [
    {
        "id": "1",
        "email": "test@example.com",
        "status": "active"
    }
]
config.save_accounts(accounts)

# 加载账号信息
accounts = config.load_accounts()
```

## 5. 错误处理

- 环境变量缺失错误
- 配置文件读写错误
- 配置验证错误

## 6. 注意事项

1. 敏感信息必须通过环境变量配置
2. 配置文件需要定期备份
3. 配置变更需要记录日志 