# 邮箱验证模块设计文档

## 1. 模块概述

邮箱验证模块（`email_manager.py`）负责处理邮箱验证相关操作，包括临时邮箱创建、邮件接收和验证码提取。

## 2. 功能说明

### 2.1 核心功能
- 临时邮箱创建和管理
- IMAP邮件接收
- 验证码提取
- 邮箱状态监控

### 2.2 主要类和方法

#### EmailManager 类
```python
class EmailManager:
    def __init__(self, config):
        """初始化邮箱管理器"""
        
    def create_temp_mail(self):
        """创建临时邮箱"""
        
    def check_mail(self, email):
        """检查邮件"""
        
    def extract_verification_code(self, email_content):
        """提取验证码"""
        
    def monitor_mailbox(self, email, callback):
        """监控邮箱状态"""
```

## 3. 接口定义

### 3.1 临时邮箱服务
- 支持多个临时邮箱服务商
- 自动选择可用服务
- 邮箱生命周期管理

### 3.2 邮件格式
```json
{
    "from": "sender@example.com",
    "subject": "Verification Code",
    "content": "Your code is: 123456",
    "received_at": "2024-03-20T10:00:00Z"
}
```

## 4. 使用示例

```python
from src.email_manager import EmailManager
from src.config import Config

# 初始化配置和邮箱管理器
config = Config()
email_manager = EmailManager(config)

# 创建临时邮箱
temp_email = email_manager.create_temp_mail()

# 检查邮件
emails = email_manager.check_mail(temp_email)

# 提取验证码
for email in emails:
    code = email_manager.extract_verification_code(email['content'])
    if code:
        print(f"验证码: {code}")
        break

# 监控邮箱
def on_new_mail(email):
    print(f"收到新邮件: {email['subject']}")
    
email_manager.monitor_mailbox(temp_email, on_new_mail)
```

## 5. 错误处理

- 临时邮箱创建失败
- 邮件接收超时
- 验证码提取失败
- 监控连接中断

## 6. 注意事项

1. 临时邮箱需要定期清理
2. 需要处理网络延迟和超时
3. 验证码提取需要考虑多种格式
4. 监控功能需要异常恢复机制 