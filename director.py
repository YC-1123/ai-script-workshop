# director.py
import asyncio
from actors.character_config import CHARACTER_NAMES
from actors.context_manager import CharacterContextManager
from prompts.story_templates import GetStoryIntro
from engine.response_coordinator import ResponseCoordinator
class StoryDirector:
    def __init__(self):
        # 定义角色名称与剧情阶段
        self.character_names = CHARACTER_NAMES
        self.contexts = {}
        self.story_phases = [
            "初步调查询问", 
            "深入审讯对质", 
            "最终真相揭露"
        ]
        self.phase_index = 0
        self.coordinator = ResponseCoordinator(self.character_names)

    async def initialize_characters(self):
        print("【系统】剧本角色初始化中...\n")
        for name in self.character_names:
            self.contexts[name] = CharacterContextManager(name)
            self.contexts[name].initialize_context()
        print("【系统】初始化完成，当前参与角色：", "、".join(self.character_names))
        # 输出剧情介绍 prompts.story_templates
        print(f"\n【系统】{GetStoryIntro()}")

    async def run_story_loop(self):
        print("\n【系统】剧情演化开始\n")
        for i in range(len(self.story_phases)):
            phase = self.story_phases[self.phase_index]
            print(f"\n———第{i+1}轮 · 剧情阶段【{phase}】———")
            
            # 使用ResponseCoordinator控制角色发言顺序
            for _ in range(len(self.character_names)):
                name = self.coordinator.next_character()
                ctx = self.contexts[name]
                # 构建角色专属Prompt，含剧情阶段
                prompt = ctx.build_prompt(phase)
                # 调用deepseek-chat接口方法
                response = await ctx.generate_response(prompt)
                ctx.update_context(response)
                print(f"\n{name}:{response}")
            self.advance_phase(ctx.msglist)

        print("\n【系统】剧情部分推进结束")
    
    def advance_phase(self, msglist):
        trigger_words = ["煤炭","黑","泥土","脏"]
        for msg in msglist:
            if any(word in msg for word in trigger_words):
                self.phase_index += 1
        # if self.phase_index < len(self.story_phases) - 1:
        #     self.phase_index += 1
        