import pytest
import imaplib
from unittest.mock import MagicMock, patch, Mock
from src.config import Config
from src.email_manager import EmailManager
import poplib
import requests

@pytest.fixture
def config():
    config = Config()
    # 设置测试配置
    config.domain = "example.com"
    config.temp_mail = "test@example.com"
    config.temp_mail_epin = "password"
    config.temp_mail_ext = "@example.com"
    config.imap_server = "imap.example.com"
    config.imap_port = "993"
    config.imap_user = "test@example.com"
    config.imap_pass = "password"
    config.imap_dir = "INBOX"
    config.browser_proxy = None  # 禁用代理检查
    return config

@pytest.fixture
def email_manager(config):
    return EmailManager(config)

def test_connect_success(email_manager):
    """测试成功连接邮箱服务器"""
    with patch('imaplib.IMAP4_SSL') as mock_imap:
        mock_imap_instance = MagicMock()
        mock_imap.return_value = mock_imap_instance
        email_manager.config.temp_mail = "null"
        email_manager.config.imap_server = "imap.example.com"
        email_manager.config.imap_port = "993"
        email_manager.config.imap_user = "test@example.com"
        email_manager.config.imap_pass = "password"
        email_manager.config.imap_dir = "INBOX"
        
        result = email_manager.connect()
        assert result is True
        assert email_manager.imap is not None
        mock_imap_instance.login.assert_called_once_with("test@example.com", "password")
        mock_imap_instance.select.assert_called_once_with("INBOX")

def test_connect_failure(email_manager):
    """测试连接邮箱服务器失败"""
    with patch('imaplib.IMAP4_SSL') as mock_imap:
        mock_imap.side_effect = imaplib.IMAP4.error("Connection failed")
        email_manager.config.temp_mail = "null"
        
        result = email_manager.connect()
        assert result is False
        assert email_manager.imap is None

def test_disconnect_success(email_manager):
    """测试成功断开邮箱连接"""
    with patch('imaplib.IMAP4_SSL') as mock_imap:
        mock_imap_instance = MagicMock()
        mock_imap.return_value = mock_imap_instance
        email_manager.connect()
        
        email_manager.disconnect()
        mock_imap_instance.close.assert_called_once()
        mock_imap_instance.logout.assert_called_once()
        assert email_manager.imap is None

def test_extract_code_success(email_manager):
    """测试成功提取验证码"""
    test_cases = [
        ("您的验证码是：123456，请勿泄露", "123456"),
        ("验证码：123456", "123456"),
        ("Code: 123456", "123456"),
        ("Your verification code is 123456", "123456"),
    ]
    
    for text, expected in test_cases:
        result = email_manager._extract_code(text)
        assert result == expected

def test_extract_code_failure(email_manager):
    """测试提取验证码失败"""
    test_cases = [
        "没有验证码的文本",
        "验证码：123",  # 位数不足
        "验证码：1234567",  # 位数过多
        "验证码：abc123",  # 包含非数字字符
    ]
    
    for text in test_cases:
        result = email_manager._extract_code(text)
        assert result is None

def test_get_verification_code_success(email_manager):
    """测试成功获取验证码"""
    with patch('imaplib.IMAP4_SSL') as mock_imap:
        mock_imap_instance = MagicMock()
        mock_imap.return_value = mock_imap_instance
        
        # 模拟邮件内容
        email_body = b"Subject: Verification Code\r\n\r\nYour code is: 123456"
        mock_imap_instance.search.return_value = (None, [b'1'])
        mock_imap_instance.fetch.return_value = (None, [(None, email_body)])
        
        email_manager.config.temp_mail = "null"
        email_manager.connect()
        
        result = email_manager.get_verification_code(timeout=1)
        assert result == "123456"

def test_get_verification_code_timeout(email_manager):
    """测试获取验证码超时"""
    with patch('imaplib.IMAP4_SSL') as mock_imap:
        mock_imap_instance = MagicMock()
        mock_imap.return_value = mock_imap_instance
        
        # 模拟没有新邮件
        mock_imap_instance.search.return_value = (None, [b''])
        
        email_manager.config.temp_mail = "null"
        email_manager.connect()
        
        result = email_manager.get_verification_code(timeout=1)
        assert result is None

def test_get_verification_code_retry(email_manager):
    """测试获取验证码重试机制"""
    with patch('imaplib.IMAP4_SSL') as mock_imap:
        mock_imap_instance = MagicMock()
        mock_imap.return_value = mock_imap_instance
        
        # 模拟第一次失败，第二次成功
        mock_imap_instance.search.side_effect = [
            (None, [b'']),  # 第一次没有邮件
            (None, [b'1'])  # 第二次有邮件
        ]
        
        email_body = b"Subject: Verification Code\r\n\r\nYour code is: 123456"
        mock_imap_instance.fetch.return_value = (None, [(None, email_body)])
        
        email_manager.config.temp_mail = "null"
        email_manager.connect()
        
        result = email_manager.get_verification_code(timeout=2)
        assert result == "123456"
        assert mock_imap_instance.search.call_count == 2

