import pytest
from PyQt6.QtWidgets import QApplication
from gui.main_window import MainWindow
from gui.worker import Worker
from gui.app import App

@pytest.fixture
def app():
    return QApplication([])

@pytest.fixture
def main_window(app):
    return MainWindow()

@pytest.fixture
def worker():
    return Worker()

def test_main_window_initialization(main_window):
    """测试主窗口初始化"""
    assert main_window is not None
    assert main_window.windowTitle() == "Cursor Auto Free"
    assert main_window.minimumSize().width() == 800
    assert main_window.minimumSize().height() == 600
    
def test_auto_tab_elements(main_window):
    """测试自动注册标签页元素"""
    assert main_window.email_input is not None
    assert main_window.password_input is not None
    assert main_window.start_button is not None
    assert main_window.stop_button is not None
    assert main_window.log_text is not None
    
def test_machine_tab_elements(main_window):
    """测试机器码管理标签页元素"""
    assert main_window.machine_id_label is not None
    assert main_window.reset_button is not None
    assert main_window.patch_button is not None
    assert main_window.verify_button is not None
    assert main_window.patch_input is not None
    
def test_settings_tab_elements(main_window):
    """测试设置标签页元素"""
    assert main_window.domain_input is not None
    assert main_window.email_setting_input is not None
    assert main_window.browser_path_input is not None
    assert main_window.save_button is not None
    
def test_worker_signals(worker):
    """测试工作线程信号"""
    assert worker.progress is not None
    assert worker.log is not None
    assert worker.finished is not None
    assert worker.machine_id is not None
    
def test_app_initialization(app):
    """测试应用程序初始化"""
    application = App()
    assert application is not None
    assert application.window is not None
    assert application.worker is not None
    
def test_app_signals(app):
    """测试应用程序信号连接"""
    application = App()
    # 验证信号是否已连接
    assert application.window.start_button.receivers(application.window.start_button.clicked) > 0
    assert application.window.stop_button.receivers(application.window.stop_button.clicked) > 0
    assert application.window.reset_button.receivers(application.window.reset_button.clicked) > 0
    assert application.window.patch_button.receivers(application.window.patch_button.clicked) > 0
    assert application.window.verify_button.receivers(application.window.verify_button.clicked) > 0
    assert application.window.save_button.receivers(application.window.save_button.clicked) > 0 