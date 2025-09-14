# actors/context_manager.py
import random
from actors.character_config import CHARACTER_CONFIGS
from prompts.character_prompt_templates import build_character_prompt
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
        prompt = build_character_prompt(
            self.name,
            self.profile.background,
            self.profile.personality,
            self.profile.speaking_style,
            self.profile.emotion,
            self.profile.special_setting,
            phase,
            context,
        )
        return prompt

    async def generate_response(self, prompt:str) -> str:
        # 调用 deepseek-chat 接口
        response = await generate_response(self.name, prompt)
        return response
    
    def update_context(self, response: str):
        self.history.append(f"{self.name}: {response}")