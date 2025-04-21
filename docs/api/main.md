# 主程序模块 API 文档

## CursorAutoFree 类

### 初始化方法
```python
def __init__(self)
```
初始化主程序。

### 运行方法
```python
def run(self) -> bool
```
运行主程序。

**返回值：**
- `bool`: 程序运行是否成功

### 机器码管理方法
```python
def reset_machine_id(self) -> bool
```
重置机器码。

**返回值：**
- `bool`: 重置是否成功

```python
def patch_machine_id(self, patch: str) -> bool
```
应用机器码补丁。

**参数：**
- `patch` (str): 补丁内容

**返回值：**
- `bool`: 补丁应用是否成功

```python
def verify_machine_id(self, machine_id: str) -> bool
```
验证机器码。

**参数：**
- `machine_id` (str): 要验证的机器码

**返回值：**
- `bool`: 验证是否成功

### 保活功能
```python
def keep_alive(self) -> bool
```
执行保活操作。

**返回值：**
- `bool`: 保活是否成功

```python
def start_keep_alive(self) -> None
```
启动保活定时任务。

**返回值：**
- `None` 