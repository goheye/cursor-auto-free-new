# BrowserManager 模块

## 概述

BrowserManager 模块负责处理浏览器自动化相关的操作，包括启动浏览器、控制浏览器操作等功能。

## 功能说明

- 启动和关闭浏览器
- 控制浏览器导航
- 处理页面元素
- 执行自动化操作

## 类定义

### BrowserManager

浏览器管理类，负责处理所有与浏览器自动化相关的操作。

#### 属性

- `config`: 配置管理器实例

#### 方法

##### `__init__(config)`

初始化浏览器管理器。

```python
def __init__(self, config):
    """
    初始化浏览器管理器
    
    参数:
        config: 配置管理器实例
    """
```

##### `start_browser() -> bool`

启动浏览器。

```python
def start_browser(self) -> bool:
    """
    启动浏览器
    
    返回:
        bool: 是否成功启动
    """
```

##### `close_browser() -> None`

关闭浏览器。

```python
def close_browser(self) -> None:
    """
    关闭浏览器
    """
```

##### `navigate_to(url: str) -> bool`

导航到指定 URL。

```python
def navigate_to(self, url: str) -> bool:
    """
    导航到指定 URL
    
    参数:
        url (str): 目标 URL
        
    返回:
        bool: 是否成功导航
    """
```

##### `wait_for_element(selector: str) -> bool`

等待元素出现。

```python
def wait_for_element(self, selector: str) -> bool:
    """
    等待指定元素出现
    
    参数:
        selector (str): 元素选择器
        
    返回:
        bool: 是否成功等待到元素
    """
```

##### `click_element(selector: str) -> bool`

点击元素。

```python
def click_element(self, selector: str) -> bool:
    """
    点击指定元素
    
    参数:
        selector (str): 元素选择器
        
    返回:
        bool: 是否成功点击
    """
```

##### `input_text(selector: str, text: str) -> bool`

输入文本。

```python
def input_text(self, selector: str, text: str) -> bool:
    """
    在指定元素输入文本
    
    参数:
        selector (str): 元素选择器
        text (str): 要输入的文本
        
    返回:
        bool: 是否成功输入
    """
```

## 使用示例

```python
from src.browser_manager import BrowserManager
from src.config import Config

# 创建配置管理器实例
config = Config()

# 创建浏览器管理器实例
browser_manager = BrowserManager(config)

# 启动浏览器
if browser_manager.start_browser():
    print("浏览器启动成功")
    
    # 导航到指定 URL
    if browser_manager.navigate_to("https://example.com"):
        print("导航成功")
        
        # 等待元素出现
        if browser_manager.wait_for_element("#element"):
            print("元素已出现")
            
            # 点击元素
            if browser_manager.click_element("#element"):
                print("点击成功")
                
            # 输入文本
            if browser_manager.input_text("#input", "text"):
                print("输入成功")
    
    # 关闭浏览器
    browser_manager.close_browser()
```

## 注意事项

1. 确保浏览器驱动正确安装
2. 页面加载可能需要等待
3. 元素操作需要注意时序
4. 注意浏览器版本兼容性

## 错误处理

- 所有方法都包含异常处理
- 错误信息会通过日志记录
- 关键操作失败会返回 False

## 依赖关系

- config.py
- 浏览器驱动
- 自动化测试框架 