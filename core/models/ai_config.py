"""AI 配置模型"""
from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class AIConfig:
    """AI 客户端配置"""
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    model: Optional[str] = None
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    timeout: Optional[int] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AIConfig':
        """从字典创建实例"""
        return cls(
            api_key=data.get('api_key'),
            base_url=data.get('base_url'),
            model=data.get('model'),
            temperature=data.get('temperature'),
            max_tokens=data.get('max_tokens'),
            timeout=data.get('timeout')
        )
