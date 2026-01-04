"""装饰器模块"""
import time
import functools
from typing import Callable, Any, Type, Tuple
from core.logger import logger


def retry(max_attempts: int = 3, delay: float = 1.0, 
         exceptions: Tuple[Type[Exception], ...] = (Exception,)):
    """重试装饰器
    
    Args:
        max_attempts: 最大重试次数
        delay: 重试间隔（秒）
        exceptions: 需要重试的异常类型
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exception = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_attempts:
                        logger.warning(
                            f"{func.__name__} 执行失败 (尝试 {attempt}/{max_attempts}): {e}"
                        )
                        time.sleep(delay)
                    else:
                        logger.error(
                            f"{func.__name__} 执行失败，已达最大重试次数 {max_attempts}"
                        )
            raise last_exception
        return wrapper
    return decorator


def log_execution(func: Callable) -> Callable:
    """日志装饰器，记录函数执行"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        logger.debug(f"开始执行: {func.__name__}")
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            elapsed = time.time() - start_time
            logger.debug(f"完成执行: {func.__name__} (耗时: {elapsed:.2f}s)")
            return result
        except Exception as e:
            elapsed = time.time() - start_time
            logger.error(f"执行失败: {func.__name__} (耗时: {elapsed:.2f}s) - {e}")
            raise
    return wrapper
