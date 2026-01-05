""" 小红书自动化工具 - 核心模块"""

from core.config import config
from core.logger import logger
from core.browser_manager import BrowserManager
# 注意： XHSClient 不在这里导入，避免循环依赖
# 使用时请直接: from core.xhs_client import XHSClient
from core.models import Comment, NoteInfo, PublishContent, UserInfo, AIConfig
from core.ai_client import BaseAIClient, OpenAIClient, ZhipuAIClient, AIClientFactory
from core.exceptions import (
    XHSPublisherException,
    BrowserInitError,
    ElementNotFoundError,
    PublishError
)

__all__ = [
    'config',
    'logger',
    'BrowserManager',
    # 'XHSClient',  # 已移除，避免循环导入
    'Comment',
    'NoteInfo',
    'PublishContent',
    'UserInfo',
    'AIConfig',
    'BaseAIClient',
    'OpenAIClient',
    'ZhipuAIClient',
    'AIClientFactory',
    'XHSPublisherException',
    'BrowserInitError',
    'ElementNotFoundError',
    'PublishError',
]
