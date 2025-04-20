from .config import Config
from .logger import logger
from .machine_manager import MachineManager
from .email_manager import EmailManager
from .browser_manager import BrowserManager

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
        
        self.logger.info("初始化完成")
        
        self.keep_alive_interval = 3600  # 保活间隔，默认1小时
        
    def run(self) -> bool:
        """运行主程序"""
        try:
            self.logger.info("开始运行程序")
            
            # 1. 获取机器码
            self.logger.info("步骤1: 获取机器码...")
            machine_id = self.machine_manager.get_machine_id()
            if not machine_id:
                self.logger.error("获取机器码失败")
                return False
            self.logger.info(f"获取机器码成功: {machine_id}")
                
            # 2. 启动浏览器
            self.logger.info("步骤2: 启动浏览器...")
            if not self.browser_manager.start_browser():
                self.logger.error("启动浏览器失败")
                return False
            self.logger.info("浏览器启动成功")
                
            try:
                # 3. 访问 Cursor 网站
                self.logger.info("步骤3: 访问 Cursor 网站...")
                domain = self.config.domain.strip().strip("'").strip('"')
                url = f"https://{domain}"
                self.logger.info(f"访问URL: {url}")
                
                if not self.browser_manager.navigate_to(url):
                    self.logger.error("访问网站失败")
                    return False
                self.logger.info("网站访问成功")
                    
                # 4. 等待并点击注册按钮
                self.logger.info("步骤4: 查找注册按钮...")
                if not self.browser_manager.wait_for_element("#register-button"):
                    self.logger.error("未找到注册按钮")
                    return False
                    
                self.logger.info("点击注册按钮...")
                if not self.browser_manager.click_element("#register-button"):
                    self.logger.error("点击注册按钮失败")
                    return False
                self.logger.info("注册按钮点击成功")
                    
                # 5. 输入邮箱
                self.logger.info("步骤5: 输入邮箱...")
                if not self.browser_manager.wait_for_element("#email-input"):
                    self.logger.error("未找到邮箱输入框")
                    return False
                    
                email = self.config.temp_mail
                self.logger.info(f"输入邮箱: {email}")
                if not self.browser_manager.input_text("#email-input", email):
                    self.logger.error("输入邮箱失败")
                    return False
                self.logger.info("邮箱输入成功")
                    
                # 6. 点击发送验证码
                self.logger.info("步骤6: 发送验证码...")
                if not self.browser_manager.click_element("#send-code-button"):
                    self.logger.error("点击发送验证码按钮失败")
                    return False
                self.logger.info("验证码发送成功")
                    
                # 7. 获取验证码
                self.logger.info("步骤7: 获取验证码...")
                verification_code = self.email_manager.get_verification_code()
                if not verification_code:
                    self.logger.error("获取验证码失败")
                    return False
                self.logger.info(f"获取验证码成功: {verification_code}")
                    
                # 8. 输入验证码
                self.logger.info("步骤8: 输入验证码...")
                if not self.browser_manager.wait_for_element("#verification-code-input"):
                    self.logger.error("未找到验证码输入框")
                    return False
                    
                self.logger.info(f"输入验证码: {verification_code}")
                if not self.browser_manager.input_text("#verification-code-input", verification_code):
                    self.logger.error("输入验证码失败")
                    return False
                self.logger.info("验证码输入成功")
                    
                # 9. 点击注册完成
                self.logger.info("步骤9: 完成注册...")
                if not self.browser_manager.click_element("#submit-button"):
                    self.logger.error("点击注册完成按钮失败")
                    return False
                self.logger.info("注册完成按钮点击成功")
                    
                # 10. 等待注册成功
                self.logger.info("步骤10: 等待注册成功...")
                if not self.browser_manager.wait_for_element(".success-message"):
                    self.logger.error("注册失败")
                    return False
                self.logger.info("注册成功")
                    
                return True
                
            finally:
                # 确保浏览器被关闭
                self.logger.info("关闭浏览器...")
                self.browser_manager.close_browser()
                
        except Exception as e:
            self.logger.error(f"运行程序时出错: {str(e)}")
            return False
            
    def reset_machine_id(self) -> bool:
        """重置机器码"""
        try:
            return self.machine_manager.reset_machine_id()
        except Exception as e:
            self.logger.error(f"重置机器码时出错: {str(e)}")
            return False
            
    def patch_machine_id(self, patch: str) -> bool:
        """应用机器码补丁"""
        try:
            return self.machine_manager.patch_machine_id(patch)
        except Exception as e:
            self.logger.error(f"应用机器码补丁时出错: {str(e)}")
            return False
            
    def verify_machine_id(self, machine_id: str) -> bool:
        """验证机器码"""
        try:
            return self.machine_manager.verify_machine_id(machine_id)
        except Exception as e:
            self.logger.error(f"验证机器码时出错: {str(e)}")
            return False
            
    def keep_alive(self):
        """保活功能"""
        try:
            # 1. 获取会话令牌
            session_token = self.get_session_token()
            if not session_token:
                self.logger.warning("获取会话令牌失败，尝试重新登录")
                return False
                
            # 2. 更新认证信息
            if not self.update_auth():
                self.logger.warning("更新认证信息失败")
                return False
                
            # 3. 检查账号状态
            if not self.check_account_status():
                self.logger.warning("账号状态异常")
                return False
                
            self.logger.info("保活成功")
            return True
            
        except Exception as e:
            self.logger.error(f"保活失败: {str(e)}")
            return False
            
    def start_keep_alive(self):
        """启动保活定时任务"""
        import threading
        import time
        
        def keep_alive_loop():
            while True:
                self.keep_alive()
                time.sleep(self.keep_alive_interval)
                
        # 启动保活线程
        self.keep_alive_thread = threading.Thread(target=keep_alive_loop, daemon=True)
        self.keep_alive_thread.start()
        self.logger.info("保活定时任务已启动") 