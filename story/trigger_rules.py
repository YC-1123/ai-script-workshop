# story/trigger_rules.py
# 触发 获取第一轮线索
def should_trigger_clue1(messages: list) -> bool:
    """
    【获取第一轮线索】触发规则：任意角色xxxxxxx提及质疑、对立情绪词则触发冲突xxxxxx
    """
    trigger_words = ["不信", "怀疑"]
    for msg in messages:
        if any(word in msg for word in trigger_words):
            return True
        return False

# 触发 与赛布尔的对话
def should_trigger_clue2(messages: list) -> bool:
    """
    【与赛布尔的对话】触发规则：
    """
    trigger_words = ["理解", "接受"]
    return all(any(word in msg for word in key_words) for msg in messages)

# 触发 获取第二轮线索
def should_trigger_clue3(messages: list) -> bool:
    """
    【获取第二轮线索】触发规则：
    """
    trigger_words = ["理解", "接受"]
    return all(any(word in msg for word in key_words) for msg in messages)

# 触发 与阿祖尔的对话
def should_trigger_clue4(messages: list) -> bool:
    """
    【与阿祖尔的对话】触发规则：
    """
    trigger_words = ["理解", "接受"]
    return all(any(word in msg for word in key_words) for msg in messages)

# 触发 获取第三轮线索
def should_trigger_clue5(messages: list) -> bool:
    """
    【获取第三轮线索】触发规则：
    """
    trigger_words = ["理解", "接受"]
    return all(any(word in msg for word in key_words) for msg in messages)

# 触发 推理凶手
def should_trigger_clue6(messages: list) -> bool:
    """
    【推理凶手】触发规则：
    """
    trigger_words = ["理解", "接受"]
    return all(any(word in msg for word in key_words) for msg in messages)
