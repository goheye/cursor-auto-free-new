import pytest
from src.main import CursorAutoFree

@pytest.fixture
def app():
    return CursorAutoFree()

def test_app_initialization(app):
    """测试应用程序初始化"""
    assert app is not None
    assert app.config is not None
    assert app.logger is not None
    assert app.machine_manager is not None
    assert app.email_manager is not None
    assert app.browser_manager is not None
    
def test_run(app):
    """测试运行主程序"""
    # 注意：这个测试需要实际的网络连接和邮箱服务器支持
    # 在实际测试中，应该使用测试环境和模拟数据
    result = app.run()
    assert isinstance(result, bool)
    
def test_reset_machine_id(app):
    """测试重置机器码"""
    result = app.reset_machine_id()
    assert isinstance(result, bool)
    
def test_patch_machine_id(app):
    """测试应用机器码补丁"""
    test_patch = "test_patch_123"
    result = app.patch_machine_id(test_patch)
    assert isinstance(result, bool)
    
def test_verify_machine_id(app):
    """测试验证机器码"""
    machine_id = app.machine_manager.get_machine_id()
    result = app.verify_machine_id(machine_id)
    assert isinstance(result, bool)
    assert result is True 