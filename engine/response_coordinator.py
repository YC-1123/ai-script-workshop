# engine/response_coordinator.py

class ResponseCoordinator:
    """
    控制多角色轮流响应逻辑
    """

    def __init__(self, character_list):
        self.characters = character_list
        self.current_index = 0
    
    def next_character(self) -> str:
        """
        轮询下一个角色
        """
        name = self.characters[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.characters)
        return name
    
    def reset(self):
        self.current_index = 0