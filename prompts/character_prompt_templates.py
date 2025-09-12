# prompts/character_prompt_templates.py

def build_character_prompt(
    name: str, 
    background: str, 
    personality: str, 
    style: str, 
    emotion: str, 
    story_phase: str, 
    history: str) -> str:

    """
    构建角色生成Prompt文本，融合剧情阶段、人物设定、当前情绪与历史上下文摘要。
    """
    return(
        f"当前剧情阶段：{story_phase}。\n"
        f"{name}，请根据设定继续对话。\n"
        f"人物背景：{background}。\n"
        f"性格特点：{personality}。\n"
        f"语气风格：{style}。\n"
        f"当前情绪：{emotion}。\n"
        f"历史上下文摘要：{history}\n"
        f"{name}："
    )
