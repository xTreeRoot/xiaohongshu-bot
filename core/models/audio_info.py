"""语音信息模型"""
from dataclasses import dataclass
from typing import Optional, Dict, Any


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
