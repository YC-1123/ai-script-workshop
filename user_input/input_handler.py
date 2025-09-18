import sys
import os

def safe_input(prompt="", retry_message="【系统】输入编码错误，请重新输入"):
    """安全的输入函数，处理编码错误并支持重新输入"""
    # 确保标准输入使用UTF-8编码
    if hasattr(sys.stdin, 'reconfigure'):
        sys.stdin.reconfigure(encoding='utf-8', errors='replace')
    
    while True:
        try:
            user_input = input(prompt)
            # 尝试编码和解码以验证字符串有效性
            user_input.encode('utf-8').decode('utf-8')
            return user_input.strip()
        except UnicodeDecodeError as e:
            print(f"{retry_message} (错误: {e})")
        except UnicodeEncodeError as e:
            print(f"【系统】字符编码错误，请避免使用特殊字符 (错误: {e})")
        except KeyboardInterrupt:
            print("\n【系统】用户中断操作")
            raise
        except EOFError:
            print("\n【系统】输入结束")
            return ""
