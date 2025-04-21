# 账号管理模块 API 文档

## AccountManager 类

### 初始化方法
```python
def __init__(self, config)
```
初始化账号管理器。

**参数：**
- `config` (Config): 配置对象

### 账号操作方法
```python
def add_account(self, account_info)
```
添加新账号。

**参数：**
- `account_info` (dict): 账号信息

**返回值：**
- `bool`: 添加是否成功

```python
def remove_account(self, account_id)
```
删除账号。

**参数：**
- `account_id` (str): 账号ID

**返回值：**
- `bool`: 删除是否成功

```python
def update_account(self, account_id, new_info)
```
更新账号信息。

**参数：**
- `account_id` (str): 账号ID
- `new_info` (dict): 新的账号信息

**返回值：**
- `bool`: 更新是否成功

```python
def get_account_info(self, account_id)
```
获取账号信息。

**参数：**
- `account_id` (str): 账号ID

**返回值：**
- `dict`: 账号信息 