"""笔记管理模块"""
import time
from typing import Optional

from selenium.webdriver.common.by import By

from core.browser_manager import BrowserManager
from core.config import config
from core.decorators import log_execution
from core.logger import logger
from core.models import NoteInfo
from utils import URLExtractor


class NoteManager:
    """笔记管理器 - 负责笔记相关操作（搜索、打开等）"""

    def __init__(self, browser_manager: BrowserManager):
        """初始化笔记管理器
        
        Args:
            browser_manager: 浏览器管理器实例
        """
        self.browser = browser_manager

    @log_execution
    def open_user_profile(self):
        """打开用户个人主页"""
        self.browser.navigate_to(config.xhs.user_profile_url, "个人主页")

    @log_execution
    def search_and_open_note(self, keyword: str) -> Optional[NoteInfo]:
        """在个人主页搜索帖子并打开
        
        Args:
            keyword: 要搜索的帖子标题关键词
            
        Returns:
            打开的帖子信息或None
        """
        try:
            logger.info(f"开始搜索包含关键词 '{keyword}' 的帖子...")

            # 1. 先打开个人主页
            self.open_user_profile()

            # 2. 等待帖子列表加载
            time.sleep(config.wait.page_load_timeout)

            # 3. 查找所有帖子标题
            # 使用DOM缓存功能查找元素
            note_item_selector = config.xhs.selectors["note_item"]
            title_elements = self.browser.driver.find_elements(
                By.CSS_SELECTOR,
                note_item_selector
            )

            logger.info(f" 找到 {len(title_elements)} 个帖子")

            # 4. 遍历所有标题，查找包含关键词的帖子
            for i, title_element in enumerate(title_elements):
                title_text = title_element.text.strip()
                logger.debug(f"  [{i + 1}] {title_text}")

                if keyword in title_text:
                    logger.info(f" 找到匹配的帖子: {title_text}")

                    # 5. 找到对应的链接并点击
                    note_section = title_element.find_element(
                        By.XPATH,
                        "./ancestor::section[@class='note-item']"
                    )

                    # 使用DOM缓存功能查找笔记封面
                    note_cover_selector = config.xhs.selectors["note_cover"]
                    note_link = note_section.find_element(
                        By.CSS_SELECTOR,
                        note_cover_selector
                    )

                    note_url = note_link.get_attribute("href")
                    logger.info(f" 帖子链接: {note_url}")

                    # 6. 点击链接
                    note_link.click()
                    logger.info(" 已点击帖子，等待页面跳转...")

                    # 7. 等待跳转到帖子详情页
                    time.sleep(config.wait.page_load_timeout)

                    # 8. 验证是否成功跳转
                    current_url = self.browser.get_current_url()
                    if "/explore/" in current_url:
                        note_id = URLExtractor.extract_note_id(current_url)
                        logger.info(f" 成功跳转到帖子详情页: {current_url}")

                        return NoteInfo(
                            note_id=note_id or "",
                            title=title_text,
                            url=current_url
                        )
                    else:
                        logger.warning(f"跳转异常，当前URL: {current_url}")
                        return None

            # 如果没找到匹配的帖子
            logger.warning(f"未找到包含关键词 '{keyword}' 的帖子")
            return None

        except Exception as e:
            logger.error(f"搜索帖子时出错: {e}")
            raise