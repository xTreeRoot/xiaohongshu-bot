"""小红书客户端 - 整合所有管理器"""
from typing import Optional, List

from core.browser_manager import BrowserManager
from core.dom_manager import DOMManager
from core.logger import logger
from core.models import PublishContent, NoteInfo


class XHSClient:
    """小红书客户端 - 提供统一的API接口"""

    def __init__(self):
        """初始化客户端"""
        # 延迟导入，避免循环依赖
        from business.comment_manager import CommentManager
        from business.note_manager import NoteManager
        from business.publish_manager import PublishManager
        
        # 初始化浏览器管理器
        self.browser = BrowserManager()
        
        # 初始化各功能管理器
        self.note = NoteManager(self.browser)
        self.comment = CommentManager(self.browser)
        self.publish = PublishManager(self.browser)
        
        # 初始化DOM管理器
        self.dom = self.browser.dom_manager
        
        logger.info("小红书客户端初始化完成")

    # ==================== 笔记相关方法 ====================
    
    def search_and_open_note(self, keyword: str) -> Optional[NoteInfo]:
        """搜索并打开笔记
        
        Args:
            keyword: 搜索关键词
            
        Returns:
            笔记信息或None
        """
        return self.note.search_and_open_note(keyword)

    # ==================== 评论相关方法 ====================
    
    def get_comments(self, note_id: str = None, enable_scroll: bool = False, 
                    scroll_count: int = 3) -> List:
        """获取评论列表
        
        Args:
            note_id: 笔记ID（可选，不提供则从当前URL提取）
            enable_scroll: 是否启用滚动加载
            scroll_count: 滚动次数
            
        Returns:
            评论列表
        """
        return self.comment.fetch_comments(
            note_id=note_id,
            enable_scroll=enable_scroll,
            scroll_count=scroll_count
        )
    
    def print_comments(self, comments: List):
        """打印评论列表
        
        Args:
            comments: 评论列表
        """
        self.comment.print_comments(comments)
    
    def reply_comment(self, comment_id: str, reply_text: str) -> bool:
        """回复评论
        
        Args:
            comment_id: 评论ID
            reply_text: 回复内容
            
        Returns:
            是否成功
        """
        return self.comment.reply_to_comment(comment_id, reply_text)

    # ==================== 发布相关方法 ====================
    
    def publish_content(self, publish_content: PublishContent) -> bool:
        """发布内容
        
        Args:
            publish_content: 发布内容对象
            
        Returns:
            是否成功
        """
        return self.publish.publish_workflow(publish_content)

    # ==================== DOM管理相关方法 ====================
    
    def get_dom_element(self, selector: str):
        """获取DOM元素信息
        
        Args:
            selector: CSS选择器或XPath
            
        Returns:
            DOM元素信息
        """
        return self.dom.get_element(selector)
    
    def update_dom_element(self, element_info):
        """更新DOM元素信息
        
        Args:
            element_info: DOM元素信息
            
        Returns:
            是否更新成功
        """
        return self.dom.update_element(element_info)

    # ==================== 通用方法 ====================
    
    def quit(self):
        """关闭客户端"""
        self.browser.quit()
        logger.info("小红书客户端已关闭")