import imaplib
import email
import time
from typing import Optional, Dict, Any
from src.logger import logger

class EmailManager:
    def __init__(self, config: Any):
        self.config = config
        self.logger = logger
        self.imap = None
        
    def connect(self) -> bool:
        """连接到邮箱服务器"""
        try:
            if self.config.temp_mail == "null":
                # IMAP 模式
                imap_config = self.config.get_imap_config()
                self.imap = imaplib.IMAP4_SSL(
                    imap_config['server'],
                    int(imap_config['port'])
                )
                self.imap.login(
                    imap_config['user'],
                    imap_config['password']
                )
                self.imap.select(imap_config['directory'])
            else:
                # 临时邮箱模式
                # 这里需要实现临时邮箱的连接逻辑
                pass
                
            self.logger.info("邮箱连接成功")
            return True
            
        except Exception as e:
            self.logger.error(f"邮箱连接失败: {str(e)}")
            return False
            
    def disconnect(self) -> None:
        """断开邮箱连接"""
        try:
            if self.imap:
                self.imap.close()
                self.imap.logout()
            self.logger.info("邮箱断开连接")
        except Exception as e:
            self.logger.error(f"邮箱断开连接失败: {str(e)}")
            
    def get_verification_code(self, timeout: int = 180) -> Optional[str]:
        """获取验证码"""
        try:
            if not self.connect():
                return None
                
            start_time = time.time()
            retry_count = 0
            max_retries = 3
            
            while time.time() - start_time < timeout:
                try:
                    # 搜索新邮件
                    if self.config.temp_mail == "null":
                        # IMAP 模式
                        _, messages = self.imap.search(None, 'UNSEEN')
                        for num in messages[0].split():
                            _, msg_data = self.imap.fetch(num, '(RFC822)')
                            email_body = msg_data[0][1]
                            email_message = email.message_from_bytes(email_body)
                            
                            # 解析邮件内容
                            for part in email_message.walk():
                                if part.get_content_type() == "text/plain":
                                    body = part.get_payload(decode=True)
                                    code = self._extract_code(body.decode())
                                    if code:
                                        self.logger.info(f"获取验证码成功: {code}")
                                        return code
                    else:
                        # 临时邮箱模式
                        # 这里需要实现临时邮箱的验证码获取逻辑
                        pass
                        
                except Exception as e:
                    self.logger.warning(f"获取验证码时出错: {str(e)}")
                    retry_count += 1
                    if retry_count >= max_retries:
                        self.logger.error("获取验证码重试次数过多")
                        return None
                    time.sleep(5)  # 等待5秒后重试
                    continue
                    
                time.sleep(5)  # 等待5秒后再次检查
                
            self.logger.warning("获取验证码超时")
            return None
            
        except Exception as e:
            self.logger.error(f"获取验证码失败: {str(e)}")
            return None
        finally:
            self.disconnect()
            
    def _extract_code(self, text: str) -> Optional[str]:
        """从文本中提取验证码"""
        # 这里需要实现验证码提取的具体逻辑
        # 可以根据实际需求修改正则表达式
        import re
        pattern = r'\b\d{6}\b'  # 假设验证码是6位数字
        match = re.search(pattern, text)
        return match.group(0) if match else None 