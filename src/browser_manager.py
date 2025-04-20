from DrissionPage import ChromiumPage, ChromiumOptions
from typing import Optional, Dict, Any
from src.logger import logger
import time

class BrowserManager:
    def __init__(self, config: Any):
        self.config = config
        self.logger = logger
        self.page = None
        
    def start_browser(self) -> bool:
        """启动浏览器"""
        try:
            browser_config = self.config.get_browser_config()
            
            # 创建浏览器选项
            options = ChromiumOptions()
            if browser_config['user_agent']:
                options.set_argument(f'--user-agent={browser_config["user_agent"]}')
            if browser_config['headless']:
                options.set_argument('--headless')
            if browser_config['path']:
                options.set_browser_path(browser_config['path'])
            
            # 创建浏览器实例
            self.page = ChromiumPage(options)
            
            self.logger.info("浏览器启动成功")
            return True
            
        except Exception as e:
            self.logger.error(f"浏览器启动失败: {str(e)}")
            return False
            
    def close_browser(self) -> None:
        """关闭浏览器"""
        try:
            if self.page:
                self.page.quit()
                self.page = None
            self.logger.info("浏览器已关闭")
        except Exception as e:
            self.logger.error(f"关闭浏览器失败: {str(e)}")
            
    def navigate_to(self, url: str) -> bool:
        """导航到指定URL"""
        try:
            if not self.page:
                if not self.start_browser():
                    return False
                    
            self.page.get(url)
            self.logger.info(f"成功导航到: {url}")
            return True
            
        except Exception as e:
            self.logger.error(f"导航失败: {str(e)}")
            return False
            
    def wait_for_element(self, selector: str, timeout: int = 10) -> bool:
        """等待元素出现"""
        try:
            if not self.page:
                return False
                
            element = self.page.ele(selector, timeout=timeout)
            if element:
                self.logger.info(f"元素已出现: {selector}")
                return True
            else:
                self.logger.warning(f"等待元素超时: {selector}")
                return False
                
        except Exception as e:
            self.logger.error(f"等待元素失败: {str(e)}")
            return False
            
    def click_element(self, selector: str) -> bool:
        """点击元素"""
        try:
            if not self.page:
                return False
                
            element = self.page.ele(selector)
            if element:
                element.click()
                self.logger.info(f"成功点击元素: {selector}")
                return True
            else:
                self.logger.warning(f"未找到元素: {selector}")
                return False
                
        except Exception as e:
            self.logger.error(f"点击元素失败: {str(e)}")
            return False
            
    def input_text(self, selector: str, text: str) -> bool:
        """输入文本"""
        try:
            if not self.page:
                return False
                
            element = self.page.ele(selector)
            if element:
                element.input(text)
                self.logger.info(f"成功输入文本: {text}")
                return True
            else:
                self.logger.warning(f"未找到元素: {selector}")
                return False
                
        except Exception as e:
            self.logger.error(f"输入文本失败: {str(e)}")
            return False
            
    def get_text(self, selector: str) -> Optional[str]:
        """获取元素文本"""
        try:
            if not self.page:
                return None
                
            element = self.page.ele(selector)
            if element:
                text = element.text
                self.logger.info(f"成功获取文本: {text}")
                return text
            else:
                self.logger.warning(f"未找到元素: {selector}")
                return None
                
        except Exception as e:
            self.logger.error(f"获取文本失败: {str(e)}")
            return None
            
    def execute_script(self, script: str) -> bool:
        """执行JavaScript脚本"""
        try:
            if not self.page:
                return False
                
            self.page.run_js(script)
            self.logger.info("成功执行脚本")
            return True
            
        except Exception as e:
            self.logger.error(f"执行脚本失败: {str(e)}")
            return False 