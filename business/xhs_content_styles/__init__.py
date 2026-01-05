"""内容风格策略 - 策略模式实现

支持的文案风格：
- fairy: 小仙女风格
- controversial: 逆天言论
- provocative: 引战风格
- unreasonable: 250风格
"""

from .base_style import BaseContentStyle
from .fairy_style import FairyStyle
from .controversial_style import ControversialStyle
from .provocative_style import ProvocativeStyle
from .unreasonable_style import UnreasonableStyle
from .style_factory import ContentStyleFactory

__all__ = [
    'BaseContentStyle',
    'FairyStyle',
    'ControversialStyle',
    'ProvocativeStyle',
    'UnreasonableStyle',
    'ContentStyleFactory',
]
