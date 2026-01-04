"""
自定义 AI 客户端示例

此文件展示如何实现自定义 AI 客户端并集成到系统中。
fork 本项目的开发者可以参考此示例来接入自己的 AI 服务。
"""
from typing import List, Dict, Optional
from core import BaseAIClient, AIClientFactory
from core.exceptions import XHSException
from core.logger import logger


class CustomAIClient(BaseAIClient):
    """
    自定义 AI 客户端实现示例
    
    这是一个示例实现，展示了如何创建符合规范的 AI 客户端。
    你需要实现 chat() 和 is_available() 两个必须的方法。
    """
    
    def __init__(self, api_key: str, api_url: str = "https://your-ai-service.com/api", **kwargs):
        """
        初始化自定义 AI 客户端
        
        Args:
            api_key: 你的 AI 服务 API 密钥
            api_url: AI 服务的 API 地址
            **kwargs: 其他自定义参数
        """
        self.api_key = api_key
        self.api_url = api_url
        self.model = kwargs.get("model", "your-default-model")
        self.temperature = kwargs.get("temperature", 0.9)
        self.max_tokens = kwargs.get("max_tokens", 300)
        
        # 初始化你的客户端
        self.is_initialized = self._init_client()
    
    def _init_client(self) -> bool:
        """初始化客户端连接（内部方法）"""
        try:
            # 在这里初始化你的 AI 服务连接
            # 例如：验证 API key，建立连接等
            
            if not self.api_key:
                logger.warning("自定义 AI 客户端：API Key 未配置")
                return False
            
            # 这里可以添加连接测试代码
            logger.info(f" 自定义 AI 客户端初始化成功 - 模型: {self.model}")
            return True
            
        except Exception as e:
            logger.error(f"自定义 AI 客户端初始化失败: {e}")
            return False
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        实现 chat 方法（必须）
        
        这是核心方法，用于与 AI 服务通信。
        
        Args:
            messages: 消息列表，格式 [{"role": "user", "content": "..."}]
            temperature: 温度参数
            max_tokens: 最大 token 数
        
        Returns:
            AI 生成的文本
        """
        if not self.is_initialized:
            raise XHSException("自定义 AI 客户端未初始化")
        
        try:
            # 方式 1: 如果你的 AI 服务提供 HTTP API
            import requests
            
            # 构建请求
            payload = {
                "model": self.model,
                "messages": messages,
                "temperature": temperature or self.temperature,
                "max_tokens": max_tokens or self.max_tokens
            }
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            # 发送请求
            response = requests.post(
                f"{self.api_url}/chat/completions",
                json=payload,
                headers=headers,
                timeout=30
            )
            
            response.raise_for_status()
            result = response.json()
            
            # 从响应中提取文本（根据你的 API 格式调整）
            content = result["choices"][0]["message"]["content"]
            logger.debug(f"自定义 AI 响应: {content[:100]}...")
            return content.strip()
            
            # 方式 2: 如果你使用本地模型或其他 SDK
            # from your_ai_sdk import YourAIClient
            # client = YourAIClient(api_key=self.api_key)
            # response = client.generate(messages=messages, ...)
            # return response.text
            
        except Exception as e:
            logger.error(f"自定义 AI 请求失败: {e}")
            raise XHSException(f"自定义 AI 请求失败: {e}")
    
    def is_available(self) -> bool:
        """
        检查客户端是否可用（必须）
        
        Returns:
            True 如果客户端已初始化且可用
        """
        return self.is_initialized
    
    def get_client_info(self) -> Dict:
        """
        获取客户端信息（可选，但建议实现）
        
        Returns:
            包含客户端信息的字典
        """
        return {
            "name": "CustomAI",
            "model": self.model,
            "api_url": self.api_url
        }


class LocalLLMClient(BaseAIClient):
    """
    本地大模型客户端示例
    
    适用于使用 Ollama、llama.cpp 等本地部署的模型
    """
    
    def __init__(self, model_name: str = "llama2", host: str = "http://localhost:11434"):
        """
        初始化本地 LLM 客户端
        
        Args:
            model_name: 模型名称（如 "llama2", "mistral"）
            host: Ollama 服务地址
        """
        self.model_name = model_name
        self.host = host
        self.is_initialized = True
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        """实现本地模型的 chat 方法"""
        try:
            import requests
            
            # Ollama API 格式
            prompt = self._messages_to_prompt(messages)
            
            response = requests.post(
                f"{self.host}/api/generate",
                json={
                    "model": self.model_name,
                    "prompt": prompt,
                    "temperature": temperature or 0.9,
                    "stream": False
                },
                timeout=60
            )
            
            response.raise_for_status()
            result = response.json()
            return result["response"].strip()
            
        except Exception as e:
            logger.error(f"本地 LLM 请求失败: {e}")
            raise XHSException(f"本地 LLM 请求失败: {e}")
    
    def _messages_to_prompt(self, messages: List[Dict[str, str]]) -> str:
        """将消息列表转换为单个 prompt"""
        prompt_parts = []
        for msg in messages:
            role = msg["role"]
            content = msg["content"]
            if role == "system":
                prompt_parts.append(f"System: {content}")
            elif role == "user":
                prompt_parts.append(f"User: {content}")
            elif role == "assistant":
                prompt_parts.append(f"Assistant: {content}")
        
        prompt_parts.append("Assistant:")
        return "\n\n".join(prompt_parts)
    
    def is_available(self) -> bool:
        """检查本地服务是否可用"""
        try:
            import requests
            response = requests.get(f"{self.host}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def get_client_info(self) -> Dict:
        return {
            "name": "LocalLLM",
            "model": self.model_name,
            "host": self.host
        }


def main():
    """主函数 - 演示如何使用自定义 AI 客户端"""
    
    logger.info("\n" + "="*60)
    logger.info("示例 1: 注册自定义 AI 客户端")
    logger.info("="*60)
    
    # 1. 注册自定义 AI 客户端
    AIClientFactory.register_client("custom", CustomAIClient)
    AIClientFactory.register_client("local-llm", LocalLLMClient)
    
    logger.info(f"可用的 AI 客户端: {AIClientFactory.list_clients()}")
    
    # 2. 使用工厂创建客户端
    try:
        # 创建自定义客户端
        client = AIClientFactory.create_client(
            "custom",
            api_key="your-api-key-here",
            api_url="https://your-ai-service.com/api"
        )
        logger.info(f"创建成功: {client.get_client_info()}")
    except Exception as e:
        logger.error(f"创建失败: {e}")
    
    # ===== 示例 2: 在 AIManager 中使用 =====
    
    logger.info("\n" + "="*60)
    logger.info("示例 2: 在 AIManager 中使用自定义客户端")
    logger.info("="*60)
    
    # 方式 1: 通过工厂创建
    # manager1 = AIManager(client_type="custom")
    
    # 方式 2: 直接传入客户端实例
    # client = CustomAIClient(api_key="your-key")
    # manager2 = AIManager(client=client)
    
    logger.info("两种方式都可以使用自定义 AI")
    
    # ===== 示例 3: 本地模型 =====
    
    logger.info("\n" + "="*60)
    logger.info("示例 3: 使用本地大模型（Ollama）")
    logger.info("="*60)
    
    # 使用本地 Ollama 模型
    # client = AIClientFactory.create_client(
    #     "local-llm",
    #     model_name="llama2",
    #     host="http://localhost:11434"
    # )
    # manager = AIManager(client=client)
    
    logger.info(f"本地模型客户端: {client.get_client_info()}")
    
    # ===== 使用说明 =====
    
    logger.info("\n" + "="*60)
    logger.info("自定义 AI 客户端示例")
    logger.info("\n此文件展示了如何实现和注册自定义 AI 客户端")
    logger.info("fork 本项目后，你可以：")
    logger.info("1. 继承 BaseAIClient 类")
    logger.info("2. 实现 chat() 和 is_available() 方法")
    logger.info("3. 使用 AIClientFactory.register_client() 注册")
    logger.info("4. 在 AIManager 中使用你的自定义客户端")
    logger.info("="*60)


if __name__ == "__main__":
    try:
        main()
        logger.info("\n示例完成")
    except Exception as e:
        logger.error(f"\n运行示例时出错: {e}")
        import traceback
        traceback.print_exc()
