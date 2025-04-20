# 邮箱验证功能使用指南

## 1. 功能简介

邮箱验证功能用于自动获取 Cursor 验证码，支持多种邮箱类型和协议。该功能可以自动连接邮箱服务器，获取验证码，并处理各种异常情况。

## 2. 支持的邮箱类型

### 2.1 普通邮箱
- 支持 IMAP 协议
- 支持 POP3 协议
- 支持 SSL/TLS 加密

### 2.2 临时邮箱
- 支持临时邮箱服务
- 自动清理已读邮件
- 支持自定义邮箱域名

### 2.3 特殊邮箱
- 支持网易邮箱（163.com、126.com、yeah.net）
- 自动处理特殊邮箱要求
- 优化邮件获取策略

## 3. 配置说明

### 3.1 基本配置
在 `.env` 文件中配置邮箱信息：

```ini
# IMAP 配置
IMAP_SERVER=imap.example.com
IMAP_PORT=993
IMAP_USER=user@example.com
IMAP_PASSWORD=password
IMAP_DIRECTORY=INBOX

# POP3 配置
POP3_SERVER=pop3.example.com
POP3_PORT=995
POP3_USER=user@example.com
POP3_PASSWORD=password

# 临时邮箱配置
TEMP_MAIL=username
TEMP_MAIL_EPIN=epin
TEMP_MAIL_EXT=@example.com

# 协议选择
PROTOCOL=IMAP  # 可选：IMAP, POP3
```

### 3.2 高级配置
在 `config.py` 中配置高级选项：

```python
# 重试配置
MAX_RETRIES = 5
RETRY_INTERVAL = 60

# 超时配置
CONNECTION_TIMEOUT = 30
READ_TIMEOUT = 180

# 日志配置
LOG_LEVEL = "INFO"
LOG_FILE = "email.log"
```

## 4. 使用说明

### 4.1 基本使用
```python
from src.email_manager import EmailManager
from config import Config

# 初始化
config = Config()
email_manager = EmailManager(config)

# 获取验证码
code = email_manager.get_verification_code()
if code:
    print(f"验证码: {code}")
else:
    print("获取验证码失败")
```

### 4.2 自定义配置
```python
# 自定义超时和重试次数
code = email_manager.get_verification_code(
    timeout=300,  # 5分钟超时
    max_retries=10  # 最多重试10次
)
```

### 4.3 错误处理
```python
try:
    code = email_manager.get_verification_code()
except Exception as e:
    print(f"错误: {str(e)}")
    # 处理错误
```

## 5. 常见问题

### 5.1 连接失败
- 检查网络连接
- 验证服务器地址和端口
- 确认账号密码正确
- 检查防火墙设置

### 5.2 验证码获取失败
- 检查邮箱是否有新邮件
- 确认邮件未被其他程序读取
- 验证邮件过滤规则
- 检查垃圾邮件箱

### 5.3 特殊邮箱问题
- 网易邮箱需要特殊配置
- 可能需要开启 IMAP/POP3 服务
- 可能需要设置应用专用密码

## 6. 最佳实践

### 6.1 安全建议
- 使用强密码
- 定期更换密码
- 使用 SSL/TLS 加密
- 保护配置文件安全

### 6.2 性能优化
- 合理设置超时时间
- 适当配置重试次数
- 定期清理旧邮件
- 使用连接池

### 6.3 维护建议
- 定期检查日志
- 更新邮箱配置
- 测试连接状态
- 备份重要数据

## 7. 故障排除

### 7.1 日志查看
```bash
# 查看错误日志
tail -f email.log
```

### 7.2 连接测试
```python
# 测试连接
email_manager.connect()
```

### 7.3 配置验证
```python
# 验证配置
config.validate()
```

## 8. 更新日志

### v1.0.0 (2024-04-20)
- 初始版本发布
- 支持多种邮箱协议
- 添加自动重试机制
- 完善错误处理
- 添加日志记录 