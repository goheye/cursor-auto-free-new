from PyQt6.QtCore import QThread, pyqtSignal
from typing import Optional
from logger import logger
from main import CursorAutoFree

class Worker(QThread):
    """工作线程类"""
    progress = pyqtSignal(int)
    log = pyqtSignal(str)
    finished = pyqtSignal(bool)
    machine_id = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.app = CursorAutoFree()
        self.is_running = True
        
    def run(self):
        """运行线程"""
        try:
            self.log.emit("开始执行任务...")
            self.progress.emit(10)
            
            # 获取机器码
            machine_id = self.app.machine_manager.get_machine_id()
            self.machine_id.emit(machine_id)
            self.log.emit(f"当前机器码: {machine_id}")
            self.progress.emit(20)
            
            # 执行注册流程
            if self.app.run():
                self.log.emit("任务执行成功")
                self.progress.emit(100)
                self.finished.emit(True)
            else:
                self.log.emit("任务执行失败")
                self.progress.emit(0)
                self.finished.emit(False)
                
        except Exception as e:
            self.log.emit(f"任务执行出错: {str(e)}")
            self.progress.emit(0)
            self.finished.emit(False)
            
    def stop(self):
        """停止线程"""
        self.is_running = False
        self.log.emit("正在停止任务...")
        
    def reset_machine_id(self) -> bool:
        """重置机器码"""
        try:
            if self.app.machine_manager.reset_machine_id():
                self.log.emit("机器码重置成功")
                return True
            else:
                self.log.emit("机器码重置失败")
                return False
        except Exception as e:
            self.log.emit(f"机器码重置出错: {str(e)}")
            return False
            
    def patch_machine_id(self, patch: str) -> bool:
        """应用机器码补丁"""
        try:
            if self.app.machine_manager.patch_machine_id(patch):
                self.log.emit("补丁应用成功")
                return True
            else:
                self.log.emit("补丁应用失败")
                return False
        except Exception as e:
            self.log.emit(f"补丁应用出错: {str(e)}")
            return False
            
    def verify_machine_id(self, machine_id: str) -> bool:
        """验证机器码"""
        try:
            if self.app.machine_manager.verify_machine_id(machine_id):
                self.log.emit("机器码验证成功")
                return True
            else:
                self.log.emit("机器码验证失败")
                return False
        except Exception as e:
            self.log.emit(f"机器码验证出错: {str(e)}")
            return False 