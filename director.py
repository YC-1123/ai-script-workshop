# director.py
import asyncio
from actors.character_config import CHARACTER_NAMES
from actors.context_manager import CharacterContextManager
from prompts.story_templates import GetStoryIntro
from engine.response_coordinator import ResponseCoordinator
from story.story_state import StoryState
from story.trigger_rules import *
class StoryDirector:
    def __init__(self):
        # 定义角色名称与剧情阶段
        self.character_names = CHARACTER_NAMES
        self.contexts = {}
        self.story_state = StoryState()
        self.coordinator = ResponseCoordinator(self.character_names)
        self.round_times = 1  # 每对角色对话轮数
        self.conversation_history = []  # 记录所有对话内容

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
        while self.story_state.current_index < len(self.story_state.phases):
            current_phase = self.story_state.get_current_phase()
            print(f"\n———第{self.story_state.current_index+1}轮 · 剧情阶段【{current_phase}】———")
            
            # 奎因侦探分别与每个嫌疑人对话
            self.coordinator.reset()
            while self.coordinator.has_more_suspects():
                pair = self.coordinator.get_conversation_pair()
                detective, suspect = pair
                
                print(f"\n>>> {detective} 与 {suspect} 的对话 <<<")
                
                # 让双方了解对方的基本信息
                detective_profile = self.contexts[detective].profile
                suspect_profile = self.contexts[suspect].profile
                
                self.contexts[detective].add_character_info(suspect, suspect_profile)
                self.contexts[suspect].add_character_info(detective, detective_profile)
                
                # 为当前嫌疑人添加其他嫌疑人的基本信息
                for other_suspect in self.character_names:
                    if other_suspect != suspect and other_suspect != detective:
                        other_profile = self.contexts[other_suspect].profile
                        self.contexts[suspect].add_character_info(other_suspect, other_profile)
                
                # 每对角色进行round_times轮对话
                for round_num in range(self.round_times):
                    print(f"\n--- 第{round_num+1}轮对话 ---")
                    
                    # 奎因侦探发言
                    speaker = detective
                    ctx = self.contexts[speaker]
                    prompt = ctx.build_prompt(f"{current_phase} - 与{suspect}对话")
                    response = await ctx.generate_response(prompt)
                    ctx.update_context(response)
                    print(f"\n{speaker}: {response}")
                    self.conversation_history.append(response)
                    
                    # 将奎因探长的问题传递给嫌疑人
                    self.contexts[suspect].set_detective_question(response)
                    
                    # 嫌疑人回应
                    speaker = suspect
                    ctx = self.contexts[speaker]
                    prompt = ctx.build_prompt(f"{current_phase} - 回应{detective}")
                    response = await ctx.generate_response(prompt)
                    ctx.update_context(response)
                    print(f"\n{speaker}: {response}")
                    self.conversation_history.append(response)
                
                # 切换到下一个嫌疑人
                self.coordinator.next_suspect()
            
            # 检查是否触发剧情推进
            if self.should_advance_phase():
                self.advance_phase()
            else:
                break

        print("\n【系统】剧情部分推进结束")
    
    def should_advance_phase(self):
        """根据对话内容判断是否应该推进剧情阶段"""
        current_phase = self.story_state.get_current_phase()
        
        # 根据当前阶段选择对应的触发规则
        if current_phase == "初步调查询问":
            return should_advance_to_deep_interrogation(self.conversation_history)
        elif current_phase == "深入审讯对质":
            return should_advance_to_final_reveal(self.conversation_history)
        elif current_phase == "最终真相揭露":
            return should_end_story(self.conversation_history)
        
        return False
    
    def advance_phase(self):
        """推进到下一个剧情阶段"""
        current_phase = self.story_state.get_current_phase()
        print(f"\n【系统】触发剧情推进条件，从【{current_phase}】进入下一阶段")
        
        self.story_state.advance_phase()
        self.conversation_history.clear()  # 清空对话历史，为下一阶段做准备
        