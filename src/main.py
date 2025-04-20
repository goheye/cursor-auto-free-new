from .config import Config
from .logger import logger
from .machine_manager import MachineManager
from .email_manager import EmailManager
from .browser_manager import BrowserManager

class CursorAutoFree:
    def __init__(self):
        self.config = Config()
        self.logger = logger
        self.machine_manager = MachineManager()
        self.email_manager = EmailManager(self.config)
        self.browser_manager = BrowserManager(self.config)
        
    def run(self) -> bool:
        """运行主程序"""
        try:
            self.logger.info("开始运行程序")
            
            # 1. 获取机器码
            machine_id = self.machine_manager.get_machine_id()
            if not machine_id:
                self.logger.error("获取机器码失败")
                return False
                
            # 2. 启动浏览器
            if not self.browser_manager.start_browser():
                self.logger.error("启动浏览器失败")
                return False
                
            try:
                # 3. 访问 Cursor 网站
                domain = self.config.domain.strip().strip("'").strip('"')  # 确保移除所有引号
                if not self.browser_manager.navigate_to(f"https://{domain}"):
                    self.logger.error("访问网站失败")
                    return False
                    
                # 4. 等待并点击注册按钮
                if not self.browser_manager.wait_for_element("#register-button"):
                    self.logger.error("未找到注册按钮")
                    return False
                if not self.browser_manager.click_element("#register-button"):
                    self.logger.error("点击注册按钮失败")
                    return False
                    
                # 5. 输入邮箱
                if not self.browser_manager.wait_for_element("#email-input"):
                    self.logger.error("未找到邮箱输入框")
                    return False
                if not self.browser_manager.input_text("#email-input", self.config.temp_mail):
                    self.logger.error("输入邮箱失败")
                    return False
                    
                # 6. 点击发送验证码
                if not self.browser_manager.click_element("#send-code-button"):
                    self.logger.error("点击发送验证码按钮失败")
                    return False
                    
                # 7. 获取验证码
                verification_code = self.email_manager.get_verification_code()
                if not verification_code:
                    self.logger.error("获取验证码失败")
                    return False
                    
                # 8. 输入验证码
                if not self.browser_manager.wait_for_element("#verification-code-input"):
                    self.logger.error("未找到验证码输入框")
                    return False
                if not self.browser_manager.input_text("#verification-code-input", verification_code):
                    self.logger.error("输入验证码失败")
                    return False
                    
                # 9. 点击注册完成
                if not self.browser_manager.click_element("#submit-button"):
                    self.logger.error("点击注册完成按钮失败")
                    return False
                    
                # 10. 等待注册成功
                if not self.browser_manager.wait_for_element(".success-message"):
                    self.logger.error("注册失败")
                    return False
                    
                self.logger.info("注册成功")
                return True
                
            finally:
                # 确保浏览器被关闭
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