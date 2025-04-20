import os
import pytest
from src.config import Config
import json
import tempfile
from datetime import datetime
import shutil
from pathlib import Path

@pytest.fixture(autouse=True)
def cleanup():
    """清理测试环境"""
    yield
    # 清理测试文件
    if os.path.exists('accounts.json'):
        os.remove('accounts.json')
    # 清理环境变量
    os.environ.pop('DOMAIN', None)
    os.environ.pop('TEMP_MAIL', None)
    os.environ.pop('TEMP_MAIL_EPIN', None)
    os.environ.pop('TEMP_MAIL_EXT', None)
    os.environ.pop('IMAP_SERVER', None)
    os.environ.pop('IMAP_PORT', None)
    os.environ.pop('IMAP_USER', None)
    os.environ.pop('IMAP_PASS', None)
    os.environ.pop('BROWSER_USER_AGENT', None)
    os.environ.pop('BROWSER_HEADLESS', None)
    os.environ.pop('BROWSER_PATH', None)
    os.environ.pop('BROWSER_PROXY', None)

def setup_base_env(monkeypatch):
    """设置基本环境变量"""
    # 清理所有相关的环境变量
    for var in [
        'DOMAIN', 'TEMP_MAIL', 'TEMP_MAIL_EPIN', 'TEMP_MAIL_EXT',
        'IMAP_SERVER', 'IMAP_PORT', 'IMAP_USER', 'IMAP_PASS',
        'BROWSER_USER_AGENT', 'BROWSER_HEADLESS', 'BROWSER_PATH', 'BROWSER_PROXY'
    ]:
        monkeypatch.delenv(var, raising=False)
    
    # 设置基本环境变量
    monkeypatch.setenv('DOMAIN', 'test.com')
    monkeypatch.setenv('TEMP_MAIL', 'test@example.com')
    monkeypatch.setenv('TEMP_MAIL_EPIN', 'password123')
    monkeypatch.setenv('TEMP_MAIL_EXT', 'example.com')
    monkeypatch.setenv('BROWSER_USER_AGENT', 'Mozilla/5.0')
    monkeypatch.setenv('BROWSER_HEADLESS', 'True')
    monkeypatch.setenv('BROWSER_PATH', '')
    monkeypatch.setenv('BROWSER_PROXY', '')

@pytest.fixture
def temp_env_file():
    """创建临时的.env文件用于测试"""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.env') as f:
        f.write("""
DOMAIN=example.com
TEMP_MAIL=test
TEMP_MAIL_EPIN=123456
TEMP_MAIL_EXT=@temp.com
IMAP_SERVER=imap.example.com
IMAP_PORT=993
IMAP_USER=test@example.com
IMAP_PASS=password
IMAP_DIR=INBOX
IMAP_PROTOCOL=IMAP
BROWSER_USER_AGENT=Mozilla/5.0
BROWSER_HEADLESS=True
BROWSER_PATH=
BROWSER_PROXY=127.0.0.1:8080
""")
        env_path = f.name
    
    # 修改环境变量指向临时文件
    original_env = os.environ.copy()
    os.environ['ENV_FILE'] = env_path
    
    yield env_path
    
    # 清理
    os.unlink(env_path)
    os.environ.clear()
    os.environ.update(original_env)

@pytest.fixture
def temp_accounts_file():
    """创建临时的accounts.json文件用于测试"""
    accounts_data = [
        {
            "username": "test1",
            "password": "pass1",
            "email": "test1@example.com"
        },
        {
            "username": "test2",
            "password": "pass2",
            "email": "test2@example.com"
        }
    ]
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        json.dump(accounts_data, f)
        accounts_path = f.name
    
    yield accounts_path
    
    os.unlink(accounts_path)

@pytest.fixture
def config(temp_env_file):
    """创建Config实例用于测试"""
    return Config()

def test_config_initialization(config):
    """测试配置初始化"""
    assert config.domain == "example.com"
    assert config.temp_mail == "test"
    assert config.temp_mail_epin == "123456"
    assert config.temp_mail_ext == "@temp.com"

def test_check_config_valid(config):
    """测试配置检查 - 有效配置"""
    config.check_config()

def test_check_config_missing_domain(monkeypatch):
    """测试配置检查 - 缺少域名"""
    setup_base_env(monkeypatch)
    monkeypatch.delenv('DOMAIN', raising=False)
    with pytest.raises(ValueError, match="域名未配置"):
        Config()

