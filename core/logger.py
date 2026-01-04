"""日志管理模块"""
import logging
import sys
from typing import Optional
from pathlib import Path


class ColoredFormatter(logging.Formatter):
    """带颜色的日志格式化器"""
    
    # ANSI 颜色代码
    COLORS = {
        'DEBUG': '\033[36m',     # 青色
        'INFO': '\033[32m',      # 绿色
        'WARNING': '\033[33m',   # 黄色
        'ERROR': '\033[31m',     # 红色
        'CRITICAL': '\033[35m',  # 紫色
    }
    RESET = '\033[0m'
    
    def format(self, record):
        """格式化日志记录"""
        # 获取颜色
        color = self.COLORS.get(record.levelname, self.RESET)
        
        # 给日志级别添加颜色
        record.levelname = f"{color}{record.levelname}{self.RESET}"
        
        # 调用父类格式化
        return super().format(record)


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
        
        # 格式化器（控制台使用带颜色的）
        console_formatter = ColoredFormatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # 文件使用普通格式化器（不带颜色代码）
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # 控制台处理器
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
        
        # 文件处理器
        if log_file:
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)
        
        return logger


# 全局日志实例
logger = Logger.get_logger()
