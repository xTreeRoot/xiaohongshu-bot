"""发布管理模块"""
import time

from selenium.webdriver.common.by import By

from core.browser_manager import BrowserManager
from core.config import config
from core.decorators import log_execution
from core.exceptions import PublishError
from core.logger import logger
from core.models import PublishContent
from utils import DataValidator


class PublishManager:
    """发布管理器 - 负责内容发布相关操作"""

    def __init__(self, browser_manager: BrowserManager):
        """初始化发布管理器
        
        Args:
            browser_manager: 浏览器管理器实例
        """
        self.browser = browser_manager

    @log_execution
    def open_publish_page(self):
        """打开小红书创作者平台发布页"""
        self.browser.navigate_to(config.xhs.publish_url, "发布页面")

    @log_execution
    def create_text_to_image(self, content: str) -> bool:
        """文字生成图片
        
        Args:
            content: 要生成图片的文字内容
            
        Returns:
            是否成功
        """
        try:
            # 点击文字生成图片按钮
            self.browser.click_element(
                By.XPATH,
                config.xhs.selectors["text2image_button"],
                "文字生成图片按钮"
            )
            time.sleep(1)

            # 输入内容
            self.browser.input_text(
                By.CSS_SELECTOR,
                config.xhs.selectors["content_editor"],
                content,
                "内容编辑器"
            )
            time.sleep(1)

            # 点击生成图片按钮
            self.browser.click_element(
                By.CSS_SELECTOR,
                config.xhs.selectors["generate_button"],
                "生成图片按钮"
            )

            logger.info("等待图片生成...")
            time.sleep(config.wait.image_generation_wait)
            return True
        except Exception as e:
            logger.error(f"文字生成图片失败: {e}")
            raise PublishError(f"文字生成图片失败: {e}")

    @log_execution
    def proceed_to_publish_page(self) -> bool:
        """进入发布页面
        
        Returns:
            是否成功
        """
        try:
            self.browser.click_element(
                By.CSS_SELECTOR,
                config.xhs.selectors["next_button"],
                "下一步按钮"
            )
            logger.info("等待跳转到发布页面...")
            time.sleep(config.wait.page_load_timeout)
            return True
        except Exception as e:
            logger.error(f"进入发布页面失败: {e}")
            raise PublishError(f"进入发布页面失败: {e}")

    @log_execution
    def fill_and_publish(self, title: str, description: str = "") -> bool:
        """填写标题和描述并发布
        
        Args:
            title: 标题
            description: 描述（可选）
            
        Returns:
            是否成功
        """
        try:
            # 填写标题
            self.browser.input_text(
                By.CSS_SELECTOR,
                config.xhs.selectors["title_input"],
                title,
                "标题输入框"
            )
            time.sleep(1)

            # 点击发布按钮
            self.browser.click_element(
                By.CSS_SELECTOR,
                config.xhs.selectors["publish_button"],
                "发布按钮"
            )

            logger.info(" 发布成功！")
            return True
        except Exception as e:
            logger.error(f"发布失败: {e}")
            raise PublishError(f"发布失败: {e}")

    @log_execution
    def publish_workflow(self, publish_content: PublishContent) -> bool:
        """完整的发布流程
        
        Args:
            publish_content: 发布内容对象
            
        Returns:
            是否发布成功
        """
        try:
            # 验证内容
            if not DataValidator.validate_publish_content(
                    publish_content.content,
                    publish_content.title
            ):
                raise PublishError("内容验证失败")

            logger.info("\n" + "=" * 50)
            logger.info("开始小红书自动发布流程")
            logger.info("=" * 50 + "\n")

            # 1. 打开发布页
            self.open_publish_page()

            # 2. 文字生成图片
            self.create_text_to_image(publish_content.content)

            # 3. 进入发布页面
            self.proceed_to_publish_page()

            # 4. 填写并发布
            self.fill_and_publish(
                publish_content.title,
                publish_content.description
            )

            logger.info("\n" + "=" * 50)
            logger.info(" 所有步骤完成")
            logger.info("=" * 50 + "\n")
            return True

        except Exception as e:
            logger.error(f"发布流程出错: {e}")
            raise PublishError(f"发布流程出错: {e}")
