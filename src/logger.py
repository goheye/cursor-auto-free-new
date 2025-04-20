import logging
import os
from datetime import datetime
from typing import Optional

class Logger:
    def __init__(self, name: str = "cursor_auto_free"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # 创建日志目录
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        # 设置日志文件名
        log_file = os.path.join(log_dir, f"{datetime.now().strftime('%Y-%m-%d')}.log")
        
        # 创建文件处理器
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        
        # 创建控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # 创建格式化器
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # 添加处理器
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        
    def debug(self, message: str) -> None:
        """记录调试信息"""
        self.logger.debug(message)
        
    def info(self, message: str) -> None:
        """记录一般信息"""
        self.logger.info(message)
        
    def warning(self, message: str) -> None:
        """记录警告信息"""
        self.logger.warning(message)
        
    def error(self, message: str) -> None:
        """记录错误信息"""
        self.logger.error(message)
        
    def critical(self, message: str) -> None:
        """记录严重错误信息"""
        self.logger.critical(message)
        
    def exception(self, message: str) -> None:
        """记录异常信息"""
        self.logger.exception(message)

# 创建全局日志实例
logger = Logger() 