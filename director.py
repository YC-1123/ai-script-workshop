# director.py
import asyncio
from actors.context_manager import CharacterContextManager

class StoryDirector:
    def __init__(self):
        # 定义角色名称与剧情阶段
        self.character_names = ["埃勒里·奎因","玛尔博","赛布尔","阿祖尔"]
        self.contexts = {}
        self.story_phases = ["与玛尔博的对话", "获取第一轮线索" ,"与赛布尔的对话", "获取第二轮线索", "与阿祖尔的对话", "获取第三轮线索", "推理凶手"]
        self.phase_index = 0

    async def initialize_characters(self):
        print("【系统】剧本角色初始化中...\n")
        for name in self.character_names:
            self.contexts[name] = CharacterContextManager(name)
            self.contexts[name].initialize_context()
        print("【系统】初始化完成，当前参与角色：", "、".join(self.character_names))
        print("\n【背景】德拉库尼亚的圣诞节是一场支持君主复辟的庆典。贵族们围聚在一起，交换礼物，追忆过去的美好时光，直到大家发现扮演圣诞老人的家伙被杀了...")

    async def run_story_loop(self):
        print("\n【系统】剧情演化开始\n")
        for i in range(7):
            phase = self.story_phases[self.phase_index]
            print(f"\n———第{i+1}轮 · 剧情阶段【{phase}】———")
            for name in self.character_names:
                ctx = self.contexts[name]
                # 构建角色专属Prompt，含剧情阶段
                prompt = ctx.build_prompt(phase)
                # 调用DeepSeek-chat接口方法
                response = await ctx.generate_response(prompt)
                ctx.update_context(response)
                print(f"\n{name}:{response}")
            self.advance_phase()

        print("\n【系统】剧情部分推进结束")
    
    def advance_phase(self):
        if self.phase_index < len(self.story_phases) - 1:
            self.phase_index += 1
        