def test_check_config_missing_imap(monkeypatch):
    """测试配置检查 - 缺少IMAP配置"""
    setup_base_env(monkeypatch)
    monkeypatch.setenv('TEMP_MAIL', 'null')
    monkeypatch.delenv('IMAP_SERVER', raising=False)
    with pytest.raises(ValueError, match="IMAP 配置不完整"):
        Config()

def test_check_config_missing_temp_mail(monkeypatch):
    """测试配置检查 - 缺少临时邮箱配置"""
    setup_base_env(monkeypatch)
    monkeypatch.delenv('TEMP_MAIL', raising=False)
    with pytest.raises(ValueError, match="临时邮箱配置不完整"):
        Config()

def test_check_config_invalid_browser_path(monkeypatch):
    """测试配置检查 - 无效的浏览器路径"""
    setup_base_env(monkeypatch)
    monkeypatch.setenv('BROWSER_PATH', '/nonexistent/path')
    with pytest.raises(ValueError, match="浏览器路径不存在"):
        Config()

def test_check_config_invalid_proxy(monkeypatch):
    """测试配置检查 - 无效的代理格式"""
    setup_base_env(monkeypatch)
    monkeypatch.setenv('BROWSER_PROXY', 'invalid-proxy')
    with pytest.raises(ValueError, match="代理格式错误"):
        Config()

def test_save_accounts(config):
    """测试保存账号信息"""
    accounts = [
        {"id": "1", "email": "test1@example.com", "status": "active"},
        {"id": "2", "email": "test2@example.com", "status": "inactive"}
    ]
    config.save_accounts(accounts)
    
    # 验证文件是否创建
    assert os.path.exists('accounts.json')
    
    # 验证文件内容
    with open('accounts.json', 'r') as f:
        saved_accounts = json.load(f)
        assert saved_accounts == accounts

def test_load_accounts(config, temp_accounts_file):
    """测试加载账号信息"""
    accounts = config.load_accounts()
    assert len(accounts) == 2
    assert accounts[0]["id"] == "1"
    assert accounts[0]["email"] == "test1@example.com"
    assert accounts[0]["status"] == "active"
    assert accounts[1]["id"] == "2"
    assert accounts[1]["email"] == "test2@example.com"
    assert accounts[1]["status"] == "inactive"

def test_load_accounts_file_not_found(config):
    """测试加载不存在的账号文件"""
    if os.path.exists('accounts.json'):
        os.remove('accounts.json')
    accounts = config.load_accounts()
    assert accounts == []

def test_backup_config(config, temp_accounts_file):
    """测试配置备份"""
    # 创建测试账号文件
    accounts = [{"id": "1", "email": "test@example.com", "status": "active"}]
    with open('accounts.json', 'w') as f:
        json.dump(accounts, f)
    
    # 执行备份
    config.backup_config()
    
    # 验证备份文件是否存在
    backup_files = [f for f in os.listdir('.') if f.startswith('accounts_') and f.endswith('.json')]
    assert len(backup_files) > 0

def test_get_imap_config(monkeypatch):
    """测试获取IMAP配置"""
    setup_base_env(monkeypatch)
    monkeypatch.setenv('TEMP_MAIL', 'null')
    monkeypatch.setenv('IMAP_SERVER', 'imap.test.com')
    monkeypatch.setenv('IMAP_PORT', '993')
    monkeypatch.setenv('IMAP_USER', 'test@test.com')
    monkeypatch.setenv('IMAP_PASS', 'imappass123')
    config = Config()
    
    imap_config = config.get_imap_config()
    assert imap_config['server'] == 'imap.test.com'
    assert imap_config['port'] == '993'
    assert imap_config['user'] == 'test@test.com'
    assert imap_config['password'] == 'imappass123'
    assert imap_config['directory'] == 'inbox'
    assert imap_config['protocol'] == 'IMAP'

def test_get_browser_config(config):
    """测试获取浏览器配置"""
    browser_config = config.get_browser_config()
    assert browser_config['user_agent'] == 'Mozilla/5.0'
    assert browser_config['headless'] is True
    assert browser_config['path'] == ''
    assert browser_config['proxy'] == ''

