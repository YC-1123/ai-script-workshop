# prompts/emotion_map.py

EMOTION_LANGUAGE_MAPPING = {
    "平静": ["简洁","理性","语气平稳"],
    "愤怒": ["短句","高强度","情绪外露"],
    "悲伤": ["拖沓","模糊","情绪低落"],
    "喜悦": ["生动","跳跃","情感外放"],
    "戒备": ["冷峻","间接","质疑"],
    "好奇": ["提问式","反复确认","带探索倾向"],
}

def emotion_tone_hint(emotion:str) -> str:
    """
    根据情绪返回语言风格提示词，用于构造提示语风格控制
    """
    styles = EMOTION_LANGUAGE_MAPPING.get(emotion, [])
    return ",".join(styles) if styles else "中性语气"