# GUI 模块 API 文档

## MainWindow 类

### 初始化方法
```python
def __init__(self)
```
初始化主窗口。

### 界面操作方法
```python
def init_ui(self)
```
初始化界面。

**返回值：**
- `None`

```python
def update_status(self, status)
```
更新状态。

**参数：**
- `status` (str): 状态信息

**返回值：**
- `None`

## AccountWidget 类

### 初始化方法
```python
def __init__(self)
```
初始化账号管理界面。

### 界面操作方法
```python
def update_accounts(self, accounts)
```
更新账号列表。

**参数：**
- `accounts` (list): 账号列表

**返回值：**
- `None`

```python
def handle_account_event(self, event)
```
处理账号事件。

**参数：**
- `event` (QEvent): 事件对象

**返回值：**
- `None`

## StatusWidget 类

### 初始化方法
```python
def __init__(self)
```
初始化状态显示界面。

### 界面操作方法
```python
def update_status(self, status)
```
更新状态显示。

**参数：**
- `status` (str): 状态信息

**返回值：**
- `None` 