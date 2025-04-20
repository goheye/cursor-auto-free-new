import imaplib
import email
from email import message
import time
import re
import logging
import poplib
from datetime import datetime
from typing import Optional, Dict, Any, Tuple
from email.parser import Parser
from src.logger import logger

class EmailManager:
    def __init__(self, config: Any):
        self.config = config
        self.logger = logger
        self.imap = None
        self.pop3 = None
        self.session = None
        self.protocol = self.config.get_protocol() or 'IMAP'
        
    def connect(self) -> bool:
        """连接到邮箱服务器"""
        try:
            if self.config.temp_mail == "null":
                if self.protocol.upper() == 'IMAP':
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
                    
                    # 针对网易系邮箱的特殊处理
                    if imap_config['user'].endswith(('@163.com', '@126.com', '@yeah.net')):
                        imap_id = ("name", imap_config['user'].split('@')[0], 
                                 "contact", imap_config['user'], 
                                 "version", "1.0.0", 
                                 "vendor", "imaplib")
                        self.imap.xatom('ID', '("' + '" "'.join(imap_id) + '")')
                        
                    self.imap.select(imap_config['directory'])
                else:
                    # POP3 模式
                    pop3_config = self.config.get_imap_config()
                    self.pop3 = poplib.POP3_SSL(
                        pop3_config['server'],
                        int(pop3_config['port'])
                    )
                    self.pop3.user(pop3_config['user'])
                    self.pop3.pass_(pop3_config['password'])
            else:
                # 临时邮箱模式
                import requests
                self.session = requests.Session()
                
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
            if self.pop3:
                self.pop3.quit()
            self.logger.info("邮箱断开连接")
        except Exception as e:
            self.logger.error(f"邮箱断开连接失败: {str(e)}")
            
    def get_verification_code(self, timeout: int = 180, max_retries: int = 5) -> Optional[str]:
        """获取验证码，带有重试机制"""
        for attempt in range(max_retries):
            try:
                self.logger.info(f"尝试获取验证码 (第 {attempt + 1}/{max_retries} 次)...")
                
                if not self.connect():
                    return None
                    
                if self.config.temp_mail == "null":
                    if self.protocol.upper() == 'IMAP':
                        code = self._get_mail_code_by_imap()
                    else:
                        code = self._get_mail_code_by_pop3()
                else:
                    code, first_id = self._get_latest_mail_code()
                    if code and first_id:
                        self._cleanup_mail(first_id)
                        
                if code:
                    self.logger.info(f"成功获取验证码: {code}")
                    return code
                    
                if attempt < max_retries - 1:
                    self.logger.warning(f"未获取到验证码，等待 {timeout//max_retries} 秒后重试...")
                    time.sleep(timeout//max_retries)
                    
            except Exception as e:
                self.logger.error(f"获取验证码失败: {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(timeout//max_retries)
                else:
                    raise Exception(f"获取验证码失败且已达最大重试次数: {str(e)}") from e
            finally:
                self.disconnect()
                
        raise Exception(f"经过 {max_retries} 次尝试后仍未获取到验证码")
        
    def _get_mail_code_by_imap(self, retry: int = 0) -> Optional[str]:
        """使用 IMAP 协议获取验证码"""
        if retry > 0:
            time.sleep(3)
        if retry >= 20:
            raise Exception("获取验证码超时")
            
        try:
            search_by_date = False
            if self.config.get_imap_config()['user'].endswith(('@163.com', '@126.com', '@yeah.net')):
                search_by_date = True
                
            if search_by_date:
                date = datetime.now().strftime("%d-%b-%Y")
                status, messages = self.imap.search(None, f'ON {date} UNSEEN')
            else:
                status, messages = self.imap.search(None, 'UNSEEN')
                
            if status != 'OK':
                return None
                
            mail_ids = messages[0].split()
            if not mail_ids:
                return self._get_mail_code_by_imap(retry=retry + 1)
                
            for mail_id in reversed(mail_ids):
                status, msg_data = self.imap.fetch(mail_id, '(RFC822)')
                if status != 'OK':
                    continue
                    
                raw_email = msg_data[0][1]
                email_message = email.message_from_bytes(raw_email)
                
                if search_by_date and email_message['to'] != self.config.get_imap_config()['user']:
                    continue
                    
                body = self._extract_email_body(email_message)
                if body:
                    code_match = re.search(r"(?<![a-zA-Z@.])\b\d{6}\b", body)
                    if code_match:
                        code = code_match.group()
                        self.imap.store(mail_id, '+FLAGS', '\\Deleted')
                        self.imap.expunge()
                        return code
                        
            return self._get_mail_code_by_imap(retry=retry + 1)
            
        except Exception as e:
            self.logger.error(f"IMAP获取验证码失败: {str(e)}")
            return None
            
    def _get_mail_code_by_pop3(self, retry: int = 0) -> Optional[str]:
        """使用 POP3 协议获取验证码"""
        if retry > 0:
            time.sleep(3)
        if retry >= 20:
            raise Exception("获取验证码超时")
            
        try:
            num_messages = len(self.pop3.list()[1])
            for i in range(num_messages, max(1, num_messages-9), -1):
                response, lines, octets = self.pop3.retr(i)
                msg_content = b'\r\n'.join(lines).decode('utf-8')
                msg = Parser().parsestr(msg_content)
                
                if 'no-reply@cursor.sh' in msg.get('From', ''):
                    body = self._extract_email_body(msg)
                    if body:
                        code_match = re.search(r"(?<![a-zA-Z@.])\b\d{6}\b", body)
                        if code_match:
                            return code_match.group()
                            
            return self._get_mail_code_by_pop3(retry=retry + 1)
            
        except Exception as e:
            self.logger.error(f"POP3获取验证码失败: {str(e)}")
            return None
            
    def _get_latest_mail_code(self) -> Tuple[Optional[str], Optional[str]]:
        """获取临时邮箱的最新验证码"""
        try:
            mail_list_url = f"https://tempmail.plus/api/mails?email={self.config.temp_mail}&limit=20&epin={self.config.temp_mail_epin}"
            mail_list_response = self.session.get(mail_list_url)
            mail_list_data = mail_list_response.json()
            
            if not mail_list_data.get("result"):
                return None, None
                
            first_id = mail_list_data.get("first_id")
            if not first_id:
                return None, None
                
            mail_detail_url = f"https://tempmail.plus/api/mails/{first_id}?email={self.config.temp_mail}&epin={self.config.temp_mail_epin}"
            mail_detail_response = self.session.get(mail_detail_url)
            mail_detail_data = mail_detail_response.json()
            
            if not mail_detail_data.get("result"):
                return None, None
                
            mail_text = mail_detail_data.get("text", "")
            mail_subject = mail_detail_data.get("subject", "")
            self.logger.info(f"找到邮件主题: {mail_subject}")
            
            code_match = re.search(r"(?<![a-zA-Z@.])\b\d{6}\b", mail_text)
            if code_match:
                return code_match.group(), first_id
                
            return None, None
            
        except Exception as e:
            self.logger.error(f"获取临时邮箱验证码失败: {str(e)}")
            return None, None
            
    def _cleanup_mail(self, first_id: str) -> None:
        """清理临时邮箱的邮件"""
        try:
            delete_url = f"https://tempmail.plus/api/mails/{first_id}?email={self.config.temp_mail}&epin={self.config.temp_mail_epin}"
            self.session.delete(delete_url)
        except Exception as e:
            self.logger.error(f"清理邮件失败: {str(e)}")
            
    def _extract_email_body(self, email_message: message.Message) -> str:
        """提取邮件正文"""
        try:
            if email_message.is_multipart():
                for part in email_message.walk():
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition"))
                    if content_type == "text/plain" and "attachment" not in content_disposition:
                        charset = part.get_content_charset() or 'utf-8'
                        try:
                            body = part.get_payload(decode=True).decode(charset, errors='ignore')
                            return body
                        except Exception as e:
                            logging.error(f"解码邮件正文失败: {e}")
            else:
                content_type = email_message.get_content_type()
                if content_type == "text/plain":
                    charset = email_message.get_content_charset() or 'utf-8'
                    try:
                        body = email_message.get_payload(decode=True).decode(charset, errors='ignore')
                        return body
                    except Exception as e:
                        logging.error(f"解码邮件正文失败: {e}")
            return ""
        except Exception as e:
            self.logger.error(f"提取邮件正文失败: {str(e)}")
            return "" 