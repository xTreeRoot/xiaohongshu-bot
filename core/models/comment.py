"""评论数据模型"""
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime

from .user_info import UserInfo
from .audio_info import AudioInfo


@dataclass
class Comment:
    """评论数据模型"""
    comment_id: str
    content: str
    user_info: UserInfo
    like_count: int = 0
    ip_location: str = "未知"
    sub_comment_count: int = 0
    create_time: Optional[datetime] = None
    audio_info: Optional[AudioInfo] = None
    pictures: List[str] = field(default_factory=list)  # 评论图片URL列表
    sub_comments: List['Comment'] = field(default_factory=list)
    target_comment: Optional['Comment'] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Comment':
        """从字典创建实例"""
        user_info = UserInfo.from_dict(data.get('user_info', {}))
        audio_info = AudioInfo.from_dict(data.get('audio_info'))
        
        # 提取图片URL
        pictures = []
        if 'pictures' in data and data['pictures']:
            for pic in data['pictures']:
                if isinstance(pic, dict):
                    # 尝试多种可能的字段名
                    pic_url = (
                        pic.get('url_default') or 
                        pic.get('url') or 
                        pic.get('url_pre') or
                        pic.get('info', {}).get('url') or
                        pic.get('info', {}).get('url_default', '')
                    )
                    if pic_url:
                        pictures.append(pic_url)
                elif isinstance(pic, str):
                    pictures.append(pic)
        
        # 处理子评论
        sub_comments = []
        for sub_data in data.get('sub_comments', []):
            sub_comments.append(cls.from_dict(sub_data))
        
        # 处理目标评论（被回复的评论）
        target_comment = None
        if 'target_comment' in data and data['target_comment']:
            target_comment = cls.from_dict(data['target_comment'])
        
        return cls(
            comment_id=data.get('id', ''),
            content=data.get('content', ''),
            user_info=user_info,
            like_count=int(data.get('like_count', 0)),
            ip_location=data.get('ip_location', '未知'),
            sub_comment_count=int(data.get('sub_comment_count', 0)),
            audio_info=audio_info,
            pictures=pictures,
            sub_comments=sub_comments,
            target_comment=target_comment
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'comment_id': self.comment_id,
            'content': self.content,
            'user_info': {
                'user_id': self.user_info.user_id,
                'nickname': self.user_info.nickname
            },
            'like_count': self.like_count,
            'ip_location': self.ip_location,
            'sub_comment_count': self.sub_comment_count
        }
