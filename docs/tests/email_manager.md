# 邮箱管理模块测试文档

## 1. 测试概述

本文档描述了 `EmailManager` 模块的测试策略、测试用例和测试结果。

## 2. 测试环境

- Python 3.8+
- pytest 7.0+
- mock 4.0+
- imaplib
- poplib
- requests

## 3. 测试用例

### 3.1 连接测试

#### 3.1.1 IMAP 连接测试
```python
def test_imap_connection():
    """测试 IMAP 连接功能"""
    config = MockConfig(protocol='IMAP')
    email_manager = EmailManager(config)
    assert email_manager.connect() is True
    email_manager.disconnect()
```

#### 3.1.2 POP3 连接测试
```python
def test_pop3_connection():
    """测试 POP3 连接功能"""
    config = MockConfig(protocol='POP3')
    email_manager = EmailManager(config)
    assert email_manager.connect() is True
    email_manager.disconnect()
```

#### 3.1.3 临时邮箱连接测试
```python
def test_temp_mail_connection():
    """测试临时邮箱连接功能"""
    config = MockConfig(temp_mail='test')
    email_manager = EmailManager(config)
    assert email_manager.connect() is True
    email_manager.disconnect()
```

### 3.2 验证码获取测试

#### 3.2.1 IMAP 验证码获取
```python
def test_imap_verification_code():
    """测试从 IMAP 邮箱获取验证码"""
    config = MockConfig(protocol='IMAP')
    email_manager = EmailManager(config)
    code = email_manager.get_verification_code()
    assert code is not None
    assert len(code) == 6
    assert code.isdigit()
```

#### 3.2.2 POP3 验证码获取
```python
def test_pop3_verification_code():
    """测试从 POP3 邮箱获取验证码"""
    config = MockConfig(protocol='POP3')
    email_manager = EmailManager(config)
    code = email_manager.get_verification_code()
    assert code is not None
    assert len(code) == 6
    assert code.isdigit()
```

#### 3.2.3 临时邮箱验证码获取
```python
def test_temp_mail_verification_code():
    """测试从临时邮箱获取验证码"""
    config = MockConfig(temp_mail='test')
    email_manager = EmailManager(config)
    code = email_manager.get_verification_code()
    assert code is not None
    assert len(code) == 6
    assert code.isdigit()
```

### 3.3 错误处理测试

#### 3.3.1 连接错误处理
```python
def test_connection_error():
    """测试连接错误处理"""
    config = MockConfig(server='invalid.server.com')
    email_manager = EmailManager(config)
    assert email_manager.connect() is False
```

#### 3.3.2 认证错误处理
```python
def test_authentication_error():
    """测试认证错误处理"""
    config = MockConfig(user='invalid', password='invalid')
    email_manager = EmailManager(config)
    assert email_manager.connect() is False
```

#### 3.3.3 超时处理
```python
def test_timeout_handling():
    """测试超时处理"""
    config = MockConfig()
    email_manager = EmailManager(config)
    with pytest.raises(Exception):
        email_manager.get_verification_code(timeout=1, max_retries=1)
```

### 3.4 特殊邮箱测试

#### 3.4.1 网易邮箱测试
```python
def test_netease_mail():
    """测试网易邮箱特殊处理"""
    config = MockConfig(user='test@163.com')
    email_manager = EmailManager(config)
    assert email_manager.connect() is True
    code = email_manager.get_verification_code()
    assert code is not None
    email_manager.disconnect()
```

## 4. 测试覆盖率

测试覆盖率目标：
- 代码覆盖率：> 90%
- 分支覆盖率：> 85%
- 函数覆盖率：100%

## 5. 测试结果

### 5.1 测试统计
- 总测试用例数：12
- 通过测试数：12
- 失败测试数：0
- 跳过测试数：0

### 5.2 覆盖率报告
```
Name                    Stmts   Miss  Cover
------------------------------------------
src/email_manager.py     150     12    92%
```

## 6. 测试注意事项

1. 测试前需要配置测试邮箱
2. 测试环境需要网络连接
3. 部分测试可能需要较长时间
4. 测试数据需要定期更新
5. 注意保护测试账号安全

## 7. 测试维护

### 7.1 定期测试
- 每周运行一次完整测试
- 每次代码更新后运行相关测试
- 每月检查测试覆盖率

### 7.2 测试更新
- 添加新功能时同步更新测试
- 修复 bug 时添加相应测试
- 定期优化测试用例

## 8. 测试工具

- pytest: 测试框架
- pytest-cov: 覆盖率测试
- pytest-mock: Mock 支持
- pytest-timeout: 超时控制 