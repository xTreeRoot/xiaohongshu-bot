"""发布内容模型"""
from dataclasses import dataclass, field
from typing import List


@dataclass
class PublishContent:
    """发布内容"""
    content: str
    title: str
    description: str = ""
    tags: List[str] = field(default_factory=list)
    
    def validate(self) -> bool:
        """验证内容是否有效"""
        return bool(self.content and self.title)
