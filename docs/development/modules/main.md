# 主程序入口模块设计文档

## 1. 模块概述

主程序入口模块负责应用程序的初始化和运行，包括配置加载、模块初始化、机器码管理、浏览器自动化和保活功能等。

## 2. 功能说明

### 2.1 程序初始化
- 加载配置文件
- 初始化日志系统
- 初始化机器码管理器
- 初始化邮箱管理器
- 初始化浏览器管理器

### 2.2 程序流程控制
- 控制程序执行流程
- 处理程序异常
- 管理程序生命周期

### 2.3 机器码管理
- 获取机器码
- 重置机器码
- 应用机器码补丁
- 验证机器码

### 2.4 浏览器自动化
- 启动浏览器
- 控制浏览器操作
- 处理浏览器异常
- 关闭浏览器

### 2.5 保活功能
- 执行保活操作
- 启动保活定时任务
- 管理保活状态

## 3. 接口定义

### 3.1 CursorAutoFree 类
```python
class CursorAutoFree:
    def __init__(self):
        """初始化主程序"""
        pass
        
    def run(self) -> bool:
        """运行程序"""
        pass
        
    def reset_machine_id(self) -> bool:
        """重置机器码"""
        pass
        
    def patch_machine_id(self, patch: str) -> bool:
        """应用机器码补丁"""
        pass
        
    def verify_machine_id(self, machine_id: str) -> bool:
        """验证机器码"""
        pass
        
    def keep_alive(self) -> bool:
        """执行保活操作"""
        pass
        
    def start_keep_alive(self) -> None:
        """启动保活定时任务"""
        pass
```

## 4. 使用示例

```python
from main import CursorAutoFree

# 创建主程序实例
app = CursorAutoFree()

try:
    # 运行程序
    if app.run():
        print("程序运行成功")
    else:
        print("程序运行失败")
        
    # 重置机器码
    if app.reset_machine_id():
        print("机器码重置成功")
        
    # 应用补丁
    if app.patch_machine_id("patch_content"):
        print("补丁应用成功")
        
    # 启动保活
    app.start_keep_alive()
    
except Exception as e:
    print(f"程序执行出错: {str(e)}")
```

## 5. 注意事项

- 确保资源正确初始化
- 提供完整的错误处理
- 保证资源正确释放
- 注意浏览器自动化操作的稳定性
- 合理设置保活间隔
- 注意机器码管理的安全性 