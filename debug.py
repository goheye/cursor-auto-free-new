import os
import sys
from importlib.metadata import version, PackageNotFoundError
from src.main import CursorAutoFree
from src.logger import logger

def check_dependencies():
    """检查项目依赖是否已安装"""
    try:
        with open('requirements.txt', 'r', encoding='utf-8') as f:
            requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            
        for requirement in requirements:
            # 处理带版本号的依赖
            package = requirement.split('==')[0]
            # 跳过 poplib，因为它是标准库
            if package == 'poplib':
                continue
            try:
                version(package)
            except PackageNotFoundError:
                logger.error(f"缺少依赖: {requirement}")
                logger.info("请运行: pip install -r requirements.txt")
                return False
                
        return True
    except Exception as e:
        logger.error(f"检查依赖时出错: {str(e)}")
        return False

def main():
    try:
        # 检查依赖
        if not check_dependencies():
            return 1
            
        # 初始化 CursorAutoFree
        logger.info("初始化 CursorAutoFree...")
        cursor_free = CursorAutoFree()
        
        # 测试注册流程
        logger.info("开始测试注册流程...")
        result = cursor_free.register_cursor_account()
        
        # 输出结果
        if result["success"]:
            logger.info("注册成功！")
            logger.info(f"账号信息: {result['account_info']}")
        else:
            logger.error(f"注册失败: {result['error']}")
            
    except Exception as e:
        logger.error(f"调试过程中出错: {str(e)}")
        return 1
        
    return 0

if __name__ == "__main__":
    # 确保在虚拟环境中运行
    if not os.environ.get("VIRTUAL_ENV"):
        logger.error("请先激活虚拟环境！")
        sys.exit(1)
        
    # 运行主函数
    sys.exit(main()) 