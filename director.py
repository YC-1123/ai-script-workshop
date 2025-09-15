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
            # "深入审讯对质", 
            # "最终真相揭露"
        ]
        self.phase_index = 0
        self.coordinator = ResponseCoordinator(self.character_names)
        self.round_times = 1  # 每对角色对话轮数

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
        
        # 对每个剧情阶段
        for phase_idx, phase in enumerate(self.story_phases):
            print(f"\n———第{phase_idx+1}轮 · 剧情阶段【{phase}】———")
            
            # 奎因侦探分别与每个嫌疑人对话
            self.coordinator.reset()
            while self.coordinator.has_more_suspects():
                pair = self.coordinator.get_conversation_pair()
                detective, suspect = pair
                
                print(f"\n>>> {detective} 与 {suspect} 的对话 <<<")
                
                # 每对角色进行round_times轮对话
                for round_num in range(self.round_times):
                    print(f"\n--- 第{round_num+1}轮对话 ---")
                    
                    # 奎因侦探发言
                    speaker = detective
                    ctx = self.contexts[speaker]
                    prompt = ctx.build_prompt(f"{phase} - 与{suspect}对话")
                    response = await ctx.generate_response(prompt)
                    ctx.update_context(response)
                    print(f"\n{speaker}: {response}")
                    
                    # 将奎因探长的问题传递给嫌疑人
                    self.contexts[suspect].set_detective_question(response)
                    
                    # 嫌疑人回应
                    speaker = suspect
                    ctx = self.contexts[speaker]
                    prompt = ctx.build_prompt(f"{phase} - 回应{detective}")
                    response = await ctx.generate_response(prompt)
                    ctx.update_context(response)
                    print(f"\n{speaker}: {response}")
                
                # 切换到下一个嫌疑人
                self.coordinator.next_suspect()
            
            # 检查是否触发剧情推进
            self.advance_phase()

        print("\n【系统】剧情部分推进结束")
    
    def advance_phase(self):
        """推进到下一个剧情阶段"""
        if self.phase_index < len(self.story_phases) - 1:
            self.phase_index += 1
        