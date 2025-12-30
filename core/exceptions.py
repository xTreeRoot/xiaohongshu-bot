"""自定义异常类"""


class XHSPublisherException(Exception):
    """基础异常类"""
    pass


class BrowserInitError(XHSPublisherException):
    """浏览器初始化失败"""
    pass


class ElementNotFoundError(XHSPublisherException):
    """元素未找到"""
    pass


class PublishError(XHSPublisherException):
    """发布失败"""
    pass


class CommentFetchError(XHSPublisherException):
    """评论获取失败"""
    pass


class NetworkError(XHSPublisherException):
    """网络请求失败"""
    pass


class ValidationError(XHSPublisherException):
    """数据验证失败"""
    pass
