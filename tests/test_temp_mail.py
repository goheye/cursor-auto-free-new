import pytest
from unittest.mock import Mock, patch
from src.email_manager import EmailManager

class MockConfig:
    def __init__(self, **kwargs):
        self.temp_mail = kwargs.get('temp_mail', 'test@example.com')
        self.temp_mail_epin = kwargs.get('temp_mail_epin', 'test_epin')
        self.temp_mail_ext = kwargs.get('temp_mail_ext', '@example.com')
        self.protocol = 'IMAP'  # 默认使用IMAP协议

    def get_protocol(self):
        return self.protocol

@pytest.fixture
def mock_requests():
    with patch('requests.Session') as mock:
        mock_instance = Mock()
        mock.return_value = mock_instance
        mock_instance.get.return_value.json.return_value = {
            'result': True,
            'first_id': '123',
            'text': 'Your code is 123456'
        }
        yield mock_instance

def test_temp_mail_connection(mock_requests):
    """测试临时邮箱连接功能"""
    config = MockConfig(temp_mail='test@example.com')
    email_manager = EmailManager(config)
    assert email_manager.connect() is True
    email_manager.disconnect()

def test_temp_mail_verification_code(mock_requests):
    """测试从临时邮箱获取验证码"""
    config = MockConfig(temp_mail='test@example.com')
    email_manager = EmailManager(config)
    code = email_manager.get_verification_code()
    assert code is not None
    assert len(code) == 6
    assert code.isdigit()

def test_temp_mail_cleanup(mock_requests):
    """测试临时邮箱邮件清理功能"""
    config = MockConfig(temp_mail='test@example.com')
    email_manager = EmailManager(config)
    email_manager.connect()
    email_manager._cleanup_mail('123')
    mock_requests.return_value.delete.assert_called_once()

def test_temp_mail_no_mails(mock_requests):
    """测试临时邮箱没有邮件的情况"""
    mock_requests.return_value.get.return_value.json.return_value = {
        'result': False
    }
    config = MockConfig(temp_mail='test@example.com')
    email_manager = EmailManager(config)
    code = email_manager.get_verification_code()
    assert code is None

def test_temp_mail_invalid_response(mock_requests):
    """测试临时邮箱返回无效响应的情况"""
    mock_requests.return_value.get.return_value.json.return_value = {
        'result': True,
        'first_id': None
    }
    config = MockConfig(temp_mail='test@example.com')
    email_manager = EmailManager(config)
    code = email_manager.get_verification_code()
    assert code is None

def test_temp_mail_network_error(mock_requests):
    """测试临时邮箱网络错误的情况"""
    mock_requests.return_value.get.side_effect = Exception("Network error")
    config = MockConfig(temp_mail='test@example.com')
    email_manager = EmailManager(config)
    code = email_manager.get_verification_code()
    assert code is None 