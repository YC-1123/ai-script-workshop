# director.py
import asyncio
from actors.character_config import CHARACTER_NAMES
from actors.context_manager import CharacterContextManager
from prompts.story_templates import GetStoryIntro
from engine.response_coordinator import ResponseCoordinator
from story.story_state import StoryState
from story.trigger_rules import *
from user_input.direct_edit import UserQueryHandler
from user_input.input_handler import safe_input
class StoryDirector:
    def __init__(self):
        # 定义角色名称与剧情阶段
        self.character_names = CHARACTER_NAMES
        self.contexts = {}
        self.story_state = StoryState()
        self.coordinator = ResponseCoordinator(self.character_names)
        self.round_times = 1  # 每对角色对话轮数
        self.conversation_history = []  # 记录所有对话内容
        self.user_handler = UserQueryHandler(self)  # 用户输入处理器
        self.auto_mode = True  # 默认自动模式

    async def initialize_characters(self):
        print("【系统】剧本角色初始化中...\n")
        for name in self.character_names:
            self.contexts[name] = CharacterContextManager(name)
            self.contexts[name].initialize_context()
        print("【系统】初始化完成，当前参与角色：", "、".join(self.character_names))
        # 输出剧情介绍 prompts.story_templates
        print(f"\n【系统】{GetStoryIntro()}")
        
        # 选择运行模式
        self.select_mode()

    def select_mode(self):
        """选择运行模式"""
        print("\n【系统】请选择运行模式：")
        print("1. 自动模式 - 剧情自动推进")
        print("2. 用户控制模式 - 每轮对话前可输入指令")
        
        while True:
            choice = safe_input("请输入选择 (1/2): ")
            if choice == "1":
                self.auto_mode = True
                print("【系统】已选择自动模式")
                break
            elif choice == "2":
                self.auto_mode = False
                print("【系统】已选择用户控制模式")
                break
            else:
                print("【系统】无效选择，请输入 1 或 2")

    async def run_story_loop(self):
        print("\n【系统】剧情演化开始")
        if self.auto_mode:
            print("【提示】输入 '暂停' 可进入用户控制模式")
        else:
            print("【提示】用户控制模式，每轮对话前可输入指令")
        print()
        
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
                    # print(f"\n--- 第{round_num+1}轮对话 ---")
                    
                    # 检查用户输入
                    if self.auto_mode:
                        if await self.check_user_input():
                            continue
                    else:
                        await self.user_control_prompt()
                    
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
        
    async def check_user_input(self):
        """检查是否有用户输入，非阻塞"""
        try:
            import select
            import sys
            if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
                user_input = safe_input()
                if user_input == "暂停":
                    await self.enter_user_mode()
                    return True
        except:
            pass
        return False
    
    async def enter_user_mode(self):
        """进入用户控制模式"""
        print("\n【系统】进入用户控制模式，输入 '继续' 返回剧情")
        while True:
            user_input = safe_input("用户指令> ")
            if user_input == "继续":
                print("【系统】返回剧情模式")
                break
            result = self.user_handler.handle_user_input(user_input)
            print(result)
    
    async def user_control_prompt(self):
        """用户控制模式下的指令输入"""
        print("【用户控制】输入指令或直接回车继续对话\n",
              "基本指令格式：命令:角色:内容 或 命令:内容（全部角色）\n",
              "命令：注入线索、切换情绪、查看状态、跳过阶段")
        
        user_input = safe_input("指令> ")
        if user_input:
            result = self.user_handler.handle_user_input(user_input)
            print(result)
        