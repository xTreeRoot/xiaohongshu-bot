"""日志管理模块"""
import logging
import sys
from typing import Optional
from pathlib import Path


class Logger:
    """统一日志管理器"""
    
    _instance: Optional[logging.Logger] = None
    
    @classmethod
    def get_logger(cls, name: str = "XHSPublisher", log_file: Optional[str] = None) -> logging.Logger:
        """获取日志实例（单例模式）"""
        if cls._instance is None:
            cls._instance = cls._create_logger(name, log_file)
        return cls._instance
    
    @classmethod
    def _create_logger(cls, name: str, log_file: Optional[str]) -> logging.Logger:
        """创建日志记录器"""
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        
        # 避免重复添加handler
        if logger.handlers:
            return logger
        
        # 格式化器
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # 控制台处理器
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        # 文件处理器
        if log_file:
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        
        return logger


# 全局日志实例
logger = Logger.get_logger()
