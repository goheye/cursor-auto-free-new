from src.main import CursorAutoFree
import argparse

def main():
    parser = argparse.ArgumentParser(description='Cursor Auto Free 工具')
    parser.add_argument('--reset-machine', action='store_true', help='重置机器码')
    parser.add_argument('--register', action='store_true', help='注册新账号')
    args = parser.parse_args()

    app = CursorAutoFree()
    
    # 关闭所有Cursor进程
    app.close_cursor_processes()
    
    # 根据参数执行相应操作
    if args.reset_machine:
        print("正在重置机器码...")
        if app.reset_machine_id():
            print("机器码重置成功")
        else:
            print("机器码重置失败")
            
    if args.register:
        print("正在注册新账号...")
        if app.register_cursor_account():
            print("账号注册成功")
        else:
            print("账号注册失败")

if __name__ == "__main__":
    main() 