"""AI 客户端模块 - 工厂模式"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from .config import config
from .logger import logger
from .exceptions import XHSException
from .models import AIConfig


class BaseAIClient(ABC):
    """AI 客户端抽象基类 - 定义统一接口规范
    
    所有自定义 AI 客户端必须继承此类并实现所有抽象方法。
    这样可以确保不同的 AI 服务都遵循相同的接口规范。
    """
    
    @abstractmethod
    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        发送聊天请求（必须实现）
        
        Args:
            messages: 消息列表，格式 [{"role": "user", "content": "..."}]
                     role 可以是 "system", "user", "assistant"
            temperature: 温度参数（0-2），控制随机性，越高越随机
            max_tokens: 最大生成 token 数
        
        Returns:
            AI 回复的文本内容
            
        Raises:
            XHSException: 当请求失败时抛出
        """
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """
        检查 AI 客户端是否可用（必须实现）
        
        Returns:
            True 如果客户端已正确初始化且可用，否则 False
        """
        pass
    
    def generate_text(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None
    ) -> str:
        """
        生成文本（默认实现，可选覆盖）
        
        这是一个便捷方法，内部调用 chat() 方法。
        子类可以选择覆盖此方法以提供更高效的实现。
        
        Args:
            prompt: 用户提示词
            system_prompt: 系统提示词（可选）
            temperature: 温度参数（可选）
        
        Returns:
            生成的文本
        """
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        return self.chat(messages, temperature=temperature)
    
    def get_client_info(self) -> Dict[str, Any]:
        """
        获取客户端信息（可选实现）
        
        Returns:
            包含客户端信息的字典，如 {"name": "OpenAI", "model": "gpt-3.5-turbo"}
        """
        return {"name": self.__class__.__name__}


class OpenAIClient(BaseAIClient):
    """OpenAI 官方 API 客户端实现
    
    这是默认的 AI 客户端实现，支持 OpenAI 及其兼容 API。
    """
    
    def __init__(self, ai_config: Optional[AIConfig] = None, **kwargs):
        """
        初始化 OpenAI 客户端
        
        Args:
            ai_config: AI 配置对象，为 None 则从参数或配置文件读取
            **kwargs: 单独传入的参数（兼容旧用法）
                api_key: API 密钥
                base_url: API 基础 URL
                model: 模型名称
                temperature: 温度参数
                max_tokens: 最大 token 数
                timeout: 超时时间
        """
        from openai import OpenAI
        
        # 支持两种用法：
        # 1. 直接传入 AIConfig 对象
        # 2. 通过单独参数传入（兼容旧用法）
        if ai_config:
            self.api_key = ai_config.api_key or config.ai.api_key
            self.base_url = ai_config.base_url or config.ai.base_url
            self.model = ai_config.model or config.ai.model
            self.temperature = ai_config.temperature or config.ai.temperature
            self.max_tokens = ai_config.max_tokens or config.ai.max_tokens
            self.timeout = ai_config.timeout or config.ai.timeout
        else:
            # 兼容旧用法
            self.api_key = kwargs.get('api_key') or config.ai.api_key
            self.base_url = kwargs.get('base_url') or config.ai.base_url
            self.model = kwargs.get('model') or config.ai.model
            self.temperature = kwargs.get('temperature') or config.ai.temperature
            self.max_tokens = kwargs.get('max_tokens') or config.ai.max_tokens
            self.timeout = kwargs.get('timeout') or config.ai.timeout
        
        self.client: Optional[OpenAI] = None
        self._init_client()
    
    def _init_client(self):
        """初始化 OpenAI 客户端"""
        from openai import OpenAI
        
        if not self.api_key:
            logger.warning("AI API Key 未配置，AI 功能将无法使用")
            return
        
        try:
            self.client = OpenAI(
                api_key=self.api_key,
                base_url=self.base_url,
                timeout=self.timeout
            )
            logger.info(f" OpenAI 客户端初始化成功 - 模型: {self.model}")
        except Exception as e:
            logger.error(f"OpenAI 客户端初始化失败: {e}")
            raise XHSException(f"OpenAI 客户端初始化失败: {e}")
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        """实现 chat 方法"""
        if not self.client:
            raise XHSException("OpenAI 客户端未初始化，请检查配置")
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature or self.temperature,
                max_tokens=max_tokens or self.max_tokens
            )
            
            content = response.choices[0].message.content
            logger.debug(f"AI 响应: {content[:100]}...")
            return content.strip()
        
        except Exception as e:
            logger.error(f"OpenAI 请求失败: {e}")
            raise XHSException(f"OpenAI 请求失败: {e}")
    
    def is_available(self) -> bool:
        """检查客户端是否可用"""
        return self.client is not None
    
    def get_client_info(self) -> Dict[str, Any]:
        """获取客户端信息"""
        return {
            "name": "OpenAI",
            "model": self.model,
            "base_url": self.base_url
        }


