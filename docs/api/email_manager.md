# 邮箱验证模块 API 文档

## EmailManager 类

### 初始化方法
```python
def __init__(self, config)
```
初始化邮箱管理器。

**参数：**
- `config` (Config): 配置对象

### 邮箱操作方法
```python
def create_temp_mail(self)
```
创建临时邮箱。

**返回值：**
- `str`: 临时邮箱地址

```python
def check_mail(self)
```
检查邮件。

**返回值：**
- `list`: 邮件列表

```python
def get_verification_code(self)
```
获取验证码。

**返回值：**
- `str`: 验证码字符串

```python
def close_mailbox(self)
```
关闭邮箱。

**返回值：**
- `bool`: 关闭是否成功 