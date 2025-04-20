from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QTextEdit,
    QTabWidget, QMessageBox, QProgressBar
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QIcon
import qdarkstyle
from typing import Optional
from logger import logger

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cursor Auto Free")
        self.setMinimumSize(800, 600)
        
        # 设置样式
        self.setStyleSheet(qdarkstyle.load_stylesheet())
        
        # 创建主窗口部件
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        
        # 创建主布局
        self.main_layout = QVBoxLayout(self.main_widget)
        
        # 创建标签页
        self.tab_widget = QTabWidget()
        self.main_layout.addWidget(self.tab_widget)
        
        # 添加标签页
        self.tab_widget.addTab(self._create_auto_tab(), "自动注册")
        self.tab_widget.addTab(self._create_machine_tab(), "机器码管理")
        self.tab_widget.addTab(self._create_settings_tab(), "设置")
        
        # 创建状态栏
        self.statusBar().showMessage("就绪")
        
        # 创建进度条
        self.progress_bar = QProgressBar()
        self.statusBar().addPermanentWidget(self.progress_bar)
        self.progress_bar.hide()
        
    def _create_auto_tab(self) -> QWidget:
        """创建自动注册标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # 账号信息组
        account_group = QWidget()
        account_layout = QVBoxLayout(account_group)
        
        # 邮箱输入
        email_layout = QHBoxLayout()
        email_label = QLabel("邮箱:")
        self.email_input = QLineEdit()
        email_layout.addWidget(email_label)
        email_layout.addWidget(self.email_input)
        account_layout.addLayout(email_layout)
        
        # 密码输入
        password_layout = QHBoxLayout()
        password_label = QLabel("密码:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        account_layout.addLayout(password_layout)
        
        layout.addWidget(account_group)
        
        # 操作按钮
        button_layout = QHBoxLayout()
        self.start_button = QPushButton("开始注册")
        self.stop_button = QPushButton("停止")
        self.stop_button.setEnabled(False)
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        layout.addLayout(button_layout)
        
        # 日志显示
        log_label = QLabel("操作日志:")
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        layout.addWidget(log_label)
        layout.addWidget(self.log_text)
        
        return tab
        
    def _create_machine_tab(self) -> QWidget:
        """创建机器码管理标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # 当前机器码显示
        machine_layout = QHBoxLayout()
        machine_label = QLabel("当前机器码:")
        self.machine_id_label = QLabel("")
        machine_layout.addWidget(machine_label)
        machine_layout.addWidget(self.machine_id_label)
        layout.addLayout(machine_layout)
        
        # 机器码操作
        operation_layout = QHBoxLayout()
        self.reset_button = QPushButton("重置机器码")
        self.patch_button = QPushButton("应用补丁")
        self.verify_button = QPushButton("验证机器码")
        operation_layout.addWidget(self.reset_button)
        operation_layout.addWidget(self.patch_button)
        operation_layout.addWidget(self.verify_button)
        layout.addLayout(operation_layout)
        
        # 补丁输入
        patch_layout = QHBoxLayout()
        patch_label = QLabel("补丁内容:")
        self.patch_input = QLineEdit()
        patch_layout.addWidget(patch_label)
        patch_layout.addWidget(self.patch_input)
        layout.addLayout(patch_layout)
        
        return tab
        
    def _create_settings_tab(self) -> QWidget:
        """创建设置标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # 域名设置
        domain_layout = QHBoxLayout()
        domain_label = QLabel("域名:")
        self.domain_input = QLineEdit()
        domain_layout.addWidget(domain_label)
        domain_layout.addWidget(self.domain_input)
        layout.addLayout(domain_layout)
        
        # 邮箱设置
        email_layout = QHBoxLayout()
        email_label = QLabel("临时邮箱:")
        self.email_setting_input = QLineEdit()
        email_layout.addWidget(email_label)
        email_layout.addWidget(self.email_setting_input)
        layout.addLayout(email_layout)
        
        # 浏览器设置
        browser_layout = QHBoxLayout()
        browser_label = QLabel("浏览器路径:")
        self.browser_path_input = QLineEdit()
        browser_layout.addWidget(browser_label)
        browser_layout.addWidget(self.browser_path_input)
        layout.addLayout(browser_layout)
        
        # 保存按钮
        save_button = QPushButton("保存设置")
        layout.addWidget(save_button)
        
        return tab
        
    def show_message(self, title: str, message: str, icon: QMessageBox.Icon = QMessageBox.Icon.Information) -> None:
        """显示消息对话框"""
        QMessageBox(self).information(self, title, message, icon)
        
    def update_progress(self, value: int) -> None:
        """更新进度条"""
        self.progress_bar.setValue(value)
        if value == 100:
            self.progress_bar.hide()
        else:
            self.progress_bar.show()
            
    def append_log(self, message: str) -> None:
        """添加日志"""
        self.log_text.append(message)
        self.log_text.verticalScrollBar().setValue(
            self.log_text.verticalScrollBar().maximum()
        )
        
    def set_machine_id(self, machine_id: str) -> None:
        """设置机器码显示"""
        self.machine_id_label.setText(machine_id)
        
    def get_email(self) -> str:
        """获取邮箱"""
        return self.email_input.text()
        
    def get_password(self) -> str:
        """获取密码"""
        return self.password_input.text()
        
    def get_patch(self) -> str:
        """获取补丁内容"""
        return self.patch_input.text()
        
    def get_domain(self) -> str:
        """获取域名"""
        return self.domain_input.text()
        
    def get_temp_email(self) -> str:
        """获取临时邮箱"""
        return self.email_setting_input.text()
        
    def get_browser_path(self) -> str:
        """获取浏览器路径"""
        return self.browser_path_input.text() 