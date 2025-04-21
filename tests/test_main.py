import pytest
from unittest.mock import Mock, patch
import psutil
from src.main import CursorAutoFree

class TestCursorAutoFree:
    @pytest.fixture
    def cursor_auto_free(self):
        """创建测试用的 CursorAutoFree 实例"""
        with patch('src.main.Config') as mock_config, \
             patch('src.main.MachineManager') as mock_machine_manager, \
             patch('src.main.EmailManager') as mock_email_manager, \
             patch('src.main.BrowserManager') as mock_browser_manager:
            
            # 设置模拟对象的返回值
            mock_config.return_value.domain = "test.com"
            mock_config.return_value.temp_mail = "test@test.com"
            
            # 创建测试实例
            instance = CursorAutoFree()
            
            # 保存模拟对象以便后续使用
            instance.mock_config = mock_config
            instance.mock_machine_manager = mock_machine_manager
            instance.mock_email_manager = mock_email_manager
            instance.mock_browser_manager = mock_browser_manager
            
            return instance

    def test_init(self, cursor_auto_free):
        """测试初始化过程"""
        # 验证各个管理器是否被正确初始化
        assert cursor_auto_free.config is not None
        assert cursor_auto_free.machine_manager is not None
        assert cursor_auto_free.email_manager is not None
        assert cursor_auto_free.browser_manager is not None

    @patch('psutil.process_iter')
    def test_close_cursor_processes_success(self, mock_process_iter, cursor_auto_free):
        """测试成功关闭Cursor进程"""
        # 模拟进程列表
        mock_process = Mock()
        mock_process.info = {'name': 'cursor.exe'}
        mock_process_iter.return_value = [mock_process]
        
        # 执行测试
        result = cursor_auto_free.close_cursor_processes()
        
        # 验证结果
        assert result is True
        mock_process.kill.assert_called_once()

    @patch('psutil.process_iter')
    def test_close_cursor_processes_failure(self, mock_process_iter, cursor_auto_free):
        """测试关闭Cursor进程失败的情况"""
        # 模拟进程迭代器抛出异常
        mock_process_iter.side_effect = Exception("测试异常")
        
        # 执行测试
        result = cursor_auto_free.close_cursor_processes()
        
        # 验证结果
        assert result is False

    def test_reset_machine_id_success(self, cursor_auto_free):
        """测试成功重置机器码"""
        # 设置模拟返回值
        cursor_auto_free.machine_manager.reset_machine_id.return_value = True
        
        # 执行测试
        result = cursor_auto_free.reset_machine_id()
        
        # 验证结果
        assert result is True
        cursor_auto_free.machine_manager.reset_machine_id.assert_called_once()

    def test_reset_machine_id_failure(self, cursor_auto_free):
        """测试重置机器码失败的情况"""
        # 设置模拟抛出异常
        cursor_auto_free.machine_manager.reset_machine_id.side_effect = Exception("测试异常")
        
        # 执行测试
        result = cursor_auto_free.reset_machine_id()
        
        # 验证结果
        assert result is False

    def test_register_cursor_account_success(self, cursor_auto_free):
        """测试成功注册账号的完整流程"""
        # 设置浏览器管理器的模拟返回值
        cursor_auto_free.browser_manager.start_browser.return_value = True
        cursor_auto_free.browser_manager.navigate_to.return_value = True
        cursor_auto_free.browser_manager.wait_for_element.return_value = True
        cursor_auto_free.browser_manager.click_element.return_value = True
        cursor_auto_free.browser_manager.input_text.return_value = True
        
        # 设置邮箱管理器的模拟返回值
        cursor_auto_free.email_manager.get_verification_code.return_value = "123456"
        
        # 执行测试
        result = cursor_auto_free.register_cursor_account()
        
        # 验证结果
        assert result is True
        cursor_auto_free.browser_manager.start_browser.assert_called_once()
        cursor_auto_free.browser_manager.close_browser.assert_called_once()

    def test_register_cursor_account_browser_failure(self, cursor_auto_free):
        """测试浏览器启动失败的情况"""
        # 设置浏览器启动失败
        cursor_auto_free.browser_manager.start_browser.return_value = False
        
        # 执行测试
        result = cursor_auto_free.register_cursor_account()
        
        # 验证结果
        assert result is False
        cursor_auto_free.browser_manager.close_browser.assert_called_once()

    def test_register_cursor_account_navigation_failure(self, cursor_auto_free):
        """测试网站导航失败的情况"""
        # 设置浏览器启动成功但导航失败
        cursor_auto_free.browser_manager.start_browser.return_value = True
        cursor_auto_free.browser_manager.navigate_to.return_value = False
        
        # 执行测试
        result = cursor_auto_free.register_cursor_account()
        
        # 验证结果
        assert result is False
        cursor_auto_free.browser_manager.close_browser.assert_called_once()

    def test_register_cursor_account_verification_failure(self, cursor_auto_free):
        """测试验证码获取失败的情况"""
        # 设置浏览器操作成功但验证码获取失败
        cursor_auto_free.browser_manager.start_browser.return_value = True
        cursor_auto_free.browser_manager.navigate_to.return_value = True
        cursor_auto_free.browser_manager.wait_for_element.return_value = True
        cursor_auto_free.browser_manager.click_element.return_value = True
        cursor_auto_free.browser_manager.input_text.return_value = True
        cursor_auto_free.email_manager.get_verification_code.return_value = None
        
        # 执行测试
        result = cursor_auto_free.register_cursor_account()
        
        # 验证结果
        assert result is False
        cursor_auto_free.browser_manager.close_browser.assert_called_once() 