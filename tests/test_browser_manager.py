import pytest
from src.config import Config
from src.browser_manager import BrowserManager

@pytest.fixture
def config():
    return Config()

@pytest.fixture
def browser_manager(config):
    return BrowserManager(config)

def test_start_browser(browser_manager):
    """测试启动浏览器"""
    assert browser_manager.start_browser() is True
    browser_manager.close_browser()
    
def test_close_browser(browser_manager):
    """测试关闭浏览器"""
    browser_manager.start_browser()
    browser_manager.close_browser()
    assert browser_manager.page is None
    
def test_navigate_to(browser_manager):
    """测试导航到URL"""
    browser_manager.start_browser()
    assert browser_manager.navigate_to("https://www.example.com") is True
    browser_manager.close_browser()
    
def test_wait_for_element(browser_manager):
    """测试等待元素"""
    browser_manager.start_browser()
    browser_manager.navigate_to("https://www.example.com")
    # 测试等待不存在的元素
    assert browser_manager.wait_for_element("#non-existent-element", timeout=1) is False
    browser_manager.close_browser()
    
def test_click_element(browser_manager):
    """测试点击元素"""
    browser_manager.start_browser()
    browser_manager.navigate_to("https://www.example.com")
    # 测试点击不存在的元素
    assert browser_manager.click_element("#non-existent-button") is False
    browser_manager.close_browser()
    
def test_input_text(browser_manager):
    """测试输入文本"""
    browser_manager.start_browser()
    browser_manager.navigate_to("https://www.example.com")
    # 测试在不存在的输入框中输入文本
    assert browser_manager.input_text("#non-existent-input", "test") is False
    browser_manager.close_browser()
    
def test_get_text(browser_manager):
    """测试获取文本"""
    browser_manager.start_browser()
    browser_manager.navigate_to("https://www.example.com")
    # 测试获取不存在的元素的文本
    assert browser_manager.get_text("#non-existent-text") is None
    browser_manager.close_browser()
    
def test_execute_script(browser_manager):
    """测试执行JavaScript脚本"""
    browser_manager.start_browser()
    browser_manager.navigate_to("https://www.example.com")
    assert browser_manager.execute_script("console.log('test')") is True
    browser_manager.close_browser() 