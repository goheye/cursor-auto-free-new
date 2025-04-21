from typing import List, Dict, Any, Optional
import os
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from src.config import Config
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class BrowserManager:
    def __init__(self, config: Optional[Config] = None):
        self.config = config if config is not None else Config()
        self.driver: Optional[webdriver.Chrome] = None
        self.logger = logging.getLogger(__name__)
        
    def start_browser(self) -> bool:
        """启动浏览器"""
        if self.driver:
            self.logger.warning("浏览器已经启动")
            return True
            
        browser_config = self.config.get_browser_config()
        options = Options()
        
        # 设置用户代理
        if browser_config['user_agent']:
            options.add_argument(f'user-agent={browser_config["user_agent"]}')
            
        # 设置无头模式
        if browser_config['headless']:
            options.add_argument('--headless')
            
        # 设置代理
        if browser_config['proxy']:
            options.add_argument(f'--proxy-server={browser_config["proxy"]}')
            
        # 添加扩展
        if browser_config['extensions']:
            for ext_path in browser_config['extensions']:
                if os.path.exists(ext_path):
                    options.add_extension(ext_path)
                    self.logger.info(f"已添加扩展: {ext_path}")
                else:
                    self.logger.warning(f"扩展路径不存在: {ext_path}")
                    
        # 设置浏览器路径
        if browser_config['path']:
            options.binary_location = browser_config['path']
            
        # 添加其他必要的选项
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        options.add_argument('--allow-insecure-localhost')
        options.add_argument('--disable-web-security')
        options.add_argument('--disable-features=IsolateOrigins,site-per-process')
        options.add_argument('--enable-unsafe-swiftshader')
        options.add_argument('--disable-software-rasterizer')
        options.add_argument('--disable-setuid-sandbox')
        
        # 设置常规首选项
        options.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option('detach', False)
        
        # 设置页面加载策略
        options.page_load_strategy = 'normal'
        
        # 尝试多次启动浏览器
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                self.logger.info(f"尝试启动浏览器 (尝试 {attempt+1}/{max_attempts})...")
                # 使用本地已安装的ChromeDriver
                # service = Service(ChromeDriverManager().install())
                # 或者使用固定路径的ChromeDriver
                driver_path = os.path.join(os.getcwd(), 'chromedriver.exe')
                if not os.path.exists(driver_path):
                    self.logger.info("未找到本地ChromeDriver，尝试自动下载...")
                    service = Service(ChromeDriverManager().install())
                else:
                    self.logger.info(f"使用本地ChromeDriver: {driver_path}")
                    service = Service(driver_path)
                
                self.driver = webdriver.Chrome(service=service, options=options)
                self.logger.info("浏览器启动成功")
                return True
            except Exception as e:
                self.logger.error(f"浏览器启动失败 (尝试 {attempt+1}), 详细错误: {str(e)}")
                if attempt < max_attempts - 1:
                    self.logger.info(f"等待 3 秒后重试...")
                    time.sleep(3)
                else:
                    self.logger.error(f"浏览器启动失败，已达最大尝试次数")
                    return False
            
    def stop_browser(self) -> None:
        """停止浏览器"""
        if self.driver:
            try:
                self.driver.quit()
                self.driver = None
                self.logger.info("浏览器已关闭")
            except Exception as e:
                self.logger.error(f"关闭浏览器时出错: {str(e)}")
                
    def get_driver(self) -> Optional[webdriver.Chrome]:
        """获取浏览器驱动"""
        return self.driver

    def navigate_to(self, url: str) -> bool:
        """导航到指定URL"""
        try:
            if not self.driver:
                if not self.start_browser():
                    return False
                    
            self.driver.get(url)
            self.logger.info(f"成功导航到: {url}")
            return True
            
        except Exception as e:
            self.logger.error(f"导航失败: {str(e)}")
            return False
            
    def wait_for_element(self, selector: str, timeout: int = 10) -> bool:
        """等待元素出现"""
        try:
            if not self.driver:
                return False
                
            element = self.driver.find_element(By.CSS_SELECTOR, selector)
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
            if not self.driver:
                return False
                
            # 等待元素出现
            element = self.driver.find_element(By.CSS_SELECTOR, selector)
            if not element:
                self.logger.warning(f"未找到元素: {selector}")
                return False
                
            # 等待元素可交互
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
            
            # 点击元素
            element.click()
            self.logger.info(f"成功点击元素: {selector}")
            return True
                
        except Exception as e:
            self.logger.error(f"点击元素失败: {str(e)}")
            return False
            
    def input_text(self, selector: str, text: str) -> bool:
        """输入文本"""
        try:
            if not self.driver:
                return False
                
            element = self.driver.find_element(By.CSS_SELECTOR, selector)
            if element:
                element.send_keys(text)
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
            if not self.driver:
                return None
                
            element = self.driver.find_element(By.CSS_SELECTOR, selector)
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
            
    def execute_script(self, script: str) -> Any:
        """执行JavaScript脚本"""
        try:
            if not self.driver:
                return None
                
            result = self.driver.execute_script(script)
            self.logger.info("成功执行脚本")
            return result
            
        except Exception as e:
            self.logger.error(f"执行脚本失败: {str(e)}")
            return None
            
    def get_cookies(self) -> List[Dict[str, Any]]:
        """获取所有 cookies"""
        try:
            if not self.driver:
                return []
                
            cookies = self.driver.get_cookies()
            return cookies
            
        except Exception as e:
            self.logger.error(f"获取 cookies 失败: {str(e)}")
            return []

    def wait_for_turnstile(self) -> bool:
        """等待Turnstile验证框出现"""
        try:
            self.logger.info("开始等待Turnstile验证框...")
            
            # 等待页面完全加载
            WebDriverWait(self.driver, 20).until(
                lambda driver: driver.execute_script('return document.readyState') == 'complete'
            )
            self.logger.info("页面加载完成")
            
            # 等待一段时间，让验证框有机会加载
            time.sleep(5)
            
            # 检查是否存在验证框
            iframes = self.driver.find_elements(By.CSS_SELECTOR, "iframe[src*='challenges.cloudflare.com']")
            if not iframes:
                self.logger.info("未检测到Turnstile验证框，可能不需要验证")
                return True
                
            self.logger.info(f"检测到 {len(iframes)} 个验证框")
            
            # 遍历所有验证框
            for iframe in iframes:
                try:
                    self.driver.switch_to.frame(iframe)
                    self.logger.info("已切换到验证框")
                    
                    # 等待验证按钮出现
                    button = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "div[class*='challenge-container']"))
                    )
                    
                    if button.is_displayed() and button.is_enabled():
                        self.logger.info("验证按钮可见且可点击")
                        return True
                    else:
                        self.logger.warning("验证按钮不可见或不可点击")
                        
                except Exception as e:
                    self.logger.warning(f"处理验证框时出错: {str(e)}")
                finally:
                    self.driver.switch_to.default_content()
                    
            self.logger.warning("未找到可用的验证按钮")
            return False
            
        except Exception as e:
            self.logger.error(f"等待Turnstile验证框失败: {str(e)}")
            return False
            
    def handle_registration(self, account_info: dict) -> bool:
        """处理注册流程"""
        try:
            # 等待页面加载
            WebDriverWait(self.driver, 20).until(
                lambda driver: driver.execute_script('return document.readyState') == 'complete'
            )
            self.logger.info("注册页面加载完成")
            
            # 填写表单
            self.logger.info("填写注册表单...")
            time.sleep(2)  # 等待表单元素完全加载
            
            # 填写各个字段
            self.input_text('input[name="firstName"]', account_info['first_name'])
            time.sleep(1)
            self.input_text('input[name="lastName"]', account_info['last_name'])
            time.sleep(1)
            self.input_text('input[name="email"]', account_info['email'])
            time.sleep(1)
            self.input_text('input[name="password"]', account_info['password'])
            time.sleep(2)
            
            # 检查是否存在验证框
            iframes = self.driver.find_elements(By.CSS_SELECTOR, "iframe[src*='challenges.cloudflare.com']")
            if iframes:
                self.logger.info("检测到验证框，等待验证完成...")
                time.sleep(10)  # 给足够的时间完成验证
            else:
                self.logger.info("未检测到验证框，直接继续注册流程")
            
            # 点击注册按钮
            self.click_element('button[type="submit"]')
            time.sleep(5)  # 等待注册请求完成
            
            return True
            
        except Exception as e:
            self.logger.error(f"注册过程出错: {str(e)}")
            return False 