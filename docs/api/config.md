# 配置管理模块 API 文档

## Config 类

### 初始化方法
```python
def __init__(self)
```
初始化配置管理器。

### 环境变量方法
```python
def load_env(self)
```
加载环境变量。

**返回值：**
- `None`

### 账号管理方法
```python
def save_accounts(self, accounts)
```
保存账号信息。

**参数：**
- `accounts` (list): 账号信息列表

**返回值：**
- `None`

```python
def load_accounts(self)
```
加载账号信息。

**返回值：**
- `list`: 账号信息列表

### 配置验证方法
```python
def validate_config(self)
```
验证配置有效性。

**返回值：**
- `bool`: 配置是否有效 