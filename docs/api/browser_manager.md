# 浏览器自动化模块 API 文档

## BrowserManager 类

### 初始化方法
```python
def __init__(self, config)
```
初始化浏览器管理器。

**参数：**
- `config` (Config): 配置对象

### 浏览器操作方法
```python
def start_browser(self)
```
启动浏览器。

**返回值：**
- `bool`: 启动是否成功

```python
def navigate(self, url)
```
导航到指定URL。

**参数：**
- `url` (str): 目标URL

**返回值：**
- `bool`: 导航是否成功

```python
def find_element(self, selector)
```
查找页面元素。

**参数：**
- `selector` (str): 元素选择器

**返回值：**
- `WebElement`: 页面元素对象

```python
def close_browser(self)
```
关闭浏览器。

**返回值：**
- `bool`: 关闭是否成功 