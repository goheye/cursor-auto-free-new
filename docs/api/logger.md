# 日志管理模块 API 文档

## Logger 类

### 初始化方法
```python
def __init__(self, config)
```
初始化日志管理器。

**参数：**
- `config` (Config): 配置对象

### 日志记录方法
```python
def debug(self, message)
```
记录调试信息。

**参数：**
- `message` (str): 日志消息

**返回值：**
- `None`

```python
def info(self, message)
```
记录普通信息。

**参数：**
- `message` (str): 日志消息

**返回值：**
- `None`

```python
def warning(self, message)
```
记录警告信息。

**参数：**
- `message` (str): 日志消息

**返回值：**
- `None`

```python
def error(self, message)
```
记录错误信息。

**参数：**
- `message` (str): 日志消息

**返回值：**
- `None`

```python
def critical(self, message)
```
记录严重错误信息。

**参数：**
- `message` (str): 日志消息

**返回值：**
- `None` 