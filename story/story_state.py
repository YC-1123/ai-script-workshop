# story/story_state.py

class StoryState:
    """
    剧情状态机，负责记录当前阶段与推进状态。
    """

    def __init__(self):
        self.phase = self.phases = ["初步调查询问", "深入审讯对质", "最终真相揭露"]
        self.current_index = 0
        self.flags = {
            "初步调查询问已触发": False,
            "深入审讯对质已建立": False,
            "最终真相揭露已建立": False,
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