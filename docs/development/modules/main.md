# Main 模块

## 概述

Main 模块是 Cursor Auto Free 程序的入口点，负责初始化和管理整个应用程序的运行。该模块包含 `CursorAutoFree` 类，用于协调各个功能模块的工作。

## 功能说明

- 程序初始化和配置加载
- 协调各个管理器的工作
- 提供主要的自动化流程控制
- 实现保活功能

## 类定义

### CursorAutoFree

主程序类，负责管理整个应用程序的生命周期。

#### 属性

- `logger`: 日志记录器实例
- `config`: 配置管理器实例
- `machine_manager`: 机器码管理器实例
- `email_manager`: 邮箱管理器实例
- `browser_manager`: 浏览器管理器实例
- `keep_alive_interval`: 保活间隔时间（秒）

#### 方法

##### `__init__()`

初始化 CursorAutoFree 实例。

```python
def __init__(self):
    self.logger = logger
    self.config = Config()
    self.machine_manager = MachineManager()
    self.email_manager = EmailManager(self.config)
    self.browser_manager = BrowserManager(self.config)
    self.keep_alive_interval = 3600
```

##### `run() -> bool`

运行主程序流程。

```python
def run(self) -> bool:
    """
    执行主要的自动化流程：
    1. 获取机器码
    2. 启动浏览器
    3. 访问 Cursor 网站
    4. 执行注册流程
    5. 处理验证码
    6. 完成注册
    
    返回:
        bool: 是否成功完成流程
    """
```

##### `reset_machine_id() -> bool`

重置机器码。

```python
def reset_machine_id(self) -> bool:
    """
    重置当前机器的机器码
    
    返回:
        bool: 是否成功重置
    """
```

##### `patch_machine_id(patch: str) -> bool`

应用机器码补丁。

```python
def patch_machine_id(self, patch: str) -> bool:
    """
    应用指定的机器码补丁
    
    参数:
        patch (str): 补丁内容
        
    返回:
        bool: 是否成功应用补丁
    """
```

##### `verify_machine_id(machine_id: str) -> bool`

验证机器码。

```python
def verify_machine_id(self, machine_id: str) -> bool:
    """
    验证指定的机器码是否有效
    
    参数:
        machine_id (str): 要验证的机器码
        
    返回:
        bool: 机器码是否有效
    """
```

##### `keep_alive() -> bool`

执行保活操作。

```python
def keep_alive(self) -> bool:
    """
    执行保活操作：
    1. 获取会话令牌
    2. 更新认证信息
    3. 检查账号状态
    
    返回:
        bool: 保活是否成功
    """
```

##### `start_keep_alive()`

启动保活定时任务。

```python
def start_keep_alive(self):
    """
    启动保活定时任务，每 keep_alive_interval 秒执行一次保活操作
    """
```

## 使用示例

```python
from src.main import CursorAutoFree

# 创建实例
app = CursorAutoFree()

# 运行主程序
if app.run():
    print("程序运行成功")
else:
    print("程序运行失败")

# 启动保活
app.start_keep_alive()
```

## 注意事项

1. 运行程序前确保已正确配置环境变量
2. 保活功能需要定期执行以维持账号状态
3. 机器码相关操作需要管理员权限
4. 浏览器自动化操作可能需要较长时间

## 错误处理

- 所有方法都包含异常处理
- 错误信息会通过日志记录
- 关键操作失败会返回 False

## 依赖关系

- config.py
- logger.py
- machine_manager.py
- email_manager.py
- browser_manager.py 