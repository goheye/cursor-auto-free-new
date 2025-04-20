from dotenv import load_dotenv
import os
import json
import sys
import logging
import shutil
from datetime import datetime
from typing import Dict, Any, Optional, List

class Config:
    def __init__(self):
        # 配置日志系统
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        
        # 如果还没有处理器，添加一个
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

        # 获取应用程序的根目录路径
        if getattr(sys, "frozen", False):
            # 如果是打包后的可执行文件
            application_path = os.path.dirname(sys.executable)
        else:
            # 如果是开发环境
            application_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # 指定 .env 文件的路径
        self.dotenv_path = os.path.join(application_path, ".env")

        # 加载环境变量
        self.load_env()
        
        # 基础配置
        self.domain = os.getenv('DOMAIN', '').strip()
        
        # 邮箱配置
        self.temp_mail = os.getenv('TEMP_MAIL', '').strip()
        self.temp_mail_epin = os.getenv('TEMP_MAIL_EPIN', '').strip()
        self.temp_mail_ext = os.getenv('TEMP_MAIL_EXT', '').strip()
        
        # IMAP 配置
        self.imap_server = os.getenv('IMAP_SERVER', '').strip()
        self.imap_port = os.getenv('IMAP_PORT', '993').strip()
        self.imap_user = os.getenv('IMAP_USER', '').strip()
        self.imap_pass = os.getenv('IMAP_PASS', '').strip()
        self.imap_dir = os.getenv('IMAP_DIR', 'inbox').strip()
        self.imap_protocol = os.getenv('IMAP_PROTOCOL', 'IMAP').strip()
        
        # 浏览器配置
        self.browser_user_agent = os.getenv('BROWSER_USER_AGENT', 'Mozilla/5.0').strip()
        self.browser_headless = os.getenv('BROWSER_HEADLESS', 'True').lower() == 'true'
        self.browser_path = os.getenv('BROWSER_PATH', '').strip()
        self.browser_proxy = os.getenv('BROWSER_PROXY', '').strip()
        
        # 检查配置
        self.check_config()
        
    def load_env(self) -> None:
        """
        加载环境变量配置文件
        
        Raises:
            FileNotFoundError: 当配置文件不存在时抛出
        """
        if not os.path.exists(self.dotenv_path):
            self.logger.warning(f"配置文件不存在: {self.dotenv_path}")
            return
            
        load_dotenv(self.dotenv_path)
        self.logger.info("成功加载环境变量配置文件")

    def check_config(self) -> None:
        """
        检查配置项是否有效
        
        Raises:
            ValueError: 当配置不完整或无效时抛出
        """
        # 检查域名配置
        if not self.domain:
            self.logger.error("域名未配置")
            raise ValueError("域名未配置")
            
        # 检查邮箱配置
        if self.temp_mail == "null":
            # IMAP 模式
            if not all([self.imap_server, self.imap_port, self.imap_user, self.imap_pass]):
                self.logger.error("IMAP 配置不完整")
                raise ValueError("IMAP 配置不完整")
        elif not all([self.temp_mail, self.temp_mail_epin, self.temp_mail_ext]):
            # 临时邮箱模式
            self.logger.error("临时邮箱配置不完整")
            raise ValueError("临时邮箱配置不完整")
            
        # 检查浏览器配置
        if self.browser_path and not os.path.exists(self.browser_path):
            self.logger.error(f"浏览器路径不存在: {self.browser_path}")
            raise ValueError(f"浏览器路径不存在: {self.browser_path}")
            
        # 检查代理配置
        if self.browser_proxy:
            try:
                proxy_parts = self.browser_proxy.split(':')
                if len(proxy_parts) != 2:
                    self.logger.error("代理格式错误")
                    raise ValueError("代理格式错误")
            except Exception as e:
                self.logger.error(f"代理配置错误: {str(e)}")
                raise ValueError(f"代理配置错误: {str(e)}")
                
        self.logger.info("配置检查通过")
            
    def save_accounts(self, accounts: List[Dict[str, Any]]) -> None:
        """
        保存账号信息到配置文件
        
        Args:
            accounts: 账号信息列表，每个账号是一个字典
            
        Raises:
            Exception: 当保存失败时抛出
        """
        try:
            # 先备份当前配置文件
            self.backup_config()
            
            with open('accounts.json', 'w', encoding='utf-8') as f:
                json.dump(accounts, f, ensure_ascii=False, indent=2)
            self.logger.info("账号信息保存成功")
        except Exception as e:
            self.logger.error(f"保存账号信息失败: {str(e)}")
            raise
            
    def load_accounts(self) -> List[Dict[str, Any]]:
        """
        从配置文件加载账号信息
        
        Returns:
            List[Dict[str, Any]]: 账号信息列表
            
        Raises:
            FileNotFoundError: 当配置文件不存在时抛出
            Exception: 当加载失败时抛出
        """
        try:
            if not os.path.exists('accounts.json'):
                self.logger.warning("账号配置文件不存在，返回空列表")
                return []
                
            with open('accounts.json', 'r', encoding='utf-8') as f:
                accounts = json.load(f)
            self.logger.info("账号信息加载成功")
            return accounts
        except json.JSONDecodeError as e:
            self.logger.error(f"账号配置文件格式错误: {str(e)}")
            return []
        except Exception as e:
            self.logger.error(f"加载账号信息失败: {str(e)}")
            raise
            
    def backup_config(self) -> None:
        """
        备份配置文件
        
        Raises:
            Exception: 当备份失败时抛出
        """
        try:
            if not os.path.exists('accounts.json'):
                self.logger.warning("没有找到配置文件，跳过备份")
                return
                
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = f'accounts_{timestamp}.json'
            shutil.copy2('accounts.json', backup_path)
            self.logger.info(f"配置文件已备份到: {backup_path}")
        except Exception as e:
            self.logger.error(f"配置文件备份失败: {str(e)}")
            raise
            
    def get_imap_config(self) -> Dict[str, Any]:
        """
        获取IMAP配置
        
        Returns:
            Dict[str, Any]: 包含以下键的字典：
                - server: IMAP服务器地址
                - port: IMAP端口号
                - user: 用户名
                - password: 密码
                - directory: 邮箱目录
                - protocol: 协议类型
                
        Raises:
            ValueError: 当配置不完整时抛出
        """
        if not all([self.imap_server, self.imap_port, self.imap_user, self.imap_pass]):
            self.logger.error("IMAP配置不完整")
            raise ValueError("IMAP配置不完整")
            
        return {
            'server': self.imap_server,
            'port': self.imap_port,
            'user': self.imap_user,
            'password': self.imap_pass,
            'directory': self.imap_dir,
            'protocol': self.imap_protocol
        }
        
    def get_browser_config(self) -> Dict[str, Any]:
        """
        获取浏览器配置
        
        Returns:
            Dict[str, Any]: 包含以下键的字典：
                - user_agent: 浏览器用户代理
                - headless: 是否无头模式
                - path: 浏览器路径
                - proxy: 代理设置
        """
        return {
            'user_agent': self.browser_user_agent,
            'headless': self.browser_headless,
            'path': self.browser_path,
            'proxy': self.browser_proxy or ''  # 确保返回空字符串而不是 None
        }
        
    def get_temp_mail_config(self) -> Dict[str, str]:
        """
        获取临时邮箱配置
        
        Returns:
            Dict[str, str]: 包含以下键的字典：
                - mail: 临时邮箱地址
                - epin: 临时邮箱密码
                - ext: 临时邮箱后缀
                
        Raises:
            ValueError: 当配置不完整时抛出
        """
        if not all([self.temp_mail, self.temp_mail_epin, self.temp_mail_ext]):
            self.logger.error("临时邮箱配置不完整")
            raise ValueError("临时邮箱配置不完整")
            
        return {
            'temp_mail': self.temp_mail,
            'temp_mail_epin': self.temp_mail_epin,
            'temp_mail_ext': self.temp_mail_ext
        }
        
    def get_protocol(self) -> str:
        """获取邮箱协议类型"""
        return self.imap_protocol if self.temp_mail == "null" else "TEMP" 