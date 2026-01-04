"""AI 管理器 - 文案生成和评论回复"""
import random
from typing import Optional, List
from core.ai_client import BaseAIClient, AIClientFactory
from core.models import Comment
from core.logger import logger
from core.exceptions import XHSException


class AIManager:
    """
    AI 管理器 - 负责生成小红书风格文案和智能评论回复
    
    使用工厂模式，支持自定义 AI 客户端。
    """
    
    # 小红书风格的 emoji 池
    EMOJIS = [
        "*", "+", "~", "=", "-", "_", ".", ",", 
        "!", "?", "@", "#", "$", "%", "&", "|",
        "<", ">", "[", "]", "{", "}", "(", ")"
    ]
    
    # 小仙女风格的常用词
    FAIRY_WORDS = [
        "姐妹们", "宝子们", "集美们", "小仙女们", "亲们",
        "真的绝了", "yyds", "爱了爱了", "太可了", "狠狠爱了",
        "疯狂心动", "直接拿下", "闭眼入", "必须安利"
    ]
    
    def __init__(self, client: Optional[BaseAIClient] = None, client_type: Optional[str] = None):
        """
        初始化 AI 管理器
        
        Args:
            client: 直接传入的 AI 客户端实例（优先级最高）
            client_type: AI 客户端类型（如 "openai", "custom_ai"）
                        如果 client 和 client_type 都为 None，则使用默认客户端
        
        Example:
            >>> # 使用默认客户端
            >>> manager = AIManager()
            
            >>> # 指定客户端类型
            >>> manager = AIManager(client_type="openai")
            
            >>> # 直接传入自定义客户端
            >>> my_client = MyCustomAI()
            >>> manager = AIManager(client=my_client)
        """
        if client is not None:
            # 直接使用传入的客户端
            if not isinstance(client, BaseAIClient):
                raise ValueError("客户端必须是 BaseAIClient 的实例")
            self.client = client
        else:
            # 使用工厂创建客户端
            self.client = AIClientFactory.create_client(client_type)
        
        logger.info(f" AI 管理器初始化成功 - 客户端: {self.client.get_client_info()}")
    
    def generate_xiaohongshu_post(
        self, 
        topic: str = None,
        style: str = "fairy",
        word_count: int = 100
    ) -> str:
        """
        生成小红书风格短文
        
        Args:
            topic: 主题，None 则随机生成
            style: 风格类型
                - fairy: 小仙女风格
                - controversial: 逆天言论风格
                - provocative: 引战风格
            word_count: 字数限制
        
        Returns:
            生成的文案
        """
        if not self.client.is_available():
            raise XHSException("AI 客户端不可用，请检查配置")
        
        # 构建 prompt
        if style == "fairy":
            system_prompt = self._get_fairy_system_prompt()
            user_prompt = self._get_fairy_user_prompt(topic, word_count)
        elif style == "controversial":
            system_prompt = self._get_controversial_system_prompt()
            user_prompt = self._get_controversial_user_prompt(topic, word_count)
        elif style == "provocative":
            system_prompt = self._get_provocative_system_prompt()
            user_prompt = self._get_provocative_user_prompt(topic, word_count)
        else:
            raise ValueError(f"不支持的风格: {style}")
        
        logger.info(f"开始生成小红书文案 - 风格: {style}, 主题: {topic or '随机'}")
        
        try:
            content = self.client.generate_text(
                prompt=user_prompt,
                system_prompt=system_prompt,
                temperature=0.9  # 高温度增加创意性
            )
            
            # 添加 emoji 装饰
            content = self._add_emojis(content)
            
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
        """
        根据评论生成回复
        
        Args:
            comment: 评论对象
            style: 回复风格
                - aggressive: 斗争性回复
                - sarcastic: 讽刺回复
                - defensive: 防御反击
                - dismissive: 不屑回复
        
        Returns:
            生成的回复内容
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
            
            # 随机添加 emoji
            if random.random() > 0.5:
                reply = self._add_emojis(reply, max_count=2)
            
            logger.info(f" 回复生成成功: {reply[:50]}...")
            return reply
        
        except Exception as e:
            logger.error(f"回复生成失败: {e}")
            raise XHSException(f"回复生成失败: {e}")
    
    # ==================== Prompt 模板方法 ====================
    
    def _get_fairy_system_prompt(self) -> str:
        """小仙女风格系统提示"""
        return """你是一个小红书博主，擅长写小仙女风格的文案。