class MockConfig:
    def __init__(self, **kwargs):
        self.protocol = kwargs.get('protocol', 'IMAP')
        self.temp_mail = kwargs.get('temp_mail', 'null')
        self.temp_mail_epin = kwargs.get('temp_mail_epin', 'test_epin')
        self.temp_mail_ext = kwargs.get('temp_mail_ext', '@example.com')
        self.server = kwargs.get('server', 'imap.example.com')
        self.port = kwargs.get('port', 993)
        self.user = kwargs.get('user', 'test@example.com')
        self.password = kwargs.get('password', 'password')
        self.directory = kwargs.get('directory', 'INBOX')

    def get_imap_config(self):
        return {
            'server': self.server,
            'port': self.port,
            'user': self.user,
            'password': self.password,
            'directory': self.directory
        }

    def get_protocol(self):
        return self.protocol

@pytest.fixture
def mock_imap():
    with patch('imaplib.IMAP4_SSL') as mock:
        mock_instance = Mock()
        mock.return_value = mock_instance
        mock_instance.login.return_value = ('OK', [])
        mock_instance.select.return_value = ('OK', [])
        mock_instance.search.return_value = ('OK', [b'1'])
        mock_instance.fetch.return_value = ('OK', [(None, b'Subject: Test\r\n\r\nYour code is 123456')])
        mock_instance.store.return_value = ('OK', [])
        mock_instance.expunge.return_value = ('OK', [])
        yield mock_instance

@pytest.fixture
def mock_pop3():
    with patch('poplib.POP3_SSL') as mock:
        mock_instance = Mock()
        mock.return_value = mock_instance
        mock_instance.user.return_value = None
        mock_instance.pass_.return_value = None
        mock_instance.list.return_value = (None, [b'1 100'])
        mock_instance.retr.return_value = (None, [b'Subject: Test', b'', b'Your code is 123456'])
        yield mock_instance

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

def test_imap_connection(mock_imap):
    """测试 IMAP 连接功能"""
    config = MockConfig(protocol='IMAP')
    email_manager = EmailManager(config)
    assert email_manager.connect() is True
    email_manager.disconnect()

def test_pop3_connection(mock_pop3):
    """测试 POP3 连接功能"""
    config = MockConfig(protocol='POP3')
    email_manager = EmailManager(config)
    assert email_manager.connect() is True
    email_manager.disconnect()

def test_temp_mail_connection(mock_requests):
    """测试临时邮箱连接功能"""
    config = MockConfig(temp_mail='test')
    email_manager = EmailManager(config)
    assert email_manager.connect() is True
    email_manager.disconnect()

def test_imap_verification_code(mock_imap):
    """测试从 IMAP 邮箱获取验证码"""
    config = MockConfig(protocol='IMAP')
    email_manager = EmailManager(config)
    code = email_manager.get_verification_code()
    assert code is not None
    assert len(code) == 6
    assert code.isdigit()

def test_pop3_verification_code(mock_pop3):
    """测试从 POP3 邮箱获取验证码"""
    config = MockConfig(protocol='POP3')
    email_manager = EmailManager(config)
    code = email_manager.get_verification_code()
    assert code is not None
    assert len(code) == 6
    assert code.isdigit()

def test_temp_mail_verification_code(mock_requests):
    """测试从临时邮箱获取验证码"""
    config = MockConfig(temp_mail='test')
    email_manager = EmailManager(config)
    code = email_manager.get_verification_code()
    assert code is not None
    assert len(code) == 6
    assert code.isdigit()

def test_connection_error():
    """测试连接错误处理"""
    config = MockConfig(server='invalid.server.com')
    email_manager = EmailManager(config)
    assert email_manager.connect() is False

def test_authentication_error(mock_imap):
    """测试认证错误处理"""
    mock_imap.login.side_effect = imaplib.IMAP4.error('Authentication failed')
    config = MockConfig(protocol='IMAP')
    email_manager = EmailManager(config)
    assert email_manager.connect() is False

def test_timeout_handling(mock_imap):
    """测试超时处理"""
    mock_imap.search.side_effect = TimeoutError()
    config = MockConfig(protocol='IMAP')
    email_manager = EmailManager(config)
    with pytest.raises(Exception):
        email_manager.get_verification_code(timeout=1, max_retries=1)

def test_netease_mail(mock_imap):
    """测试网易邮箱特殊处理"""
    config = MockConfig(user='test@163.com')
    email_manager = EmailManager(config)
    assert email_manager.connect() is True
    code = email_manager.get_verification_code()
    assert code is not None
    email_manager.disconnect() 