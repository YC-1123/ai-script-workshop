# story/story_state.py

class StoryState:
    """
    剧情状态机，负责记录当前阶段与推进状态。
    """

    def __init__(self):
        self.phase = ["与玛尔博的对话", "获取第一轮线索" ,"与赛布尔的对话", "获取第二轮线索", "与阿祖尔的对话", "获取第三轮线索", "推理凶手"]
        self.current_index = 0
        self.flags = {
            "获取第一轮线索已触发": False,
            "与赛布尔的对话已建立": False,
            "获取第二轮线索已建立": False,
            "与阿祖尔的对话已建立": False,
            "获取第三轮线索已建立": False,
            "推理凶手已建立": False,
        }

    def get_current_phase(self) -> str:
        return self.phase[self.current_index]

    def advance_phase(self):
        if self.current_index < len(self.phases) - 1:
            self.current_index += 1
    
    def set_flag(self, key:str, value: bool = True):
        self.flags[key] = value

    def get_flag(self, key:str) -> bool:
        return self.flags.get(key, False)
    
    def reset(self):
        self.current_index = 0
        for key in self.flags:
            self.flags[key] = False