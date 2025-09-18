# user_input/branch_controller.py

class InputRouter:
    """
    将用户输入指令映射为具体分支行为
    """

    def __init__(self, director=None):
        self.director = director
        self.valid_commands = {
            "切换情绪": self.route_emotion_switch,
            "注入线索": self.route_clues_injection,
            "查看状态": self.route_status_view,
            "跳过阶段": self.route_skip_phase,
        }
    
    def _find_character(self, character: str):
        """查找匹配的角色名称"""
        if not self.director:
            return None
            
        # 首先尝试精确匹配
        if character in self.director.contexts:
            return character
            
        # 然后尝试部分匹配
        for name in self.director.contexts.keys():
            if character in name or name in character:
                return name
        return None
    
    def route(self, command: str, content: str, character: str = None) -> str:
        for keyword, handler in self.valid_commands.items():
            if keyword == command:  # 精确匹配而不是startswith
                return handler(content, character)
        return f"【系统】未知指令 '{command}'，可用指令：" + "、".join(self.valid_commands.keys())
    
    def route_emotion_switch(self, emotion: str, character: str = None) -> str:
        if self.director:
            if character:
                matched_char = self._find_character(character)
                if matched_char:
                    self.director.contexts[matched_char].set_emotion(emotion)
                    return f"【系统】{matched_char}的情绪已替换为：{emotion}"
                else:
                    available = "、".join(self.director.contexts.keys())
                    return f"【系统】角色 '{character}' 不存在，可用角色：{available}"
            else:
                # 所有角色
                for name, context in self.director.contexts.items():
                    context.set_emotion(emotion)
                return f"【系统】所有角色情绪已替换为：{emotion}"
        return f"【系统】角色情绪已设定为：{emotion}"
    
    def route_clues_injection(self, clues: str, character: str = None) -> str:
        if self.director:
            if character:
                matched_char = self._find_character(character)
                if matched_char:
                    self.director.contexts[matched_char].set_clues(clues)
                    return f"【系统】{matched_char}的线索已替换为：{clues}"
                else:
                    available = "、".join(self.director.contexts.keys())
                    return f"【系统】角色 '{character}' 不存在，可用角色：{available}"
            else:
                # 所有角色
                for name, context in self.director.contexts.items():
                    context.set_clues(clues)
                return f"【系统】所有角色线索已替换为：{clues}"
        return f"【系统】已注入新线索：{clues}"

    def route_status_view(self, _: str, character: str = None) -> str:
        if self.director:
            current_phase = self.director.story_state.get_current_phase()
            if character:
                # 调试信息
                available_chars = list(self.director.contexts.keys())
                matched_char = self._find_character(character)
                
                if matched_char:
                    ctx = self.director.contexts[matched_char]
                    return f"【系统】{matched_char} - 情绪:{ctx.profile.emotion}, 线索:{ctx.profile.clues}"
                else:
                    return f"【系统】角色 '{character}' 不存在，可用角色：{', '.join(available_chars)}"
            else:
                # 查看所有角色状态
                status_info = [f"阶段:{current_phase}"]
                for name, ctx in self.director.contexts.items():
                    status_info.append(f"{name}(情绪:{ctx.profile.emotion})")
                return f"【系统】当前状态 - " + ", ".join(status_info)
        return "【系统】当前状态：阶段-相遇，情绪-平静，角色-艾琳、诺亚"
    
    def route_skip_phase(self, _: str, character: str = None) -> str:
        if self.director:
            self.director.advance_phase()
            return "【系统】已跳过当前阶段"
        return "【系统】跳过阶段功能暂不可用"
