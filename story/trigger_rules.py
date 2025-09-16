# story/trigger_rules.py

def should_advance_to_deep_interrogation(messages: list) -> bool:
    """
    【初步调查询问】→【深入审讯对质】触发规则
    """
    trigger_words = ["不信", "怀疑", "可疑", "奇怪", "不对劲", "证据", "线索"]
    return any(any(word in msg for word in trigger_words) for msg in messages)

def should_advance_to_final_reveal(messages: list) -> bool:
    """
    【深入审讯对质】→【最终真相揭露】触发规则
    """
    trigger_words = ["矛盾", "冲突", "不一致", "发现", "重要", "关键"]
    return any(any(word in msg for word in trigger_words) for msg in messages)

def should_end_story(messages: list) -> bool:
    """
    【最终真相揭露】→结束剧情触发规则
    """
    trigger_words = ["真相", "凶手", "动机", "确定", "结论", "推理", "答案", "就是你"]
    return any(any(word in msg for word in trigger_words) for msg in messages)
