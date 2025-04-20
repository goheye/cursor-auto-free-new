import pytest
import time
from src.email_manager import EmailManager
from src.config import Config

class TestTempMailIntegration:
    @pytest.fixture
    def config(self):
        """加载测试配置"""
        return Config()
        
    @pytest.fixture
    def email_manager(self, config):
        """创建 EmailManager 实例"""
        return EmailManager(config)
        
    def test_real_temp_mail_connection(self, email_manager):
        """测试真实的临时邮箱连接"""
        assert email_manager.connect() is True
        email_manager.disconnect()
        
    def test_real_temp_mail_verification(self, email_manager):
        """测试从真实临时邮箱获取验证码"""
        # 连接邮箱
        assert email_manager.connect() is True
        
        try:
            # 获取验证码
            code = email_manager.get_verification_code(timeout=60, max_retries=3)
            
            # 验证结果
            assert code is not None
            assert len(code) == 6
            assert code.isdigit()
            
        finally:
            # 确保断开连接
            email_manager.disconnect()
            
    def test_real_temp_mail_cleanup(self, email_manager):
        """测试真实临时邮箱的邮件清理功能"""
        # 连接邮箱
        assert email_manager.connect() is True
        
        try:
            # 获取最新邮件
            code, mail_id = email_manager._get_latest_mail_code()
            
            if mail_id:
                # 清理邮件
                assert email_manager._cleanup_mail(mail_id) is True
                
        finally:
            # 确保断开连接
            email_manager.disconnect()
            
    def test_real_temp_mail_no_mails(self, email_manager):
        """测试真实临时邮箱没有邮件的情况"""
        # 连接邮箱
        assert email_manager.connect() is True
        
        try:
            # 获取最新邮件
            code, mail_id = email_manager._get_latest_mail_code()
            
            # 验证结果
            assert code is None
            assert mail_id is None
            
        finally:
            # 确保断开连接
            email_manager.disconnect() 