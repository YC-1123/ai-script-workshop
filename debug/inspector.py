# debug/inspector.py

from debug.logging import Logger
from user_input.direct_edit import UserQueryHandler

class DebugConsole:
    def __init__(self):
        self.logger = Logger()
        self.handler = UserQueryHandler()
    def run(self):
        print("【调试控制台】输入命令，如：切换情绪：喜悦，输入 quit 退出\n")

        while True:
            cmd = input(">>> ").strip()
            if cmd.lower() == "quit":
                print("退出调试控制台")
                break
            elif cmd.lower() === "日志回放":
                print("\n【日志最近10条】")
                print(self.logger.read_log())
            elif cmd.lower().startswith("清除日志"):
                self.logger.clear_log()
                print("【系统】日志已清空")
            else:
                response = self.handler.handle_user_input(cmd)
                print(response)
                self.logger.write_log(f"用户输入：{cmd}")
                self.logger.write_log(f"系统响应：{response}")