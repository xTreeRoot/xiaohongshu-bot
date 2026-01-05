"""内容风格工厂 - 工厂模式实现"""

from typing import Dict, Type
from .base_style import BaseContentStyle
from .fairy_style import FairyStyle
from .controversial_style import ControversialStyle
from .provocative_style import ProvocativeStyle
from .unreasonable_style import UnreasonableStyle


class ContentStyleFactory:
    """内容风格工厂类
    
    使用工厂模式创建不同的内容风格策略实例
    """
    
    # 风格注册表
    _styles: Dict[str, Type[BaseContentStyle]] = {
        'fairy': FairyStyle,
        'controversial': ControversialStyle,
        'provocative': ProvocativeStyle,
        'unreasonable': UnreasonableStyle,
    }
    
    @classmethod
    def create_style(cls, style_name: str) -> BaseContentStyle:
        """创建内容风格实例
        
        Args:
            style_name: 风格名称
            
        Returns:
            内容风格实例
            
        Raises:
            ValueError: 不支持的风格类型
        """
        style_class = cls._styles.get(style_name)
        if not style_class:
            raise ValueError(
                f"不支持的风格: {style_name}。"
                f"可用风格: {', '.join(cls._styles.keys())}"
            )
        return style_class()
    
    @classmethod
    def register_style(cls, name: str, style_class: Type[BaseContentStyle]):
        """注册新的内容风格
        
        Args:
            name: 风格名称
            style_class: 风格类（必须继承 BaseContentStyle）
        """
        if not issubclass(style_class, BaseContentStyle):
            raise TypeError("风格类必须继承 BaseContentStyle")
        cls._styles[name] = style_class
    
    @classmethod
    def get_available_styles(cls) -> Dict[str, str]:
        """获取所有可用风格及其描述
        
        Returns:
            风格名称到描述的映射
        """
        return {
            name: style_class().description
            for name, style_class in cls._styles.items()
        }
