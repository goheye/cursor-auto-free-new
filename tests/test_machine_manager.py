import pytest
from unittest.mock import patch, MagicMock
from src.machine_manager import MachineManager

@pytest.fixture
def machine_manager():
    """创建 MachineManager 实例的 fixture"""
    return MachineManager()

def test_get_machine_id(machine_manager):
    """测试获取机器码"""
    # 测试首次获取机器码
    machine_id = machine_manager.get_machine_id()
    assert isinstance(machine_id, str)
    assert len(machine_id) > 0
    assert "Windows" in machine_id
    
    # 测试缓存机制
    cached_id = machine_manager.get_machine_id()
    assert cached_id == machine_id

def test_get_machine_id_with_wmi(machine_manager):
    """测试使用 WMI 获取机器码"""
    with patch('wmi.WMI') as mock_wmi:
        mock_instance = MagicMock()
        mock_instance.UUID = "test-uuid"
        mock_wmi.return_value.Win32_ComputerSystemProduct.return_value = [mock_instance]
        
        machine_id = machine_manager.get_machine_id()
        assert "Windows" in machine_id
        assert "test-uuid" in machine_id

def test_reset_machine_id(machine_manager):
    """测试重置机器码"""
    # 获取原始机器码
    original_id = machine_manager.get_machine_id()
    
    # 测试重置功能
    assert machine_manager.reset_machine_id() is True
    
    # 获取新的机器码
    new_id = machine_manager.get_machine_id()
    assert isinstance(new_id, str)
    assert len(new_id) > 0
    assert "Windows" in new_id

def test_patch_machine_id(machine_manager):
    """测试应用机器码补丁"""
    # 获取原始机器码
    original_id = machine_manager.get_machine_id()
    
    # 应用补丁
    patch_str = "test-patch"
    assert machine_manager.patch_machine_id(patch_str) is True
    
    # 验证补丁是否成功应用
    patched_id = machine_manager._machine_id
    assert patch_str in patched_id
    assert original_id in patched_id
    assert "Windows" in patched_id

def test_verify_machine_id(machine_manager):
    """测试验证机器码"""
    # 获取有效的机器码
    valid_id = machine_manager.get_machine_id()
    assert machine_manager.verify_machine_id(valid_id) is True
    
    # 测试无效的机器码
    invalid_id = "invalid-machine-id"
    assert machine_manager.verify_machine_id(invalid_id) is False

def test_error_handling(machine_manager):
    """测试错误处理"""
    # 测试 WMI 异常
    with patch('wmi.WMI', side_effect=Exception("WMI 错误")):
        with pytest.raises(Exception):
            machine_manager.get_machine_id()
    
    # 测试重置机器码时的异常
    with patch.object(machine_manager, 'get_machine_id', side_effect=Exception("测试异常")):
        assert machine_manager.reset_machine_id() is False
    
    # 测试应用补丁时的异常
    with patch.object(machine_manager, 'get_machine_id', side_effect=Exception("测试异常")):
        assert machine_manager.patch_machine_id("test-patch") is False 