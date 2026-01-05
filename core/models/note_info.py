"""笔记信息模型"""
from dataclasses import dataclass
from typing import Optional, Dict, Any
from datetime import datetime

from .user_info import UserInfo


@dataclass
class NoteInfo:
    """笔记信息"""
    note_id: str
    title: str
    url: str
    author: Optional[UserInfo] = None
    create_time: Optional[datetime] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'NoteInfo':
        """从字典创建实例"""
        author = None
        if 'author' in data:
            author = UserInfo.from_dict(data['author'])
        
        return cls(
            note_id=data.get('note_id', ''),
            title=data.get('title', ''),
            url=data.get('url', ''),
            author=author
        )
