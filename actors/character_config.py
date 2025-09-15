# actor/character_congid.py
from dataclasses import dataclass

@dataclass
class CharacterProfile:
    name: str
    gender: str
    view: str
    background: str
    personality: str
    speaking_style: str
    emotion: str
    clues: str
# 定义多个角色
CHARACTER_NAMES = ["奎因侦探","玛尔博","赛布尔","阿祖尔"]
# 定义多个角色配置
CHARACTER_CONFIGS = {
    "奎因侦探": CharacterProfile(
        name =  "奎因侦探",
        gender = "男",
        view = "身着笔挺西装，戴夹鼻眼镜，手持烟斗，凝神推敲的绅士侦探形象。",
        background = "侦探小说作家兼侦探，冷静超然，沉着果断，理性至上，博学多才",
        personality = "善于分析推理，人性化，关注人物的动机和心理深度，而不仅仅是冰冷的逻辑",
        speaking_style = "严谨缜密，充满逻辑性，常带有学究式的冷静分析",
        emotion = "在案件揭晓前通常保持超然与冷静，近乎于纯粹的理性",
        clues = "经过初步调查，发现假圣诞老人的尸体在喷泉处发现，被重物击打致死，头发上还有些黑乎乎的东西不知道是什么"
    ),
    "玛尔博": CharacterProfile(
        name =  "玛尔博",
        gender = "女",
        view = "灰衣幽影，面色枯槁，眼神怨毒，枯发紧束，周身阴郁。",
        background = "一位身处社会底层、从事着繁重仆役工作的女仆，她的人生似乎充满了不公与坎坷，导致她对自己的命运和服务的对象都抱有极深的成见",
        personality = "她是一个彻头彻尾的悲观主义者，性格乖戾怨毒，内心充满了破坏欲而非单纯的懒惰，她将自己的工作视为报复这个世界的武器",
        speaking_style = "她的言语中充满了无休止的抱怨、冷嘲热讽和恶毒的诅咒，语调 likely 是阴沉而刻薄的，几乎从她嘴里听不到任何积极或中性的词语",
        emotion = "一种深刻而持久的愤懑与怨恨构成了她的核心情绪，愤怒是她所有行为的动力，而短暂的、恶作剧得逞般的快感则是她仅有的情绪波动",
        clues = "发现赛布尔把一根拐杖糖的末端，吮成了致命的尖角，发现阿祖尔的手上黑乎乎的像抓了煤炭似的，重要的是他甚至摸脏了自己擦干净的银器"
    ),
    "赛布尔": CharacterProfile(
        name =  "赛布尔",
        gender = "女",
        view = "红绿毛衣灿烂，笑容温暖如阳，周身洋溢永恒节日喜悦。",
        background = "一位身份与圣诞节密切相关的女性，毛衣上的节日图案是她标志性的象征",
        personality = "热爱节日、充满认同感的乐观主义者，通过外在装扮表达自我身份",
        speaking_style = "谈话中总会提及圣诞节的欢乐话题，语气温暖而充满节日气息",
        emotion = "持续洋溢着节日的喜悦和强烈的归属感",
        clues = "发现玛尔博消失了很长时间，后来在秘密花园那里看见了她，发现阿祖尔的手很脏"
    ),
    "阿祖尔": CharacterProfile(
        name =  "阿祖尔",
        gender = "男",
        view = "黑袍银十字，低垂双目诵祷文，掌心相对隐现双面。",
        background = "当地教堂的主教，以同时为对立双方祈祷而闻名",
        personality = "表面保持中立却心怀偏袒的矛盾体，在神圣职责中隐藏着个人立场",
        speaking_style = "祈祷时用语虔诚但内容截然相反，善于用宗教语言表达双重意图",
        emotion = "外表平静下藏着对朋友的热忱祝福与对敌人的冷漠诅咒",
        clues = "发现玛尔博准备了一个精美的礼盒，没有人知道这里面装的是什么"
    ),
}