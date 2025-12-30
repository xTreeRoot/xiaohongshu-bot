"""配置管理模块"""
import os
from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class BrowserConfig:
    """浏览器配置"""
    # 用户数据目录
    user_data_dir: str = "~/selenium_chrome_data"
    # 窗口大小
    window_size: str = "--start-maximized"
    # 禁用自动化
    disable_automation: bool = True
    # 无头模式
    headless: bool = False
    
    def get_user_data_dir(self) -> str:
        """获取展开后的用户数据目录"""
        return os.path.expanduser(self.user_data_dir)


@dataclass
class WaitConfig:
    """等待时间配置"""
    default_timeout: int = 10
    element_timeout: int = 10
    page_load_timeout: int = 3
    action_delay: float = 0.5
    input_delay: float = 0.3
    image_generation_wait: int = 5


@dataclass
class XHSConfig:
    """小红书平台配置"""
    #发布页
    publish_url: str = "https://creator.xiaohongshu.com/publish/publish?from=menu&target=image"
    # 我的页（请替换为你的个人主页URL）
    user_profile_url: str = "https://www.xiaohongshu.com/user/profile/YOUR_USER_ID"
    # 评论接口
    comment_api_pattern: str = "api/sns/web/v2/comment/page"
    
    # CSS选择器
    selectors: Dict[str, str] = None
    
    def __post_init__(self):
        if self.selectors is None:
            self.selectors = {
                "text2image_button": "//button[contains(@class, 'text2image-button')]",
                "content_editor": "div.tiptap.ProseMirror",
                "generate_button": "div.edit-text-button",
                "next_button": "button.custom-button.bg-red",
                "title_input": "div.d-input input.d-text",
                "publish_button": "button.publishBtn.red",
                "note_item": "section.note-item .footer .title span",
                "note_cover": "a.cover"
            }


@dataclass
class AppConfig:
    """应用总配置"""
    browser: BrowserConfig = None
    wait: WaitConfig = None
    xhs: XHSConfig = None
    
    def __post_init__(self):
        if self.browser is None:
            self.browser = BrowserConfig()
        if self.wait is None:
            self.wait = WaitConfig()
        if self.xhs is None:
            self.xhs = XHSConfig()


# 全局配置实例
config = AppConfig()

# 尝试加载个人配置文件（如果存在）
try:
    import sys
    from pathlib import Path
    
    # 获取项目根目录
    root_dir = Path(__file__).parent.parent
    sys.path.insert(0, str(root_dir))
    
    from config_personal import PERSONAL_CONFIG
    
    # 应用个人配置
    if "user_profile_url" in PERSONAL_CONFIG:
        config.xhs.user_profile_url = PERSONAL_CONFIG["user_profile_url"]
    if "chrome_user_data_dir" in PERSONAL_CONFIG:
        config.browser.user_data_dir = PERSONAL_CONFIG["chrome_user_data_dir"]
    if "headless" in PERSONAL_CONFIG:
        config.browser.headless = PERSONAL_CONFIG["headless"]
    if "wait_timeout" in PERSONAL_CONFIG:
        config.wait.default_timeout = PERSONAL_CONFIG["wait_timeout"]
    if "page_load_timeout" in PERSONAL_CONFIG:
        config.wait.page_load_timeout = PERSONAL_CONFIG["page_load_timeout"]
    
    print("✓ 已加载个人配置文件")
except ImportError:
    # 个人配置文件不存在，使用默认配置
    pass
except Exception as e:
    print(f"  加载个人配置文件失败: {e}")
    print("将使用默认配置")
