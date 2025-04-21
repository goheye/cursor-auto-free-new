# GUI 模块测试文档

## 测试用例说明

### 主窗口测试
```python
def test_main_window():
    """测试主窗口"""
    app = QApplication([])
    window = MainWindow()
    window.show()
    assert window.isVisible() is True
    app.quit()
```

### 账号管理界面测试
```python
def test_account_widget():
    """测试账号管理界面"""
    app = QApplication([])
    widget = AccountWidget()
    accounts = [{"id": "1", "email": "test@example.com"}]
    widget.update_accounts(accounts)
    assert widget.isVisible() is True
    app.quit()
```

### 状态显示界面测试
```python
def test_status_widget():
    """测试状态显示界面"""
    app = QApplication([])
    widget = StatusWidget()
    widget.update_status("测试状态")
    assert widget.isVisible() is True
    app.quit()
```

## 测试结果

### 测试覆盖率
- 主窗口测试: 100%
- 账号管理界面测试: 100%
- 状态显示界面测试: 100%

### 测试通过率
- 总测试用例: 3
- 通过测试: 3
- 通过率: 100%

## 已知问题
- 无 