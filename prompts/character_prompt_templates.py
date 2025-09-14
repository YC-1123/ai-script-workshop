# prompts/character_prompt_templates.py

def build_character_prompt(
    name: str, 
    gender: str,
    background: str, 
    personality: str, 
    style: str, 
    emotion: str, 
    clues: str,
    story_phase: str, 
    history: str) -> str:

    """
    构建角色生成Prompt文本，融合剧情阶段、人物设定、当前情绪与历史上下文摘要。
    """
    
    # 不同阶段的行为指导
    phase_instructions = {
        "初步调查询问": "现在是初步调查阶段，你需要：谨慎回答基础问题，透露部分信息但保留关键细节，表现出配合但略有保留的态度。",
        "深入审讯对质": "现在是深入审讯阶段，你需要：面对更尖锐的质疑，可能出现情绪波动，在压力下可能暴露更多信息或产生矛盾表述。",
        "最终真相揭露": "现在是真相揭露阶段，你需要：在重重证据面前，情绪达到高潮，最终承认或揭露关键真相。"
    }
    
    instruction = phase_instructions.get(story_phase, "请根据当前情况自然对话。")
    
    return(
        f"=== 剧情阶段指导 ===\n"
        f"当前阶段：{story_phase}\n"
        f"行为要求：{instruction}\n\n"
        f"=== 角色设定 ===\n"
        f"角色：{name}（{gender}）\n"
        f"背景：{background}\n"
        f"性格：{personality}\n"
        f"语气：{style}\n"
        f"当前情绪：{emotion}\n"
        f"掌握线索：{clues}\n\n"
        f"=== 对话历史 ===\n"
        f"{history}\n\n"
        f"请以{name}的身份，根据当前阶段要求和角色设定继续对话：\n"
        f"{name}："
    )
