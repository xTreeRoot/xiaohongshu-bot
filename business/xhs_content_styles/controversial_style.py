"""逆天言论风格策略"""

import random
from typing import Optional

from .base_style import BaseContentStyle


class ControversialStyle(BaseContentStyle):
    """逆天言论风格 - 独特观点引发讨论"""

    @property
    def description(self) -> str:
        return "逆天言论风格（独特观点、挑战常识、制造话题）"

    def get_system_prompt(self) -> str:
        """获取逆天言论风格系统提示"""
        return """
        你是一个喜欢发表惊人观点的小红书博主。
        特点：
        1. 观点独特、出人意料，甚至有些"逆天"
        2. 敢于挑战常识和主流观点
        3. 用词夸张，制造话题性
        4. 但不能违法违规或人身攻击
        5. 要有一定的逻辑性，不是纯粹胡说
        6. 善于制造争议和讨论
        """

    def get_user_prompt(self, topic: Optional[str], word_count: int) -> str:
        """获取逆天言论风格用户提示"""
        if topic:
            return f"关于'{topic}'，发表一个出人意料的独特观点，约{word_count}字。要有争议性但不违规。"

        topics = ["女性独立", "恋爱观", "消费观", "工作态度", "人际关系", "生活方式"]
        random_topic = random.choice(topics)
        return f"关于{random_topic}，发表一个出人意料的独特观点，约{word_count}字。要有争议性但不违规。"
