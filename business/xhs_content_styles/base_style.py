"""内容风格基类 - 策略模式抽象基类"""

from abc import ABC, abstractmethod
from typing import Optional


class BaseContentStyle(ABC):
    """内容风格策略抽象基类
    
    所有内容风格必须继承此类并实现 get_system_prompt 和 get_user_prompt 方法
    """
    
    @abstractmethod
    def get_system_prompt(self) -> str:
        """获取系统提示词
        
        Returns:
            系统提示词字符串
        """
        pass
    
    @abstractmethod
    def get_user_prompt(self, topic: Optional[str], word_count: int) -> str:
        """获取用户提示词
        
        Args:
            topic: 主题，None 则随机生成
            word_count: 目标字数
            
        Returns:
            用户提示词字符串
        """
        pass
    
    @property
    def style_name(self) -> str:
        """风格名称"""
        return self.__class__.__name__.replace('Style', '').lower()
    
    @property
    def description(self) -> str:
        """风格描述"""
        return "未定义风格描述"
