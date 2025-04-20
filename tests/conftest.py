import pytest
import os
import shutil
from src.config import Config
import sys

# 获取项目根目录
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 将项目根目录添加到 Python 路径
sys.path.insert(0, project_root)

@pytest.fixture(scope="session")
def test_env():
    """创建测试环境"""
    # 创建测试目录
    test_dir = "test_data"
    os.makedirs(test_dir, exist_ok=True)
    
    # 创建测试配置文件
    test_config = {
        "DOMAIN": "test.example.com",
        "TEMP_MAIL": "test@example.com",
        "TEMP_MAIL_EPIN": "test_epin",
        "TEMP_MAIL_EXT": "test_ext",
        "IMAP_SERVER": "imap.test.com",
        "IMAP_PORT": "993",
        "IMAP_USER": "test@test.com",
        "IMAP_PASS": "test_password",
        "IMAP_DIR": "inbox",
        "BROWSER_USER_AGENT": "test_user_agent",
        "BROWSER_HEADLESS": "True",
        "BROWSER_PATH": "test_browser_path"
    }
    
    # 写入测试配置文件
    with open(os.path.join(test_dir, ".env"), "w") as f:
        for key, value in test_config.items():
            f.write(f"{key}={value}\n")
            
    # 设置环境变量
    os.environ["TEST_MODE"] = "True"
    
    yield test_dir
    
    # 清理测试环境
    shutil.rmtree(test_dir)
    if "TEST_MODE" in os.environ:
        del os.environ["TEST_MODE"]
        
@pytest.fixture
def test_config(test_env):
    """创建测试配置对象"""
    config = Config()
    config.dotenv_path = os.path.join(test_env, ".env")
    return config 