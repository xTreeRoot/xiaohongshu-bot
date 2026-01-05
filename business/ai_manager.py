"""AI 管理器 - 文案生成和评论回复

本模块提供智能文案生成和评论回复功能。
支持多种风格：小仙女、逆天言论、引战、250风格等。
"""

from typing import Optional, List

from core import BaseAIClient, AIClientFactory
from core.exceptions import XHSException
from core.logger import logger
from core.models import Comment
from .xhs_content_styles import ContentStyleFactory


class AIManager:
    """AI 管理器 - 负责生成小红书风格文案和智能评论回复
    
    使用策略模式和工厂模式，支持自定义内容风格。
    """

    def __init__(
            self,
            client: Optional[BaseAIClient] = None,
            client_type: Optional[str] = None
    ):
        """初始化 AI 管理器
        
        Args:
            client: AI 客户端实例（必须是 BaseAIClient 的子类）
            client_type: 客户端类型，如 "openai", "zhipu"
        
        Raises:
            ValueError: client 不是 BaseAIClient 实例时
        """
        if client is not None:
            if not isinstance(client, BaseAIClient):
                raise ValueError("客户端必须是 BaseAIClient 的实例")
            self.client = client
        else:
            self.client = AIClientFactory.create_client(client_type)

        logger.info(f" AI 管理器初始化成功 - 客户端: {self.client.get_client_info()}")

    def generate_xiaohongshu_post(
            self,
            topic: str = None,
            style: str = "fairy",
            word_count: int = 100
    ) -> str:
        """生成小红书风格短文
        
        Args:
            topic: 主题，None 则随机生成
            style: 风格类型
                - fairy: 小仙女风格（甜美活泼）
                - controversial: 逆天言论（独特观点）
                - provocative: 引战风格（制造站队）
                - unreasonable: 250风格（ 高流量但需谨慎）
            word_count: 字数限制
        
        Returns:
            生成的文案内容
            
        Raises:
            XHSException: AI 客户端不可用或生成失败
            ValueError: 不支持的风格类型
        """
        if not self.client.is_available():
            raise XHSException("AI 客户端不可用，请检查配置")

        # 使用策略模式获取内容风格
        try:
            content_style = ContentStyleFactory.create_style(style)
        except ValueError as e:
            raise ValueError(f"不支持的风格: {style}") from e

        system_prompt = content_style.get_system_prompt()
        user_prompt = content_style.get_user_prompt(topic, word_count)

        logger.info(f"开始生成小红书文案 - 风格: {style}, 主题: {topic or '随机'}")

        try:
            content = self.client.generate_text(
                prompt=user_prompt,
                system_prompt=system_prompt,
                temperature=0.9  # 高温度增加创意性
            )

            logger.info(f" 文案生成成功，长度: {len(content)} 字")
            return content

        except Exception as e:
            logger.error(f"文案生成失败: {e}")
            raise XHSException(f"文案生成失败: {e}")

    def generate_comment_reply(
            self,
            comment: Comment,
            style: str = "aggressive"
    ) -> str:
        """根据评论生成智能回复
        
        Args:
            comment: 评论对象
            style: 回复风格
                - aggressive: 斗争性回复（强硬直接）
                - sarcastic: 讽刺回复（阴阳怪气）
                - defensive: 防御反击（摆事实讲道理）
                - dismissive: 不屑回复（高傲冷淡）
        
        Returns:
            生成的回复内容（20-50字）
            
        Raises:
            XHSException: AI 客户端不可用或生成失败
        """
        if not self.client.is_available():
            raise XHSException("AI 客户端不可用，请检查配置")

        system_prompt = self._get_reply_system_prompt(style)
        user_prompt = self._get_reply_user_prompt(comment, style)

        logger.info(f"生成评论回复 - 风格: {style}, 评论: {comment.content[:30]}...")

        try:
            reply = self.client.generate_text(
                prompt=user_prompt,
                system_prompt=system_prompt,
                temperature=0.8
            )

            logger.info(f" 回复生成成功: {reply[:50]}...")
            return reply

        except Exception as e:
            logger.error(f"回复生成失败: {e}")
            raise XHSException(f"回复生成失败: {e}")

    # ==================== 评论回复 Prompt 模板 ====================

    @staticmethod
    def _get_reply_system_prompt(style: str) -> str:
        """评论回复系统提示"""
        prompts = {
            "aggressive":
                """
                    你是一个不怕怼人的小红书博主。
                    特点：
                    1. 态度强硬，直接反驳
                    2. 语气犀利但不失风度
                    3. 善于抓住对方逻辑漏洞
                    4. 不使用脏话，但很有杀伤力
                    5. 回复简短有力""",

            "sarcastic": """你是一个擅长讽刺的小红书博主。
                    特点：
                    1. 使用反讽、明褒暗贬
                    2. 看似客气实则嘲讽
                    3. 语气阴阳怪气
                    4. 善用"呵呵"、"哦"等语气词
                    5. 不直接骂人但让对方难受""",

            "defensive": """你是一个善于防御反击的小红书博主。
                    特点：
                    1. 先解释立场，再反击
                    2. 摆事实讲道理
                    3. 暗示对方无知或偏见
                    4. 态度坚定但不失礼貌
                    5. 适当展示优越感""",

            "dismissive": """你是一个不屑与人争辩的小红书博主。
                    特点：
                    1. 表现出不屑和轻蔑
                    2. 用最少的字回怼
                    3. 暗示对方不值得认真对待
                    4. 语气高傲冷淡
                    5. 简短但有杀伤力
                """
        }
        return prompts.get(style, prompts["aggressive"])

    @staticmethod
    def _get_reply_user_prompt(comment: Comment, style: str) -> str:
        """评论回复用户提示"""
        return f"""
                有人在我的小红书帖子下评论："{comment.content}"
                帖子标题：{getattr(comment, 'post_title', '未知标题')}
                帖子内容：{getattr(comment, 'post_content', '未知内容')}
                
                请用{style}风格回复这条评论，要求：
                1. 20-50字以内
                2. 直击要害
                3. 符合小红书语境
                4. 不使用脏话粗口
            """

    # ==================== 辅助方法 ====================

    def batch_generate_posts(
            self,
            count: int,
            style: str = "fairy",
            topics: Optional[List[str]] = None
    ) -> List[str]:
        """批量生成文案
        
        Args:
            count: 生成数量
            style: 风格类型
            topics: 主题列表，None 则随机
        
        Returns:
            成功生成的文案列表
        """
        posts = []
        for i in range(count):
            topic = topics[i] if topics and i < len(topics) else None
            try:
                post = self.generate_xiaohongshu_post(topic=topic, style=style)
                posts.append(post)
                logger.info(f" 已生成第 {i + 1}/{count} 篇文案")
            except Exception as e:
                logger.error(f"第 {i + 1} 篇文案生成失败: {e}")
                continue

        return posts