特点：
1. 使用"姐妹们"、"宝子们"、"集美们"等称呼
2. 大量使用感叹号和 emoji
3. 语气夸张、情绪化
4. 喜欢用"绝了"、"爱了"、"yyds"等网络用语
5. 内容要有分享欲，仿佛在和闺蜜聊天
6. 适当制造话题和争议点"""
    
    def _get_fairy_user_prompt(self, topic: Optional[str], word_count: int) -> str:
        """小仙女风格用户提示"""
        if topic:
            return f"写一篇关于'{topic}'的小红书文案，约{word_count}字。要有小仙女的感觉，语气活泼夸张。"
        else:
            topics = ["穿搭", "美妆", "减肥", "恋爱", "职场", "美食", "旅行", "日常吐槽"]
            random_topic = random.choice(topics)
            return f"写一篇关于{random_topic}的小红书文案，约{word_count}字。要有小仙女的感觉，语气活泼夸张。"
    
    def _get_controversial_system_prompt(self) -> str:
        """逆天言论风格系统提示"""
        return """你是一个喜欢发表惊人观点的小红书博主。
特点：
1. 观点独特、出人意料，甚至有些"逆天"
2. 敢于挑战常识和主流观点
3. 用词夸张，制造话题性
4. 但不能违法违规或人身攻击
5. 要有一定的逻辑性，不是纯粹胡说
6. 善于制造争议和讨论"""
    
    def _get_controversial_user_prompt(self, topic: Optional[str], word_count: int) -> str:
        """逆天言论风格用户提示"""
        if topic:
            return f"关于'{topic}'，发表一个出人意料的独特观点，约{word_count}字。要有争议性但不违规。"
        else:
            topics = ["女性独立", "恋爱观", "消费观", "工作态度", "人际关系", "生活方式"]
            random_topic = random.choice(topics)
            return f"关于{random_topic}，发表一个出人意料的独特观点，约{word_count}字。要有争议性但不违规。"
    
    def _get_provocative_system_prompt(self) -> str:
        """引战风格系统提示"""
        return """你是一个擅长制造话题的小红书博主。
特点：
1. 善于挑起不同群体之间的讨论
2. 使用对比、反问等手法
3. 语气略带挑衅，但不恶意
4. 容易引发评论区争论
5. 善于制造"站队"话题
6. 不涉及敏感政治、民族等话题"""
    
    def _get_provocative_user_prompt(self, topic: Optional[str], word_count: int) -> str:
        """引战风格用户提示"""
        if topic:
            return f"写一篇关于'{topic}'的文案，约{word_count}字。要能引发讨论和争论，但不要过于恶意。"
        else:
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
    
    def _get_reply_system_prompt(self, style: str) -> str:
        """评论回复系统提示"""
        prompts = {
            "aggressive": """你是一个不怕怼人的小红书博主。
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
5. 简短但有杀伤力"""
        }
        return prompts.get(style, prompts["aggressive"])
    
    def _get_reply_user_prompt(self, comment: Comment, style: str) -> str:
        """评论回复用户提示"""
        return f"""有人在我的小红书帖子下评论："{comment.content}"

请用{style}风格回复这条评论，要求：
1. 20-50字以内
2. 直击要害
3. 符合小红书语境
4. 不使用脏话粗口"""
    
    # ==================== 辅助方法 ====================
    
    def _add_emojis(self, text: str, max_count: int = 5) -> str:
        """在文本中添加 emoji"""
        sentences = text.split("。")
        result = []
        
        emoji_count = 0
        for sentence in sentences:
            if sentence.strip():
                # 随机决定是否添加 emoji
                if random.random() > 0.4 and emoji_count < max_count:
                    emoji = random.choice(self.EMOJIS)
                    result.append(f"{sentence}{emoji}")
                    emoji_count += 1
                else:
                    result.append(sentence)
        
        return "。".join(result)
    
    def batch_generate_posts(
        self,
        count: int,
        style: str = "fairy",
        topics: Optional[List[str]] = None
    ) -> List[str]:
        """
        批量生成文案
        
        Args:
            count: 生成数量
            style: 风格
            topics: 主题列表，None 则随机
        
        Returns:
            文案列表
        """
        posts = []
        for i in range(count):
            topic = topics[i] if topics and i < len(topics) else None
            try:
                post = self.generate_xiaohongshu_post(topic=topic, style=style)
                posts.append(post)
                logger.info(f" 已生成第 {i+1}/{count} 篇文案")
            except Exception as e:
                logger.error(f"第 {i+1} 篇文案生成失败: {e}")
                continue
        
        return posts
