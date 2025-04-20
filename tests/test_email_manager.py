import pytest
from src.config import Config
from src.email_manager import EmailManager

@pytest.fixture
def config():
    return Config()

@pytest.fixture
def email_manager(config):
    return EmailManager(config)

def test_connect(email_manager):
    """测试连接邮箱服务器"""
    assert email_manager.connect() is True
    email_manager.disconnect()
    
def test_disconnect(email_manager):
    """测试断开邮箱连接"""
    email_manager.connect()
    email_manager.disconnect()
    # 验证是否成功断开连接
    assert email_manager.imap is None
    
def test_get_verification_code(email_manager):
    """测试获取验证码"""
    # 注意：这个测试需要实际的邮箱服务器支持
    # 在实际测试中，应该使用测试邮箱账号
    email_manager.connect()
    code = email_manager.get_verification_code(timeout=5)
    email_manager.disconnect()
    # 验证返回的验证码格式
    if code is not None:
        assert isinstance(code, str)
        assert len(code) == 6
        assert code.isdigit()
        
def test_extract_code(email_manager):
    """测试提取验证码"""
    test_text = "您的验证码是：123456，请勿泄露"
    code = email_manager._extract_code(test_text)
    assert code == "123456"
    
    # 测试无效文本
    invalid_text = "没有验证码的文本"
    code = email_manager._extract_code(invalid_text)
    assert code is None 