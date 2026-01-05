"""浏览器管理模块"""
import time
from typing import Optional

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from core.config import config
from core.decorators import retry, log_execution
from core.exceptions import BrowserInitError, ElementNotFoundError
from core.logger import logger


class BrowserManager:
    """浏览器管理器 - 负责浏览器初始化和基础操作"""

    def __init__(self):
        """初始化浏览器管理器"""
        self.driver: Optional[webdriver.Chrome] = None
        self.wait: Optional[WebDriverWait] = None
        # 延迟导入DOMManager以避免循环导入
        from core.dom_manager import DOMManager
        self.dom_manager: DOMManager = DOMManager()  # 添加DOM管理器
        self._init_driver()

    def _init_driver(self):
        """配置并启动Chrome浏览器"""
        try:
            options = webdriver.ChromeOptions()

            # 浏览器配置
            options.add_argument(config.browser.window_size)
            options.add_argument(f"user-data-dir={config.browser.get_user_data_dir()}")

            if config.browser.disable_automation:
                options.add_argument("--disable-blink-features=AutomationControlled")
                options.add_experimental_option("excludeSwitches", ["enable-automation"])
                options.add_experimental_option('useAutomationExtension', False)

            if config.browser.headless:
                options.add_argument("--headless")

            # 启用网络日志
            options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})

            self.driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=options
            )
            self.wait = WebDriverWait(self.driver, config.wait.default_timeout)

            # 初始化DOM元素到数据库
            self._init_dom_elements()

            logger.info("浏览器初始化成功")
        except Exception as e:
            logger.error(f"浏览器初始化失败: {e}")
            raise BrowserInitError(f"浏览器初始化失败: {e}")

    def _init_dom_elements(self):
        """初始化DOM元素到数据库"""
        # 从配置中的选择器初始化DOM元素
        selectors = config.xhs.selectors
        if selectors:
            self.dom_manager.batch_insert_initial_elements(selectors, self.get_current_url())
            logger.info(f"已初始化 {len(selectors)} 个DOM元素到数据库")

    def find_element(self, by, value, timeout=None, clickable=False, element_description=None):
        """查找元素，支持等待，优先从缓存/数据库获取
        
        Args:
            by: 查找方式
            value: 查找值
            timeout: 超时时间
            clickable: 是否等待可点击
            element_description: 元素描述，用于缓存和日志
            
        Returns:
            找到的元素
        """
        if timeout is None:
            timeout = config.wait.element_timeout

        # 尝试从DOM管理器获取元素信息
        dom_element = None
        if element_description:
            dom_element = self.dom_manager.get_element(value)
        
        try:
            if clickable:
                element = WebDriverWait(self.driver, timeout).until(
                    EC.element_to_be_clickable((by, value))
                )
            else:
                element = WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located((by, value))
                )
            
            # 如果找到了元素且有描述，更新DOM信息到数据库
            if element_description and element:
                from core.models import DOMElement
                from datetime import datetime
                
                # 获取元素的其他信息
                element_type = element.tag_name if hasattr(element, 'tag_name') else 'unknown'
                text_content = element.text if hasattr(element, 'text') else ''
                page_url = self.get_current_url()
                
                # 如果之前没有在数据库中找到该元素，则插入新记录
                if not dom_element:
                    new_dom_element = DOMElement(
                        element_id=element_description,
                        selector=value,
                        element_type=element_type,
                        text_content=text_content,
                        updated_at=datetime.now(),
                        page_url=page_url,
                        description=element_description
                    )
                    self.dom_manager.insert_element(new_dom_element)
                else:
                    # 如果数据库中已有该元素，更新信息
                    updated_dom_element = DOMElement(
                        element_id=dom_element.element_id,
                        selector=dom_element.selector,
                        element_type=element_type,
                        text_content=text_content,
                        updated_at=datetime.now(),
                        page_url=page_url,
                        description=dom_element.description
                    )
                    self.dom_manager.update_element(updated_dom_element)
            
            return element
        except Exception as e:
            logger.error(f"查找元素失败 [{value}]: {e}")
            raise ElementNotFoundError(f"元素未找到: {value}")

    @retry(max_attempts=2, delay=1.0)
    def find_element_with_dom_cache(self, selector, timeout=None, clickable=False, element_description=None):
        """使用DOM缓存查找元素
        
        Args:
            selector: 选择器（CSS或XPath）
            timeout: 超时时间
            clickable: 是否等待可点击
            element_description: 元素描述
            
        Returns:
            找到的元素
        """
        if timeout is None:
            timeout = config.wait.element_timeout

        # 优先从DOM管理器获取元素信息
        dom_element = self.dom_manager.get_element(selector)
        actual_selector = dom_element.selector if dom_element else selector

        try:
            if clickable:
                element = WebDriverWait(self.driver, timeout).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR if actual_selector.startswith('.') else By.XPATH, actual_selector))
                )
            else:
                element = WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR if actual_selector.startswith('.') else By.XPATH, actual_selector))
                )
            
            # 更新DOM元素信息
            if dom_element:
                from core.models import DOMElement
                from datetime import datetime
                
                element_type = element.tag_name if hasattr(element, 'tag_name') else 'unknown'
                text_content = element.text if hasattr(element, 'text') else ''
                page_url = self.get_current_url()
                
                updated_dom_element = DOMElement(
                    element_id=dom_element.element_id,
                    selector=actual_selector,
                    element_type=element_type,
                    text_content=text_content,
                    updated_at=datetime.now(),
                    page_url=page_url,
                    description=element_description or dom_element.description
                )
                self.dom_manager.update_element(updated_dom_element)
            
            return element
        except Exception as e:
            logger.error(f"使用DOM缓存查找元素失败 [{actual_selector}]: {e}")
            # 如果缓存中的选择器失败，尝试原始选择器
            if actual_selector != selector:
                logger.info(f"尝试原始选择器: {selector}")
                return self.find_element(By.CSS_SELECTOR if selector.startswith('.') else By.XPATH, selector, timeout, clickable)
            raise ElementNotFoundError(f"元素未找到: {selector}")

    @log_execution
    def click_element(self, by, value, description="元素"):
        """点击元素
        
        Args:
            by: 查找方式
            value: 查找值
            description: 元素描述
            
        Returns:
            是否成功
        """
        element = self.find_element(by, value, clickable=True, element_description=description)
        # 滚动到元素可见
        ActionChains(self.driver).move_to_element(element).perform()
        time.sleep(config.wait.action_delay)
        element.click()
        logger.info(f"已点击 '{description}'")
        return True

    @log_execution
    def input_text(self, by, value, text, description="输入框"):
        """输入文本
        
        Args:
            by: 查找方式
            value: 查找值
            text: 输入文本
            description: 元素描述
            
        Returns:
            是否成功
        """
        element = self.find_element(by, value, element_description=description)
        element.click()
        time.sleep(config.wait.input_delay)
        element.clear()
        element.send_keys(text)
        logger.info(f"已在 '{description}' 输入: {text}")
        return True

    def navigate_to(self, url: str, description: str = "页面"):
        """导航到指定URL
        
        Args:
            url: 目标URL
            description: 页面描述
        """
        self.driver.get(url)
        logger.info(f"已打开{description}: {url}")
        time.sleep(config.wait.page_load_timeout)

    def get_current_url(self) -> str:
        """获取当前URL"""
        return self.driver.current_url

    def get_network_logs(self):
        """获取浏览器网络日志"""
        return self.driver.get_log('performance')

    def execute_script(self, script: str, *args):
        """执行JavaScript脚本"""
        return self.driver.execute_script(script, *args)

    def execute_cdp_cmd(self, cmd: str, params: dict):
        """执行Chrome DevTools协议命令"""
        return self.driver.execute_cdp_cmd(cmd, params)

    def quit(self):
        """退出浏览器"""
        if self.driver:
            self.driver.quit()
            logger.info("浏览器已关闭")