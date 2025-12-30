"""数据模型定义"""
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime


@dataclass
class UserInfo:
    """用户信息"""
    user_id: str = ""
    nickname: str = "未知用户"
    avatar: str = ""
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UserInfo':
        """从字典创建实例"""
        return cls(
            user_id=data.get('user_id', ''),
            nickname=data.get('nickname', '未知用户'),
            avatar=data.get('avatar', '')
        )


@dataclass
class AudioInfo:
    """语音信息"""
    asr_text: str = ""
    tag_text: str = ""
    duration: int = 0
    
    @classmethod
    def from_dict(cls, data: Optional[Dict[str, Any]]) -> Optional['AudioInfo']:
        """从字典创建实例"""
        if not data:
            return None
        return cls(
            asr_text=data.get('asr_text', ''),
            tag_text=data.get('tag_text', ''),
            duration=data.get('duration', 0)
        )


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
