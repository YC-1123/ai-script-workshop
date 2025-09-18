def safe_input(prompt="", retry_message="【系统】输入编码错误，请重新输入"):
    """安全的输入函数，处理编码错误并支持重新输入"""
    while True:
        try:
            return input(prompt).strip()
        except UnicodeDecodeError:
            print(retry_message)
        except KeyboardInterrupt:
            print("\n【系统】用户中断操作")
            raise
        except EOFError:
            print("\n【系统】输入结束")
            return ""
