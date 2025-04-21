from dotenv import load_dotenv
import os
import json
import sys
import logging
import shutil
from datetime import datetime
from typing import Dict, Any, Optional, List
import base64
from cryptography.fernet import Fernet
import yaml
import jsonschema
from pathlib import Path

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

        # 指定配置文件路径
        self.config_dir = os.path.join(application_path, "config")
        self.dotenv_path = os.path.join(application_path, ".env")
        self.accounts_path = os.path.join(self.config_dir, "accounts.json")
        self.template_path = os.path.join(self.config_dir, "template.yaml")
        
        # 创建配置目录
        os.makedirs(self.config_dir, exist_ok=True)
        
        # 初始化加密密钥
        self._init_encryption()
        
        # 加载环境变量
        self.load_env()
        
        # 加载配置
        self.load_config()
        
    def _init_encryption(self) -> None:
        """初始化加密密钥"""
        key_path = os.path.join(self.config_dir, ".key")
        if os.path.exists(key_path):
            with open(key_path, "rb") as f:
                self.key = f.read()
        else:
            self.key = Fernet.generate_key()
            with open(key_path, "wb") as f:
                f.write(self.key)
        self.cipher = Fernet(self.key)
        
    def _encrypt(self, data: str) -> str:
        """加密数据"""
        return self.cipher.encrypt(data.encode()).decode()
        
    def _decrypt(self, data: str) -> str:
        """解密数据"""
        return self.cipher.decrypt(data.encode()).decode()
        
    def load_env(self) -> None:
        """加载环境变量配置文件"""
        if not os.path.exists(self.dotenv_path):
            self.logger.warning(f"配置文件不存在: {self.dotenv_path}")
            self._create_template()
            return
            
        load_dotenv(self.dotenv_path)
        self.logger.info("成功加载环境变量配置文件")
        
    def _create_template(self) -> None:
        """创建配置模板"""
        template = {
            'domain': 'example.com',
            'temp_mail': {
                'enabled': True,
                'mail': 'your_temp_mail',
                'epin': 'your_epin',
                'ext': 'your_ext'
            },
            'imap': {
                'enabled': False,
                'server': 'imap.example.com',
                'port': 993,
                'user': 'your_user',
                'password': 'your_password',
                'directory': 'inbox',
                'protocol': 'IMAP'
            },
            'browser': {
                'user_agent': 'Mozilla/5.0',
                'headless': True,
                'path': '',
                'proxy': ''
            }
        }
        
        with open(self.template_path, 'w', encoding='utf-8') as f:
            yaml.dump(template, f, default_flow_style=False)
        self.logger.info(f"已创建配置模板: {self.template_path}")
        
    def load_config(self) -> None:
        """加载配置"""
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
        
    def validate_config(self, config: Dict[str, Any]) -> bool:
        """验证配置格式"""
        schema = {
            "type": "object",
            "required": ["domain"],
            "properties": {
                "domain": {"type": "string"},
                "temp_mail": {
                    "type": "object",
                    "properties": {
                        "enabled": {"type": "boolean"},
                        "mail": {"type": "string"},
                        "epin": {"type": "string"},
                        "ext": {"type": "string"}
                    }
                },
                "imap": {
                    "type": "object",
                    "properties": {
                        "enabled": {"type": "boolean"},
                        "server": {"type": "string"},
                        "port": {"type": "integer"},
                        "user": {"type": "string"},
                        "password": {"type": "string"},
                        "directory": {"type": "string"},
                        "protocol": {"type": "string"}
                    }
                },
                "browser": {
                    "type": "object",
                    "properties": {
                        "user_agent": {"type": "string"},
                        "headless": {"type": "boolean"},
                        "path": {"type": "string"},
                        "proxy": {"type": "string"}
                    }
                }
            }
        }
        
        try:
            jsonschema.validate(instance=config, schema=schema)
            return True
        except jsonschema.exceptions.ValidationError as e:
            self.logger.error(f"配置验证失败: {str(e)}")
            return False
            
    def save_accounts(self, accounts: List[Dict[str, Any]]) -> None:
        """保存账号信息到配置文件"""
        try:
            # 先备份当前配置文件
            self.backup_config()
            
            # 加密敏感信息
            encrypted_accounts = []
            for account in accounts:
                encrypted = account.copy()
                if 'password' in encrypted:
                    encrypted['password'] = self._encrypt(encrypted['password'])
                encrypted_accounts.append(encrypted)
                
            with open(self.accounts_path, 'w', encoding='utf-8') as f:
                json.dump(encrypted_accounts, f, ensure_ascii=False, indent=2)
            self.logger.info("账号信息保存成功")
        except Exception as e:
            self.logger.error(f"保存账号信息失败: {str(e)}")
            raise
            
    def load_accounts(self) -> List[Dict[str, Any]]:
        """从配置文件加载账号信息"""
        try:
            if not os.path.exists(self.accounts_path):
                self.logger.warning("账号配置文件不存在，返回空列表")
                return []
                
            with open(self.accounts_path, 'r', encoding='utf-8') as f:
                encrypted_accounts = json.load(f)
                
            # 解密敏感信息
            accounts = []
            for account in encrypted_accounts:
                decrypted = account.copy()
                if 'password' in decrypted:
                    decrypted['password'] = self._decrypt(decrypted['password'])
                accounts.append(decrypted)
                
            self.logger.info("账号信息加载成功")
            return accounts
        except json.JSONDecodeError as e:
            self.logger.error(f"账号配置文件格式错误: {str(e)}")
            return []
        except Exception as e:
            self.logger.error(f"加载账号信息失败: {str(e)}")
            raise
            
    def backup_config(self) -> None:
        """备份配置文件"""
        try:
            if not os.path.exists(self.accounts_path):
                self.logger.warning("没有找到配置文件，跳过备份")
                return
                
            backup_dir = os.path.join(self.config_dir, "backups")
            os.makedirs(backup_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = os.path.join(backup_dir, f'accounts_{timestamp}.json')
            shutil.copy2(self.accounts_path, backup_path)
            
            # 清理旧备份（保留最近5个）
            backups = sorted(Path(backup_dir).glob('accounts_*.json'))
            if len(backups) > 5:
                for old_backup in backups[:-5]:
                    old_backup.unlink()
                    
            self.logger.info(f"配置文件已备份到: {backup_path}")
        except Exception as e:
            self.logger.error(f"配置文件备份失败: {str(e)}")
            raise
            
    def get_imap_config(self) -> Dict[str, Any]:
        """获取IMAP配置"""
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
        """获取浏览器配置"""
        return {
            'user_agent': self.browser_user_agent,
            'headless': self.browser_headless,
            'path': self.browser_path,
            'proxy': self.browser_proxy or ''
        }
        
    def get_temp_mail_config(self) -> Dict[str, str]:
        """获取临时邮箱配置"""
        if not all([self.temp_mail, self.temp_mail_epin, self.temp_mail_ext]):
            self.logger.error("临时邮箱配置不完整")
            raise ValueError("临时邮箱配置不完整")
            
        return {
            'temp_mail': self.temp_mail,
            'epin': self.temp_mail_epin,
            'ext': self.temp_mail_ext
        }
        
    def check_config(self) -> None:
        """检查配置项是否有效"""
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