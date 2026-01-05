"""引战风格策略"""

import random
from typing import Optional

from .base_style import BaseContentStyle


class ProvocativeStyle(BaseContentStyle):
    """引战风格 - 制造话题引发争论"""

    @property
    def description(self) -> str:
        return "引战风格（对比挑衅、制造站队、引发争论）"

    def get_system_prompt(self) -> str:
        """获取引战风格系统提示"""
        return """
                你是一个擅长制造话题的小红书博主。
                特点：
                1. 善于挑起不同群体之间的讨论
                2. 使用对比、反问等手法
                3. 语气略带挑衅，但不恶意
                4. 容易引发评论区争论
                5. 善于制造"站队"话题
                6. 不涉及敏感政治、民族等话题
                """

    def get_user_prompt(self, topic: Optional[str], word_count: int) -> str:
        """获取引战风格用户提示"""
        if topic:
            return f"写一篇关于'{topic}'的文案，约{word_count}字。要能引发讨论和争论，但不要过于恶意。"

        topics = [
            "全职太太 vs 职场女性",
            "奢侈品消费",
            "相亲条件",
            "家务分工",
            "育儿观念",
            "消费主义"
        ]
        random_topic = random.choice(topics)
        return f"写一篇关于'{random_topic}'的文案，约{word_count}字。要能引发讨论和争论，但不要过于恶意。"
