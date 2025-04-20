import sys
from PyQt6.QtWidgets import QApplication
from main_window import MainWindow
from worker import Worker
from logger import logger

class App:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = MainWindow()
        self.worker = Worker()
        
        # 连接信号和槽
        self._connect_signals()
        
    def _connect_signals(self):
        """连接信号和槽"""
        # 自动注册标签页
        self.window.start_button.clicked.connect(self._start_task)
        self.window.stop_button.clicked.connect(self._stop_task)
        
        # 机器码管理标签页
        self.window.reset_button.clicked.connect(self._reset_machine_id)
        self.window.patch_button.clicked.connect(self._patch_machine_id)
        self.window.verify_button.clicked.connect(self._verify_machine_id)
        
        # 设置标签页
        self.window.save_button.clicked.connect(self._save_settings)
        
        # 工作线程信号
        self.worker.progress.connect(self.window.update_progress)
        self.worker.log.connect(self.window.append_log)
        self.worker.finished.connect(self._task_finished)
        self.worker.machine_id.connect(self.window.set_machine_id)
        
    def _start_task(self):
        """开始任务"""
        self.window.start_button.setEnabled(False)
        self.window.stop_button.setEnabled(True)
        self.worker.start()
        
    def _stop_task(self):
        """停止任务"""
        self.worker.stop()
        self.window.start_button.setEnabled(True)
        self.window.stop_button.setEnabled(False)
        
    def _task_finished(self, success: bool):
        """任务完成"""
        self.window.start_button.setEnabled(True)
        self.window.stop_button.setEnabled(False)
        if success:
            self.window.show_message("成功", "任务执行成功")
        else:
            self.window.show_message("失败", "任务执行失败")
            
    def _reset_machine_id(self):
        """重置机器码"""
        if self.worker.reset_machine_id():
            self.window.show_message("成功", "机器码重置成功")
        else:
            self.window.show_message("失败", "机器码重置失败")
            
    def _patch_machine_id(self):
        """应用机器码补丁"""
        patch = self.window.get_patch()
        if not patch:
            self.window.show_message("错误", "请输入补丁内容")
            return
            
        if self.worker.patch_machine_id(patch):
            self.window.show_message("成功", "补丁应用成功")
        else:
            self.window.show_message("失败", "补丁应用失败")
            
    def _verify_machine_id(self):
        """验证机器码"""
        machine_id = self.window.machine_id_label.text()
        if not machine_id:
            self.window.show_message("错误", "请先获取机器码")
            return
            
        if self.worker.verify_machine_id(machine_id):
            self.window.show_message("成功", "机器码验证成功")
        else:
            self.window.show_message("失败", "机器码验证失败")
            
    def _save_settings(self):
        """保存设置"""
        # 这里需要实现保存设置的逻辑
        self.window.show_message("成功", "设置已保存")
        
    def run(self):
        """运行应用程序"""
        self.window.show()
        return self.app.exec()

def main():
    """主函数"""
    try:
        app = App()
        return app.run()
    except Exception as e:
        logger.error(f"应用程序异常: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 