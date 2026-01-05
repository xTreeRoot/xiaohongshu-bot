"""DOM元素数据模型"""
from dataclasses import dataclass
from typing import Optional
import json
from datetime import datetime


@dataclass
class DOMElement:
    """DOM元素信息"""
    element_id: str
    selector: str
    element_type: str
    position: Optional[str] = None
    text_content: Optional[str] = None
    updated_at: Optional[datetime] = None
    page_url: Optional[str] = None
    description: Optional[str] = None

    def to_dict(self) -> dict:
        """转换为字典格式"""
        return {
            'element_id': self.element_id,
            'selector': self.selector,
            'element_type': self.element_type,
            'position': self.position,
            'text_content': self.text_content,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'page_url': self.page_url,
            'description': self.description
        }

    @classmethod
    def from_dict(cls, data: dict):
        """从字典创建实例"""
        updated_at = None
        if data.get('updated_at'):
            try:
                updated_at = datetime.fromisoformat(data['updated_at'])
            except ValueError:
                # 如果格式不正确，尝试其他格式
                pass
        
        return cls(
            element_id=data['element_id'],
            selector=data['selector'],
            element_type=data['element_type'],
            position=data.get('position'),
            text_content=data.get('text_content'),
            updated_at=updated_at,
            page_url=data.get('page_url'),
            description=data.get('description')
        )