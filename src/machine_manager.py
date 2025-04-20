import os
import sys
import uuid
import platform
from typing import Optional
from src.logger import logger

class MachineManager:
    def __init__(self):
        self.logger = logger
        self._machine_id = None
        
    def get_machine_id(self) -> str:
        """获取机器码"""
        try:
            if self._machine_id:
                return self._machine_id
                
            # 获取系统信息
            system = platform.system()
            machine = platform.machine()
            processor = platform.processor()
            
            # 生成唯一标识符
            if system == "Windows":
                # Windows 系统使用 WMI 获取更多信息
                import wmi
                c = wmi.WMI()
                for item in c.Win32_ComputerSystemProduct():
                    uuid_str = item.UUID
                    break
            else:
                # 其他系统使用 uuid
                uuid_str = str(uuid.getnode())
                
            # 组合机器码
            self._machine_id = f"{system}_{machine}_{processor}_{uuid_str}"
            self.logger.info(f"获取机器码成功: {self._machine_id}")
            return self._machine_id
            
        except Exception as e:
            self.logger.error(f"获取机器码失败: {str(e)}")
            raise
            
    def reset_machine_id(self) -> bool:
        """重置机器码"""
        try:
            self._machine_id = None
            self.get_machine_id()  # 重新生成机器码
            self.logger.info("重置机器码成功")
            return True
        except Exception as e:
            self.logger.error(f"重置机器码失败: {str(e)}")
            return False
            
    def patch_machine_id(self, patch: str) -> bool:
        """应用机器码补丁"""
        try:
            if not self._machine_id:
                self.get_machine_id()
                
            # 在机器码后添加补丁
            self._machine_id = f"{self._machine_id}_{patch}"
            self.logger.info(f"应用机器码补丁成功: {patch}")
            return True
        except Exception as e:
            self.logger.error(f"应用机器码补丁失败: {str(e)}")
            return False
            
    def verify_machine_id(self, machine_id: str) -> bool:
        """验证机器码是否有效"""
        try:
            current_id = self.get_machine_id()
            is_valid = current_id == machine_id
            self.logger.info(f"验证机器码: {is_valid}")
            return is_valid
            
        except Exception as e:
            self.logger.error(f"验证机器码失败: {str(e)}")
            return False 