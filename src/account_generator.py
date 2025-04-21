import random
import string
import time
from typing import Dict
import logging

class AccountGenerator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.names = self._load_names()
        
    def _load_names(self) -> list:
        """加载名字列表"""
        try:
            with open("names-dataset.txt", "r", encoding="utf-8") as file:
                return file.read().split()
        except FileNotFoundError:
            self.logger.warning("未找到名字数据集文件，使用默认名字列表")
            return ["John", "Jane", "Alex", "Emma", "Michael", "Olivia", 
                   "William", "Sophia", "James", "Isabella", "Robert", 
                   "Mia", "David", "Charlotte", "Joseph", "Amelia"]
                   
    def _generate_random_name(self) -> str:
        """生成随机名字"""
        return random.choice(self.names)
        
    def _generate_random_password(self, length: int = 12) -> str:
        """生成随机密码"""
        characters = string.ascii_letters + string.digits + "!@#$%^&*"
        return ''.join(random.choices(characters, k=length))
        
    def _generate_random_email(self, first_name: str, length: int = 4) -> str:
        """生成随机邮箱地址"""
        # 生成随机数字
        timestamp = str(int(time.time()))[-length:]
        # 生成随机域名
        domains = ["gmail.com", "outlook.com", "yahoo.com", "hotmail.com"]
        domain = random.choice(domains)
        # 组合邮箱地址
        return f"{first_name.lower()}{timestamp}@{domain}"
        
    def generate_account(self) -> Dict:
        """生成完整的账号信息"""
        first_name = self._generate_random_name()
        last_name = self._generate_random_name()
        password = self._generate_random_password()
        email = self._generate_random_email(first_name)
        
        account_info = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": password
        }
        
        self.logger.info(f"生成账号信息: {account_info}")
        return account_info 