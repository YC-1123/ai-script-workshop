# actors/context_manager.py
import random
from actors.character_config import CHARACTER_CONFIGS
from engine.generator import generate_response
from typing import List

class CharacterContextManager:
    def __init__(self, character_name: str):
        self.profile = CHARACTER_CONFIGS[character_name]
        self.name = character_name
        self.history: List[str] = []
        
    def initialize_context(self):
        self.history.clear()
        self.history.append(f"角色设定：{self.profile.background}，性格：{self.profile.personality}，语气风格：{self.profile.speaking_style}，当前情绪：{self.profile.emotion}")

    def build_prompt(self, phase: str) -> str:
        # 取最近3轮上下文
        context = "\n".join(self.history[-3:])
        prompt = (
            f"当前剧情阶段：{phase}。\n"
            f"{self.name}，请根据设定继续对话。\n"
            f"人物背景：{self.profile.background}。\n"
            f"性格特点：{self.profile.personality}。\n"
            f"语气风格：{self.profile.speaking_style}。\n"
            f"当前情绪：{self.profile.emotion}。\n"
            f"历史对话摘要：{context}\n"
            f"{self.name}："
        )
        return prompt

    async def generate_response(self, prompt:str) -> str:
        # 调用 deepseek-chat 接口
        response = await generate_response(self.name, prompt)
        return response
    
    def update_context(self, response: str):
        self.history.append(f"{self.name}: {response}")