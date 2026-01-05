"""简单DOM管理器测试脚本"""
import os
import sys
from core.logger import logger

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.dom_manager import DOMManager, DOMCacheManager
from core.dom_mapper import DOMElementMapper
from core.models.dom_element import DOMElement
from datetime import datetime


def test_dom_simple():
    """简单测试DOM管理器功能"""
    logger.info("开始简单DOM管理器测试...")
    
    # 1. 测试数据库映射器
    logger.info("\n1. 测试数据库映射器...")
    db_mapper = DOMElementMapper("test_dom_elements.db")
    logger.info("数据库映射器创建成功")
    
    # 2. 测试缓存管理器
    logger.info("\n2. 测试缓存管理器...")
    cache_manager = DOMCacheManager("test_cache")
    logger.info("缓存管理器创建成功")
    
    # 3. 测试DOM管理器
    logger.info("\n3. 测试DOM管理器...")
    dom_manager = DOMManager("test_dom_elements.db", "test_cache")
    logger.info("DOM管理器创建成功")
    
    # 4. 测试插入DOM元素
    logger.info("\n4. 测试插入DOM元素...")
    test_element = DOMElement(
        element_id="test_button",
        selector="#test-button",
        element_type="button",
        position="top-right",
        text_content="测试按钮",
        updated_at=datetime.now(),
        page_url="https://example.com",
        description="测试用按钮元素"
    )
    
    success = dom_manager.insert_element(test_element)
    logger.info(f"插入元素结果: {success}")
    
    # 5. 测试获取DOM元素
    logger.info("\n5. 测试获取DOM元素...")
    retrieved_element = dom_manager.get_element("#test-button")
    if retrieved_element:
        logger.info(f"获取到元素: {retrieved_element.element_id}")
        logger.info(f"选择器: {retrieved_element.selector}")
        logger.info(f"类型: {retrieved_element.element_type}")
        logger.info(f"文本内容: {retrieved_element.text_content}")
        logger.info(f"页面URL: {retrieved_element.page_url}")
    else:
        logger.info("未获取到元素")
    
    # 6. 测试更新DOM元素
    logger.info("\n6. 测试更新DOM元素...")
    updated_element = DOMElement(
        element_id="test_button",
        selector="#test-button",
        element_type="button",
        position="bottom-right",
        text_content="更新后的测试按钮",
        updated_at=datetime.now(),
        page_url="https://example.com",
        description="更新后的测试用按钮元素"
    )
    
    update_success = dom_manager.update_element(updated_element)
    logger.info(f"更新元素结果: {update_success}")
    
    # 再次获取验证更新
    retrieved_element = dom_manager.get_element("#test-button")
    if retrieved_element:
        logger.info(f"更新后元素位置: {retrieved_element.position}")
        logger.info(f"更新后文本内容: {retrieved_element.text_content}")
    
    # 7. 测试批量插入初始元素
    logger.info("\n7. 测试批量插入初始元素...")
    test_selectors = {
        "login_button": "#login-btn",
        "username_input": "input[name='username']",
        "password_input": "input[name='password']",
        "submit_button": "button[type='submit']",
        "text2image_button": "//button[contains(@class, 'text2image-button')]",
        "content_editor": "div.tiptap.ProseMirror",
        "generate_button": "div.edit-text-button",
        "next_button": "button.custom-button.bg-red",
        "title_input": "div.d-input input.d-text",
        "publish_button": "button.publishBtn.red",
        "note_item": "section.note-item .footer .title span",
        "note_cover": "a.cover"
    }
    
    dom_manager.batch_insert_initial_elements(test_selectors, "https://example.com/login")
    logger.info("批量插入初始元素完成")
    
    # 8. 测试从数据库获取批量插入的元素
    logger.info("\n8. 验证批量插入的元素...")
    selectors = dom_manager.mapper.search(element_type="selector")
    logger.info(f"从数据库获取的DOM元素数量: {len(selectors)}")
    
    for selector in selectors:
        logger.info(f"  - {selector.element_id}: {selector.selector}")
    
    # 9. 测试缓存功能
    logger.info("\n9. 测试缓存功能...")
    # 先从数据库获取一个元素
    element = dom_manager.mapper.find_by_selector("#login-btn")
    if element:
        logger.info(f"从数据库获取: {element.element_id}")
    
    # 使用DOM管理器获取（应该从缓存或数据库获取）
    cached_element = dom_manager.get_element("#login-btn")
    if cached_element:
        logger.info(f"通过DOM管理器获取: {cached_element.element_id}")
    
    # 10. 清理测试文件
    logger.info("\n10. 清理测试文件...")
    try:
        os.remove("test_dom_elements.db")
        import shutil
        if os.path.exists("test_cache"):
            shutil.rmtree("test_cache")
        logger.info("测试文件清理完成")
    except:
        logger.info("清理测试文件时出错（可能文件不存在）")
    
    logger.info("\n简单DOM管理器测试完成！")


if __name__ == "__main__":
    test_dom_simple()