def test_get_temp_mail_config(config):
    """测试获取临时邮箱配置"""
    temp_mail_config = config.get_temp_mail_config()
    assert temp_mail_config['mail'] == 'test@example.com'
    assert temp_mail_config['epin'] == 'password123'
    assert temp_mail_config['ext'] == 'example.com'

def test_get_temp_mail_config_missing(monkeypatch):
    """测试获取临时邮箱配置 - 缺少配置"""
    setup_base_env(monkeypatch)
    monkeypatch.delenv('TEMP_MAIL', raising=False)
    with pytest.raises(ValueError, match="临时邮箱配置不完整"):
        Config()

def test_get_imap_config_missing(monkeypatch):
    """测试获取IMAP配置 - 缺少配置"""
    setup_base_env(monkeypatch)
    monkeypatch.setenv('TEMP_MAIL', 'null')
    monkeypatch.delenv('IMAP_SERVER', raising=False)
    with pytest.raises(ValueError, match="IMAP 配置不完整"):
        Config()

def test_config_validation(monkeypatch):
    """测试配置验证"""
    setup_base_env(monkeypatch)
    config = Config()
    config.domain = ''
    with pytest.raises(ValueError, match="域名未配置"):
        config.check_config()

def test_error_handling():
    """测试错误处理"""
    with pytest.raises(FileNotFoundError):
        config = Config()
        config.dotenv_path = 'nonexistent.env'
        config.load_env()

def test_config_value_types(config):
    """测试配置值类型"""
    assert isinstance(config.imap_port, str)
    assert isinstance(config.browser_headless, bool)

def test_file_paths(config):
    """测试文件路径处理"""
    assert os.path.exists(config.dotenv_path)
    assert os.path.isfile(config.dotenv_path)

def test_imap_config(config):
    """测试IMAP配置"""
    imap_config = config.get_imap_config()
    assert imap_config['server'] == "imap.example.com"
    assert imap_config['port'] == "993"
    assert imap_config['user'] == "test@example.com"
    assert imap_config['password'] == "password"
    assert imap_config['directory'] == "INBOX"
    assert imap_config['protocol'] == "IMAP"

def test_browser_config(config):
    """测试浏览器配置"""
    browser_config = config.get_browser_config()
    assert browser_config['user_agent'] == "Mozilla/5.0"
    assert browser_config['headless'] is True
    assert browser_config['path'] == ""
    assert browser_config['proxy'] == "127.0.0.1:8080"

def test_temp_mail_config(config):
    """测试临时邮箱配置"""
    temp_mail_config = config.get_temp_mail_config()
    assert temp_mail_config['mail'] == "test"
    assert temp_mail_config['epin'] == "123456"
    assert temp_mail_config['ext'] == "@temp.com"

def test_save_load_accounts(temp_accounts_file, config):
    """测试保存和加载账号信息"""
    # 测试加载账号
    accounts = config.load_accounts()
    assert len(accounts) == 0  # 初始应该为空
    
    # 测试保存账号
    test_accounts = [
        {"username": "test1", "password": "pass1"},
        {"username": "test2", "password": "pass2"}
    ]
    config.save_accounts(test_accounts)
    
    # 测试重新加载
    loaded_accounts = config.load_accounts()
    assert len(loaded_accounts) == 2
    assert loaded_accounts[0]["username"] == "test1"
    assert loaded_accounts[1]["username"] == "test2"

def test_invalid_proxy_format(temp_env_file):
    """测试无效的代理格式"""
    # 修改环境变量中的代理格式
    with open(temp_env_file, 'a') as f:
        f.write("\nBROWSER_PROXY=invalid:proxy:format\n")
    
    with pytest.raises(ValueError) as exc_info:
        Config()
    assert "代理格式错误" in str(exc_info.value)

def test_missing_required_config(temp_env_file):
    """测试缺少必需的配置项"""
    # 创建一个缺少必需配置的环境文件
    with open(temp_env_file, 'w') as f:
        f.write("DOMAIN=\n")  # 空域名
    
    with pytest.raises(ValueError) as exc_info:
        Config()
    assert "域名未配置" in str(exc_info.value)

def test_empty_config_file():
    """测试空配置文件的情况"""
    config = Config()
    accounts = config.load_accounts()
    assert isinstance(accounts, list)
    assert len(accounts) == 0 