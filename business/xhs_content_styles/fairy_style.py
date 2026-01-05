"""小仙女风格策略"""

import random
from typing import Optional

from .base_style import BaseContentStyle


class FairyStyle(BaseContentStyle):
    """小仙女风格 - 甜美活泼的日常分享"""

    @property
    def description(self) -> str:
        return "小仙女风格（甜美活泼、情绪化、网络用语）"

    def get_system_prompt(self) -> str:
        """获取小仙女风格系统提示"""
        return """
                你是一个小红书博主，擅长写小仙女风格的文案。
                特点：
                1. 使用"姐妹们"、"宝子们"、"集美们"等称呼
                2. 大量使用感叹号和 emoji
                3. 语气夸张、情绪化
                4. 喜欢用"绝了"、"爱了"、"yyds"等网络用语
                5. 内容要有分享欲，仿佛在和闺蜜聊天
                6. 适当制造话题和争议点
                """

    def get_user_prompt(self, topic: Optional[str], word_count: int) -> str:
        """获取小仙女风格用户提示"""
        if topic:
            return f"写一篇关于'{topic}'的小红书文案，约{word_count}字。要有小仙女的感觉，语气活泼夸张。"

        topics = ["穿搭", "美妆", "减肥", "恋爱", "职场", "美食", "旅行", "日常吐槽"]
        random_topic = random.choice(topics)
        return f"写一篇关于{random_topic}的小红书文案，约{word_count}字。要有小仙女的感觉，语气活泼夸张。"
