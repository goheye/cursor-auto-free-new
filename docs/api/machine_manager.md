# 机器码管理模块 API 文档

## MachineManager 类

### 初始化方法
```python
def __init__(self)
```
初始化机器码管理器。

### 机器码操作方法
```python
def get_machine_id(self)
```
获取机器码。

**返回值：**
- `str`: 机器码字符串

```python
def reset_machine_id(self)
```
重置机器码。

**返回值：**
- `bool`: 重置是否成功

### 补丁操作方法
```python
def apply_patch(self, patch_data)
```
应用补丁。

**参数：**
- `patch_data` (dict): 补丁数据

**返回值：**
- `bool`: 补丁应用是否成功

```python
def rollback_patch(self)
```
回滚补丁。

**返回值：**
- `bool`: 回滚是否成功 