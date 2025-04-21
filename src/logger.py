import logging
import os
from datetime import datetime
from typing import Optional
from logging.handlers import RotatingFileHandler
import colorama
from colorama import Fore, Style
import json
import re

class Logger:
    def __init__(self, name: str = "cursor_auto_free"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # 初始化colorama
        colorama.init()
        
        # 创建日志目录
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        # 设置日志文件名
        log_file = os.path.join(log_dir, f"{datetime.now().strftime('%Y-%m-%d')}.log")
        
        # 创建文件处理器（带轮转）
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
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
        
        # 初始化统计信息
        self.stats = {
            'total': 0,
            'success': 0,
            'failed': 0,
            'errors': []
        }
        
    def _get_color(self, level: str) -> str:
        """获取日志级别对应的颜色"""
        colors = {
            'DEBUG': Fore.BLUE,
            'INFO': Fore.GREEN,
            'WARNING': Fore.YELLOW,
            'ERROR': Fore.RED,
            'CRITICAL': Fore.RED + Style.BRIGHT
        }
        return colors.get(level, Fore.WHITE)
        
    def debug(self, message: str) -> None:
        """记录调试信息"""
        self.logger.debug(message)
        self.stats['total'] += 1
        
    def info(self, message: str) -> None:
        """记录一般信息"""
        self.logger.info(message)
        self.stats['total'] += 1
        self.stats['success'] += 1
        
    def warning(self, message: str) -> None:
        """记录警告信息"""
        self.logger.warning(message)
        self.stats['total'] += 1
        
    def error(self, message: str) -> None:
        """记录错误信息"""
        self.logger.error(message)
        self.stats['total'] += 1
        self.stats['failed'] += 1
        self.stats['errors'].append({
            'time': datetime.now().isoformat(),
            'message': message
        })
        
    def critical(self, message: str) -> None:
        """记录严重错误信息"""
        self.logger.critical(message)
        self.stats['total'] += 1
        self.stats['failed'] += 1
        self.stats['errors'].append({
            'time': datetime.now().isoformat(),
            'message': message
        })
        
    def exception(self, message: str) -> None:
        """记录异常信息"""
        self.logger.exception(message)
        self.stats['total'] += 1
        self.stats['failed'] += 1
        self.stats['errors'].append({
            'time': datetime.now().isoformat(),
            'message': message
        })
        
    def get_stats(self) -> dict:
        """获取统计信息"""
        return self.stats
        
    def save_stats(self, filename: str = "logs/stats.json") -> None:
        """保存统计信息到文件"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.stats, f, indent=2, ensure_ascii=False)
            
    def analyze_logs(self, pattern: str = None) -> list:
        """分析日志文件"""
        results = []
        log_dir = "logs"
        for filename in os.listdir(log_dir):
            if filename.endswith('.log'):
                with open(os.path.join(log_dir, filename), 'r', encoding='utf-8') as f:
                    for line in f:
                        if pattern and re.search(pattern, line):
                            results.append(line.strip())
        return results

# 创建全局日志实例
logger = Logger() 