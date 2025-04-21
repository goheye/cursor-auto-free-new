# 邮箱验证模块设计文档

## 1. 模块概述

邮箱验证模块负责处理所有与邮箱相关的操作，包括临时邮箱管理、IMAP 邮件接收和验证码处理等功能。

## 2. 功能说明

### 2.1 临时邮箱管理
- 创建临时邮箱
- 管理邮箱生命周期
- 提供邮箱状态监控

### 2.2 IMAP 邮件接收
- 连接 IMAP 服务器
- 接收和解析邮件
- 提取验证码信息

### 2.3 验证码处理
- 识别验证码
- 验证码格式转换
- 验证码有效性检查

## 3. 接口定义

### 3.1 EmailManager 类
```python
class EmailManager:
    def __init__(self, config):
        """初始化邮箱管理器"""
        pass
        
    def create_temp_mail(self):
        """创建临时邮箱"""
        pass
        
    def check_mail(self):
        """检查邮件"""
        pass
        
    def get_verification_code(self):
        """获取验证码"""
        pass
        
    def close_mailbox(self):
        """关闭邮箱"""
        pass
```

## 4. 使用示例

```python
from email_manager import EmailManager
from config import Config

# 初始化配置
config = Config()

# 初始化邮箱管理器
email_manager = EmailManager(config)

# 创建临时邮箱
email = email_manager.create_temp_mail()

# 检查邮件
emails = email_manager.check_mail()

# 获取验证码
verification_code = email_manager.get_verification_code()

# 关闭邮箱
email_manager.close_mailbox()
```

## 5. 注意事项

- 临时邮箱需要定期清理
- IMAP 连接需要处理超时和重连
- 验证码识别需要考虑多种格式
- 提供完整的错误处理机制

## 6. 功能特性

- 支持多种邮箱协议（IMAP、POP3）
- 支持临时邮箱服务
- 自动重试机制
- 完善的错误处理
- 详细的日志记录
- 支持特殊邮箱（如网易邮箱）的处理

## 7. 类定义

### EmailManager

邮箱管理类，负责处理所有与邮箱验证相关的操作。

#### 属性

- `config`: 配置管理器实例

#### 方法

##### `__init__(config)`

初始化邮箱管理器。

```python
def __init__(self, config):
    """
    初始化邮箱管理器
    
    参数:
        config: 配置管理器实例
    """
```

##### `get_verification_code() -> str`

获取验证码。

```python
def get_verification_code(self) -> str:
    """
    获取验证码
    
    返回:
        str: 验证码字符串，如果获取失败则返回空字符串
    """
```

## 8. 方法说明

### 8.1 初始化方法

```python
def __init__(self, config: Any)
```

**参数**:
- `config`: 配置对象，包含邮箱连接所需的配置信息

**说明**:
初始化邮箱管理器，设置必要的属性和配置。

### 8.2 连接方法

```python
def connect(self) -> bool
```

**返回值**:
- `bool`: 连接是否成功

**说明**:
根据配置连接到邮箱服务器，支持 IMAP、POP3 和临时邮箱模式。

### 8.3 断开连接方法

```python
def disconnect(self) -> None
```

**说明**:
安全地断开与邮箱服务器的连接。

### 8.4 获取验证码方法

```python
def get_verification_code(self, timeout: int = 180, max_retries: int = 5) -> Optional[str]
```

**参数**:
- `timeout`: 超时时间（秒），默认 180 秒
- `max_retries`: 最大重试次数，默认 5 次

**返回值**:
- `Optional[str]`: 验证码字符串，如果获取失败则返回 None

**说明**:
尝试获取验证码，支持自动重试机制。

## 9. 配置要求

### 9.1 IMAP 配置
```json
{
    "server": "imap.example.com",
    "port": 993,
    "user": "user@example.com",
    "password": "password",
    "directory": "INBOX"
}
```

### 9.2 POP3 配置
```json
{
    "server": "pop3.example.com",
    "port": 995,
    "user": "user@example.com",
    "password": "password"
}
```

### 9.3 临时邮箱配置
```json
{
    "temp_mail": "username",
    "temp_mail_epin": "epin",
    "temp_mail_ext": "@example.com"
}
```

## 10. 使用示例

### 10.1 基本使用
```python
from src.email_manager import EmailManager
from config import Config

# 初始化配置
config = Config()

# 创建邮箱管理器
email_manager = EmailManager(config)

# 获取验证码
code = email_manager.get_verification_code()
if code:
    print(f"获取到验证码: {code}")
else:
    print("获取验证码失败")
```

### 10.2 自定义重试次数
```python
# 设置更长的超时时间和更多的重试次数
code = email_manager.get_verification_code(timeout=300, max_retries=10)
```

## 11. 错误处理

模块会处理以下类型的错误：
- 连接错误
- 认证错误
- 网络错误
- 解析错误
- 超时错误

所有错误都会记录到日志中，并提供友好的错误信息。

## 12. 注意事项

1. 使用网易邮箱时，需要特殊处理
2. 临时邮箱服务可能需要额外的 API 密钥
3. 建议使用 SSL/TLS 连接
4. 定期检查邮箱连接状态
5. 注意处理敏感信息

## 13. 更新日志

### v1.0.0 (2024-04-20)
- 初始版本发布
- 支持 IMAP 和 POP3 协议
- 支持临时邮箱服务
- 添加自动重试机制
- 完善错误处理
- 添加日志记录 