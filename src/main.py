from .config import Config
from .logger import logger
from .machine_manager import MachineManager
from .email_manager import EmailManager
from .browser_manager import BrowserManager
from .account_generator import AccountGenerator
import psutil
import os
import time
import random
from typing import Optional, Dict
from selenium.webdriver.common.by import By

class CursorAutoFree:
    def __init__(self):
        self.logger = logger
        self.logger.info("初始化 CursorAutoFree...")
        
        # 初始化配置
        self.logger.info("加载配置文件...")
        self.config = Config()
        
        # 初始化各个管理器
        self.logger.info("初始化机器码管理器...")
        self.machine_manager = MachineManager()
        
        self.logger.info("初始化邮箱管理器...")
        self.email_manager = EmailManager(self.config)
        
        self.logger.info("初始化浏览器管理器...")
        self.browser_manager = BrowserManager(self.config)
        
        self.logger.info("初始化账号生成器...")
        self.account_generator = AccountGenerator()
        
        self.logger.info("初始化完成")
        
    def close_cursor_processes(self):
        """关闭所有Cursor进程"""
        try:
            self.logger.info("正在关闭所有Cursor进程...")
            for proc in psutil.process_iter(['name']):
                if proc.info['name'] and 'cursor' in proc.info['name'].lower():
                    try:
                        proc.kill()
                        self.logger.info(f"已关闭进程: {proc.info['name']}")
                    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                        pass
            self.logger.info("所有Cursor进程已关闭")
            return True
        except Exception as e:
            self.logger.error(f"关闭Cursor进程时出错: {str(e)}")
            return False
            
    def reset_machine_id(self) -> bool:
        """重置机器码"""
        try:
            return self.machine_manager.reset_machine_id()
        except Exception as e:
            self.logger.error(f"重置机器码时出错: {str(e)}")
            return False
            
    def handle_turnstile(self, tab) -> bool:
        """处理 Turnstile 验证"""
        try:
            self.logger.info("检测 Turnstile 验证...")
            
            # 更精确的验证框检测 - 只检测明确的Cloudflare验证框
            iframes = self.browser_manager.driver.find_elements(
                By.CSS_SELECTOR, 
                "iframe[src*='challenges.cloudflare.com']"
            )
            
            # 记录找到的iframe
            if iframes:
                self.logger.info(f"找到 {len(iframes)} 个验证框iframe")
                for i, iframe in enumerate(iframes):
                    src = iframe.get_attribute("src") or ""
                    self.logger.info(f"iframe {i+1}: src={src}")
                
                # 确认是否真的是验证框
                verification_confirmed = False
                for iframe in iframes:
                    src = iframe.get_attribute("src") or ""
                    # 确保是Cloudflare验证iframe
                    if "cloudflare" in src.lower() and "challenge" in src.lower():
                        verification_confirmed = True
                        break
                
                if not verification_confirmed:
                    self.logger.info("发现iframe但不是验证框，继续注册流程")
                    return True
                
                self.logger.info("确认发现验证框，开始处理...")
                
                # 尝试截取当前页面截图
                try:
                    screenshot_path = os.path.join(os.getcwd(), "verification_screenshot.png")
                    self.browser_manager.driver.save_screenshot(screenshot_path)
                    self.logger.info(f"已保存验证页面截图: {screenshot_path}")
                except Exception as e:
                    self.logger.warning(f"保存截图失败: {str(e)}")
                
                # 尝试处理每个验证框
                for i, iframe in enumerate(iframes):
                    try:
                        self.logger.info(f"处理第 {i+1} 个验证框...")
                        
                        # 切换到iframe
                        self.browser_manager.driver.switch_to.frame(iframe)
                        self.logger.info("已切换到验证框内部")
                        
                        # 检查iframe内部是否包含验证元素
                        validation_elements = self.browser_manager.driver.find_elements(
                            By.CSS_SELECTOR,
                            "div[class*='turnstile'], div[class*='cf-'], div[class*='challenge']"
                        )
                        
                        if not validation_elements:
                            self.logger.info("iframe内未找到验证元素，跳过此iframe")
                            self.browser_manager.driver.switch_to.default_content()
                            continue
                        
                        # 尝试点击验证元素
                        clicked = False
                        for elem in validation_elements:
                            if elem.is_displayed():
                                try:
                                    elem.click()
                                    self.logger.info("点击验证元素成功")
                                    clicked = True
                                    time.sleep(5)
                                    break
                                except Exception as e:
                                    self.logger.warning(f"点击验证元素失败: {str(e)}")
                        
                        if not clicked:
                            self.logger.info("未能点击任何验证元素")
                            
                        # 等待验证完成
                        for _ in range(5):
                            time.sleep(1)
                            # 检查是否有成功标志
                            success_elements = self.browser_manager.driver.find_elements(
                                By.CSS_SELECTOR,
                                "div[class*='success'], span[class*='success']"
                            )
                            if success_elements:
                                self.logger.info("验证成功完成")
                                break
                        
                    except Exception as e:
                        self.logger.warning(f"处理验证框时出错: {str(e)}")
                    finally:
                        # 切回主框架
                        self.browser_manager.driver.switch_to.default_content()
                
                # 额外等待时间，确保验证处理完成
                self.logger.info("验证处理完成，等待继续...")
                time.sleep(5)
                return True
            
            # 如果没有找到验证iframe，检查页面源码确认
            page_source = self.browser_manager.driver.page_source.lower()
            turnstile_indicators = [
                "cf-turnstile", 
                "cloudflare turnstile", 
                "cf-challenge"
            ]
            
            for indicator in turnstile_indicators:
                if indicator in page_source:
                    self.logger.info(f"页面源码中发现验证标识: {indicator}")
                    # 等待，让用户有机会手动处理验证
                    self.logger.info("等待可能的验证完成...")
                    time.sleep(10)
                    return True
            
            # 如果没有任何验证指标，确认没有验证
            self.logger.info("确认没有验证，继续注册流程")
            return True
                
        except Exception as e:
            self.logger.error(f"处理 Turnstile 验证时出错: {str(e)}")
            return False
            
    def get_session_token(self) -> Optional[str]:
        """获取会话令牌"""
        try:
            self.logger.info("获取会话令牌...")
            cookies = self.browser_manager.get_cookies()
            for cookie in cookies:
                if cookie.get("name") == "WorkosCursorSessionToken":
                    token = cookie["value"].split("%3A%3A")[1]
                    self.logger.info("成功获取会话令牌")
                    return token
            self.logger.error("未找到会话令牌")
            return None
        except Exception as e:
            self.logger.error(f"获取会话令牌时出错: {str(e)}")
            return None
            
    def check_and_handle_turnstile(self) -> bool:
        """检查是否出现验证并处理"""
        self.logger.info("检查是否出现验证...")
        try:
            time.sleep(5)  # 增加等待时间，确保验证框有足够时间加载
            result = self.handle_turnstile(None)
            time.sleep(3)  # 等待验证处理完成
            return result
        except Exception as e:
            self.logger.warning(f"处理验证时出现异常: {str(e)}，但继续注册流程")
            return True
            
    def register_cursor_account(self) -> Dict:
        """注册Cursor账号"""
        try:
            self.logger.info("开始注册Cursor账号")
            
            # 1. 生成随机账号信息
            account_info = self.account_generator.generate_account()
            self.logger.info(f"生成账号信息: {account_info}")
            
            # 2. 启动浏览器
            self.logger.info("启动浏览器...")
            if not self.browser_manager.start_browser():
                self.logger.error("启动浏览器失败")
                return {"success": False, "error": "启动浏览器失败"}
                
            try:
                # 3. 访问注册页面
                self.logger.info("访问注册页面...")
                sign_up_url = "https://authenticator.cursor.sh/sign-up"
                if not self.browser_manager.navigate_to(sign_up_url):
                    self.logger.error("访问注册页面失败")
                    return {"success": False, "error": "访问注册页面失败"}
                
                # 等待页面完全加载
                time.sleep(5)  # 增加等待时间
                
                # 检查初始页面加载后是否出现验证
                self.check_and_handle_turnstile()
                    
                # 4. 填写第一步表单（个人信息）
                self.logger.info("填写第一步个人信息...")
                
                # 填写名字
                self.logger.info("填写名字...")
                self.browser_manager.input_text("input[name='first_name']", account_info["first_name"])
                time.sleep(1)
                    
                # 填写姓氏
                self.logger.info("填写姓氏...")
                self.browser_manager.input_text("input[name='last_name']", account_info["last_name"])
                time.sleep(1)
                    
                # 填写邮箱
                self.logger.info("填写邮箱...")
                self.browser_manager.input_text("input[name='email']", account_info["email"])
                time.sleep(1)
                
                # 6. 点击Continue按钮
                self.logger.info("点击Continue按钮...")
                if not self.browser_manager.click_element("button[type='submit']"):
                    self.logger.error("点击Continue按钮失败")
                    return {"success": False, "error": "点击Continue按钮失败"}
                
                # 等待第二页加载
                self.logger.info("等待第二页(密码设置页)加载...")
                time.sleep(5)
                
                # 检查点击Continue后是否出现验证
                self.check_and_handle_turnstile()
                
                # 获取并显示当前页面源码，帮助诊断密码字段
                try:
                    page_source = self.browser_manager.driver.page_source
                    self.logger.info(f"当前页面URL: {self.browser_manager.driver.current_url}")
                    self.logger.info(f"页面标题: {self.browser_manager.driver.title}")
                    
                    # 尝试查找输入元素
                    inputs = self.browser_manager.driver.find_elements(By.TAG_NAME, "input")
                    self.logger.info(f"找到 {len(inputs)} 个输入元素:")
                    for i, input_elem in enumerate(inputs):
                        input_type = input_elem.get_attribute("type")
                        input_name = input_elem.get_attribute("name")
                        input_id = input_elem.get_attribute("id")
                        self.logger.info(f"输入元素 {i+1}: type={input_type}, name={input_name}, id={input_id}")
                except Exception as e:
                    self.logger.warning(f"获取页面信息失败: {str(e)}")
                
                # 7. 设置密码 (在第二步页面)
                self.logger.info("设置密码...")
                password_selectors = ["input[name='password']", "input[type='password']", "input#password"]
                password_set = False
                
                for selector in password_selectors:
                    try:
                        if self.browser_manager.input_text(selector, account_info["password"]):
                            self.logger.info(f"使用选择器 {selector} 成功设置密码")
                            password_set = True
                            break
                    except Exception as e:
                        self.logger.warning(f"使用选择器 {selector} 设置密码失败: {str(e)}")
                
                if not password_set:
                    # 尝试直接使用JavaScript设置密码
                    try:
                        self.logger.info("尝试使用JavaScript设置密码...")
                        js_result = self.browser_manager.driver.execute_script(
                            "var inputs = document.querySelectorAll('input[type=\"password\"]'); "
                            "if(inputs.length > 0) { inputs[0].value = arguments[0]; return true; } return false;", 
                            account_info["password"]
                        )
                        if js_result:
                            self.logger.info("使用JavaScript设置密码成功")
                            password_set = True
                        else:
                            self.logger.warning("没有找到密码输入框")
                    except Exception as e:
                        self.logger.error(f"使用JavaScript设置密码出错: {str(e)}")
                
                if not password_set:
                    self.logger.error("设置密码失败")
                    return {"success": False, "error": "设置密码失败"}
                
                # 点击注册页面2的提交按钮
                self.logger.info("点击第二页提交按钮...")
                if not self.browser_manager.click_element("button[type='submit']"):
                    self.logger.error("点击第二页提交按钮失败")
                    return {"success": False, "error": "点击第二页提交按钮失败"}
                
                # 等待验证邮件页面加载
                self.logger.info("等待验证邮件页面加载...")
                time.sleep(5)
                
                # 检查点击第二页提交按钮后是否出现验证
                self.check_and_handle_turnstile()
                
                # 等待验证邮件发送
                self.logger.info("等待验证邮件发送...")
                time.sleep(5)  # 给服务器足够时间发送验证邮件
                    
                # 8. 获取并输入验证码
                self.logger.info("获取验证码...")
                verification_code = self.email_manager.get_verification_code(account_info["email"])
                if not verification_code:
                    self.logger.error("获取验证码失败")
                    return {"success": False, "error": "获取验证码失败"}
                    
                self.logger.info(f"输入验证码: {verification_code}")
                for i, digit in enumerate(verification_code):
                    if not self.browser_manager.input_text(f"[data-index='{i}']", digit):
                        self.logger.error(f"输入验证码第{i+1}位失败")
                        return {"success": False, "error": f"输入验证码第{i+1}位失败"}
                    time.sleep(random.uniform(0.1, 0.3))
                
                # 点击验证按钮（如果有）
                verify_button_selectors = ["button[type='submit']", "button.submit", "button.verify"]
                for selector in verify_button_selectors:
                    try:
                        if self.browser_manager.click_element(selector):
                            self.logger.info(f"点击验证按钮成功: {selector}")
                            break
                    except Exception as e:
                        self.logger.warning(f"点击验证按钮失败: {str(e)}")
                
                # 检查点击验证按钮后是否出现验证
                self.check_and_handle_turnstile()
                    
                # 9. 等待注册完成
                self.logger.info("等待注册完成...")
                time.sleep(5)  # 增加等待时间
                
                # 检查是否注册成功（检查URL或特定元素）
                current_url = self.browser_manager.driver.current_url
                if "dashboard" in current_url or "home" in current_url:
                    self.logger.info(f"检测到成功页面: {current_url}")
                else:
                    self.logger.warning(f"未检测到成功页面，当前URL: {current_url}")
                    # 尝试继续，可能还是成功了
                
                # 10. 获取会话令牌
                session_token = self.get_session_token()
                if not session_token:
                    self.logger.warning("获取会话令牌失败，但继续保存账号信息")
                    # return {"success": False, "error": "获取会话令牌失败"}
                else:
                    account_info["session_token"] = session_token
                    
                # 11. 保存账号信息
                self.config.save_account(account_info)
                
                self.logger.info("账号注册成功")
                return {"success": True, "account_info": account_info}
                
            finally:
                # 确保浏览器被关闭
                self.logger.info("关闭浏览器...")
                self.browser_manager.stop_browser()
                
        except Exception as e:
            self.logger.error(f"注册账号时出错: {str(e)}")
            return {"success": False, "error": str(e)} 