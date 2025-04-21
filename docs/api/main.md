# Main 模块 API 文档

## CursorAutoFree 类

### 类说明
`CursorAutoFree` 类是应用程序的主入口类，负责管理整个应用程序的生命周期和协调各个功能模块的工作。

### 属性

| 属性名 | 类型 | 说明 |
|--------|------|------|
| logger | Logger | 日志记录器实例 |
| config | Config | 配置管理器实例 |
| machine_manager | MachineManager | 机器码管理器实例 |
| email_manager | EmailManager | 邮箱管理器实例 |
| browser_manager | BrowserManager | 浏览器管理器实例 |

### 方法

#### `__init__()`
初始化 CursorAutoFree 实例。

**参数**: 无

**返回**: 无

**示例**:
```python
app = CursorAutoFree()
```

#### `close_cursor_processes()`
关闭所有运行的 Cursor 进程。

**参数**: 无

**返回**: 
- `bool`: 是否成功关闭所有进程

**示例**:
```python
if app.close_cursor_processes():
    print("成功关闭所有Cursor进程")
```

#### `reset_machine_id()`
重置当前机器的机器码。

**参数**: 无

**返回**: 
- `bool`: 是否成功重置机器码

**示例**:
```python
if app.reset_machine_id():
    print("成功重置机器码")
```

#### `register_cursor_account()`
执行 Cursor 账号注册流程。

**参数**: 无

**返回**: 
- `bool`: 是否成功注册账号

**流程**:
1. 启动浏览器
2. 访问 Cursor 网站
3. 点击注册按钮
4. 输入邮箱
5. 发送验证码
6. 获取验证码
7. 输入验证码
8. 完成注册

**示例**:
```python
if app.register_cursor_account():
    print("成功注册账号")
```

### 异常处理

所有方法都包含异常处理机制，错误信息会通过日志记录。主要异常类型包括：

- `ProcessError`: 进程操作相关错误
- `BrowserError`: 浏览器操作相关错误
- `NetworkError`: 网络操作相关错误
- `ConfigError`: 配置相关错误

### 使用示例

```python
from src.main import CursorAutoFree

def main():
    # 创建实例
    app = CursorAutoFree()
    
    try:
        # 关闭现有进程
        if not app.close_cursor_processes():
            print("关闭进程失败")
            return
            
        # 重置机器码
        if not app.reset_machine_id():
            print("重置机器码失败")
            return
            
        # 注册账号
        if not app.register_cursor_account():
            print("注册账号失败")
            return
            
        print("所有操作成功完成")
        
    except Exception as e:
        print(f"发生错误: {str(e)}")

if __name__ == "__main__":
    main()
```

### 注意事项

1. 运行程序前确保已正确配置环境变量
2. 某些操作可能需要管理员权限
3. 浏览器自动化操作可能需要较长时间
4. 确保网络连接稳定
5. 建议在虚拟环境中运行 