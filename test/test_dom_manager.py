"""DOM管理器测试脚本"""
from core.dom_manager import DOMManager
from core.models import DOMElement
from core.logger import logger
from datetime import datetime


def test_dom_manager():
    """测试DOM管理器功能"""
    logger.info("开始测试DOM管理器...")
    
    # 创建DOM管理器实例
    dom_manager = DOMManager()
    
    # 测试插入DOM元素
    logger.info("\n1. 测试插入DOM元素...")
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
    
    # 测试获取DOM元素
    logger.info("\n2. 测试获取DOM元素...")
    retrieved_element = dom_manager.get_element("#test-button")
    if retrieved_element:
        logger.info(f"获取到元素: {retrieved_element.element_id}")
        logger.info(f"选择器: {retrieved_element.selector}")
        logger.info(f"类型: {retrieved_element.element_type}")
        logger.info(f"文本内容: {retrieved_element.text_content}")
    else:
        logger.info("未获取到元素")
    
    # 测试更新DOM元素
    logger.info("\n3. 测试更新DOM元素...")
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
    
    # 测试批量插入初始元素
    logger.info("\n4. 测试批量插入初始元素...")
    test_selectors = {
        "login_button": "#login-btn",
        "username_input": "input[name='username']",
        "password_input": "input[name='password']",
        "submit_button": "button[type='submit']"
    }
    
    dom_manager.batch_insert_initial_elements(test_selectors, "https://example.com/login")
    logger.info("批量插入初始元素完成")
    
    # 测试从数据库获取批量插入的元素
    logger.info("\n5. 验证批量插入的元素...")
    for element_id, selector in test_selectors.items():
        element = dom_manager.get_element(selector)
        if element:
            logger.info(f"  {element_id}: {element.selector}")
        else:
            logger.info(f"  {element_id}: 未找到")
    
    logger.info("\nDOM管理器测试完成！")


def test_with_browser():
    """测试与浏览器管理器集成"""
    logger.info("\n开始测试与浏览器管理器集成...")
    
    from core.xhs_client import XHSClient
    
    try:
        # 创建XHS客户端（会自动初始化DOM管理器）
        client = XHSClient()
        
        # 检查DOM管理器是否正确集成
        logger.info(f"DOM管理器已集成: {hasattr(client, 'dom')}")
        
        # 获取初始配置中的DOM元素
        selectors = client.browser.dom_manager.db_manager.search_elements(element_type="selector")
        logger.info(f"从配置中加载的DOM元素数量: {len(selectors)}")
        
        for selector in selectors:
            logger.info(f"  - {selector.element_id}: {selector.selector}")
        
        # 关闭浏览器
        client.quit()
        
    except Exception as e:
        logger.error(f"集成测试出错: {e}")


if __name__ == "__main__":
    test_dom_manager()
    test_with_browser()