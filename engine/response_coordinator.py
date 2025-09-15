# engine/response_coordinator.py

class ResponseCoordinator:
    """
    控制多角色轮流响应逻辑，支持奎因侦探与其他角色的一对一对话
    """

    def __init__(self, character_list):
        self.characters = character_list
        self.detective = "奎因侦探"
        self.suspects = [char for char in character_list if char != self.detective]
        self.current_suspect_index = 0
        self.conversation_round = 0
    
    def get_conversation_pair(self) -> tuple:
        """
        获取当前对话的角色对：奎因侦探 + 当前嫌疑人
        """
        if self.current_suspect_index < len(self.suspects):
            suspect = self.suspects[self.current_suspect_index]
            return (self.detective, suspect)
        return None
    
    def next_speaker(self) -> str:
        """
        在当前对话对中轮换发言者
        """
        pair = self.get_conversation_pair()
        if not pair:
            return None
        
        # 奇数轮奎因侦探先说，偶数轮嫌疑人先说
        if self.conversation_round % 2 == 0:
            return pair[0]  # 奎因侦探
        else:
            return pair[1]  # 当前嫌疑人
    
    def advance_conversation(self):
        """
        推进对话轮次
        """
        self.conversation_round += 1
    
    def next_suspect(self):
        """
        切换到下一个嫌疑人
        """
        self.current_suspect_index += 1
        self.conversation_round = 0
    
    def has_more_suspects(self) -> bool:
        """
        检查是否还有更多嫌疑人需要对话
        """
        return self.current_suspect_index < len(self.suspects)
    
    def reset(self):
        self.current_suspect_index = 0
        self.conversation_round = 0