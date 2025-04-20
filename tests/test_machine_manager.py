import pytest
from src.machine_manager import MachineManager

def test_get_machine_id():
    """测试获取机器码"""
    manager = MachineManager()
    machine_id = manager.get_machine_id()
    assert isinstance(machine_id, str)
    assert len(machine_id) > 0
    
def test_verify_machine_id():
    """测试验证机器码"""
    manager = MachineManager()
    machine_id = manager.get_machine_id()
    assert manager.verify_machine_id(machine_id) is True 