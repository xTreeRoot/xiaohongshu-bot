"""用户信息模型"""
from dataclasses import dataclass
from typing import Dict, Any


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