class ZhipuAIClient(BaseAIClient):
    """智谱 AI 客户端实现
    
    支持智谱 AI 的 GLM 系列模型。
    """
    
    def __init__(self, ai_config: Optional[AIConfig] = None, **kwargs):
        """
        初始化智谱 AI 客户端
        
        Args:
            ai_config: AI 配置对象，为 None 则从参数或配置文件读取
            **kwargs: 单独传入的参数（兼容旧用法）
                api_key: API 密钥
                model: 模型名称，默认 glm-4
                temperature: 温度参数
                max_tokens: 最大 token 数
        """
        try:
            from zhipuai import ZhipuAI
        except ImportError:
            raise XHSException("请安装 zhipuai: pip install zhipuai")
        
        # 支持两种用法
        if ai_config:
            self.api_key = ai_config.api_key or config.ai.api_key
            self.model = ai_config.model or config.ai.model if hasattr(config.ai, 'model') else "glm-4"
            self.temperature = ai_config.temperature or config.ai.temperature
            self.max_tokens = ai_config.max_tokens or config.ai.max_tokens
        else:
            # 兼容旧用法
            self.api_key = kwargs.get('api_key') or config.ai.api_key
            self.model = kwargs.get('model') or config.ai.model if hasattr(config.ai, 'model') else "glm-4"
            self.temperature = kwargs.get('temperature') or config.ai.temperature
            self.max_tokens = kwargs.get('max_tokens') or config.ai.max_tokens
        
        self.client: Optional[ZhipuAI] = None
        self._init_client()
    
    def _init_client(self):
        """初始化智谱 AI 客户端"""
        from zhipuai import ZhipuAI
        
        if not self.api_key:
            logger.warning("AI API Key 未配置，AI 功能将无法使用")
            return
        
        try:
            self.client = ZhipuAI(api_key=self.api_key)
            logger.info(f" 智谱 AI 客户端初始化成功 - 模型: {self.model}")
        except Exception as e:
            logger.error(f"智谱 AI 客户端初始化失败: {e}")
            raise XHSException(f"智谱 AI 客户端初始化失败: {e}")
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        """实现 chat 方法"""
        if not self.client:
            raise XHSException("智谱 AI 客户端未初始化，请检查配置")
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature or self.temperature,
                max_tokens=max_tokens or self.max_tokens
            )
            
            content = response.choices[0].message.content
            logger.debug(f"AI 响应: {content[:100]}...")
            return content.strip()
        
        except Exception as e:
            logger.error(f"智谱 AI 请求失败: {e}")
            raise XHSException(f"智谱 AI 请求失败: {e}")
    
    def is_available(self) -> bool:
        """检查客户端是否可用"""
        return self.client is not None
    
    def get_client_info(self) -> Dict[str, Any]:
        """获取客户端信息"""
        return {
            "name": "ZhipuAI",
            "model": self.model,
            "provider": "zhipuai.cn"
        }


class AIClientFactory:
    """
    AI 客户端工厂类
    
    负责创建和管理 AI 客户端实例。
    支持注册自定义客户端实现。
    """
    
    # 已注册的客户端类型
    _clients: Dict[str, type] = {
        "openai": OpenAIClient,
        "zhipu": ZhipuAIClient,
    }
    
    # 默认客户端类型
    # 使用 openai 可以兼容 Ollama 本地模型（通过配置 base_url）
    _default_client = "openai"
    
    @classmethod
    def register_client(cls, name: str, client_class: type):
        """
        注册自定义 AI 客户端
        
        Args:
            name: 客户端名称（如 "custom_ai", "local_llm"）
            client_class: 客户端类，必须继承 BaseAIClient
            
        Raises:
            ValueError: 如果 client_class 不是 BaseAIClient 的子类
            
        Example:
            >>> class MyAI(BaseAIClient):
            ...     def chat(self, messages, temperature=None, max_tokens=None):
            ...         # 你的实现
            ...         pass
            ...     def is_available(self):
            ...         return True
            >>> AIClientFactory.register_client("my_ai", MyAI)
        """
        if not issubclass(client_class, BaseAIClient):
            raise ValueError(f"{client_class} 必须继承 BaseAIClient")
        
        cls._clients[name.lower()] = client_class
        logger.info(f" 已注册 AI 客户端: {name}")
    
    @classmethod
    def set_default_client(cls, name: str):
        """
        设置默认客户端类型
        
        Args:
            name: 客户端名称
            
        Raises:
            ValueError: 如果指定的客户端未注册
        """
        name = name.lower()
        if name not in cls._clients:
            raise ValueError(f"客户端 '{name}' 未注册，可用: {list(cls._clients.keys())}")
        
        cls._default_client = name
        logger.info(f" 设置默认 AI 客户端: {name}")
    
    @classmethod
    def create_client(cls, client_type: Optional[str] = None, **kwargs) -> BaseAIClient:
        """
        创建 AI 客户端实例
        
        Args:
            client_type: 客户端类型，为 None 则使用默认类型
            **kwargs: 传递给客户端构造函数的参数
            
        Returns:
            AI 客户端实例
            
        Raises:
            ValueError: 如果指定的客户端类型未注册
            
        Example:
            >>> client = AIClientFactory.create_client("openai", api_key="sk-xxx")
            >>> client = AIClientFactory.create_client()  # 使用默认
        """
        client_type = (client_type or cls._default_client).lower()
        
        if client_type not in cls._clients:
            raise ValueError(
                f"未知的 AI 客户端类型: {client_type}, "
                f"可用: {list(cls._clients.keys())}"
            )
        
        client_class = cls._clients[client_type]
        return client_class(**kwargs)
    
    @classmethod
    def list_clients(cls) -> List[str]:
        """
        列出所有已注册的客户端类型
        
        Returns:
            客户端名称列表
        """
        return list(cls._clients.keys())


# 为了向后兼容，保留 AIClient 别名
AIClient = OpenAIClient
