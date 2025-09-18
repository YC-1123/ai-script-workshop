# user_input/direct_edit.py

from user_input.branch_controller import InputRouter

class UserQueryHandler:
    """
    用户输入的处理协调器，结合输入路由模块
    """

    def __init__(self, director=None):
        self.router = InputRouter(director)

    def handle_user_input(self, raw_input: str) -> str:
        """
        基本指令格式：命令:角色:内容 或 命令:内容（全部角色）
        例如：切换情绪:玛尔博:愤怒 或 切换情绪:愤怒
        """
        if ":" not in raw_input:
            return "【系统】指令格式错误，应为 '命令:角色:内容' 或 '命令:内容'"
        
        parts = raw_input.split(":", 2)
        if len(parts) == 3:
            # 指定角色：命令:角色:内容
            command, character, content = [p.strip() for p in parts]
            return self.router.route(command, content, character)
        elif len(parts) == 2:
            # 全部角色：命令:内容
            command, content = [p.strip() for p in parts]
            return self.router.route(command, content, None)
        else:
            return "【系统】指令格式错误"
            