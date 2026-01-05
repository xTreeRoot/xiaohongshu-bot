"""DOM管理器测试脚本"""
from core.dom_manager import DOMManager
from core.models import DOMElement
from datetime import datetime


def test_dom_manager():
    """测试DOM管理器功能"""
    print("开始测试DOM管理器...")
    
    # 创建DOM管理器实例
    dom_manager = DOMManager()
    
    # 测试插入DOM元素
    print("\n1. 测试插入DOM元素...")
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
    print(f"插入元素结果: {success}")
    
    # 测试获取DOM元素
    print("\n2. 测试获取DOM元素...")
    retrieved_element = dom_manager.get_element("#test-button")
    if retrieved_element:
        print(f"获取到元素: {retrieved_element.element_id}")
        print(f"选择器: {retrieved_element.selector}")
        print(f"类型: {retrieved_element.element_type}")
        print(f"文本内容: {retrieved_element.text_content}")
    else:
        print("未获取到元素")
    
    # 测试更新DOM元素
    print("\n3. 测试更新DOM元素...")
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
    print(f"更新元素结果: {update_success}")
    
    # 再次获取验证更新
    retrieved_element = dom_manager.get_element("#test-button")
    if retrieved_element:
        print(f"更新后元素位置: {retrieved_element.position}")
        print(f"更新后文本内容: {retrieved_element.text_content}")
    
    # 测试批量插入初始元素
    print("\n4. 测试批量插入初始元素...")
    test_selectors = {
        "login_button": "#login-btn",
        "username_input": "input[name='username']",
        "password_input": "input[name='password']",
        "submit_button": "button[type='submit']"
    }
    
    dom_manager.batch_insert_initial_elements(test_selectors, "https://example.com/login")
    print("批量插入初始元素完成")
    
    # 测试从数据库获取批量插入的元素
    print("\n5. 验证批量插入的元素...")
    for element_id, selector in test_selectors.items():
        element = dom_manager.get_element(selector)
        if element:
            print(f"  {element_id}: {element.selector}")
        else:
            print(f"  {element_id}: 未找到")
    
    print("\nDOM管理器测试完成！")


def test_with_browser():
    """测试与浏览器管理器集成"""
    print("\n开始测试与浏览器管理器集成...")
    
    from core.xhs_client import XHSClient
    
    try:
        # 创建XHS客户端（会自动初始化DOM管理器）
        client = XHSClient()
        
        # 检查DOM管理器是否正确集成
        print(f"DOM管理器已集成: {hasattr(client, 'dom')}")
        
        # 获取初始配置中的DOM元素
        selectors = client.browser.dom_manager.db_manager.search_elements(element_type="selector")
        print(f"从配置中加载的DOM元素数量: {len(selectors)}")
        
        for selector in selectors:
            print(f"  - {selector.element_id}: {selector.selector}")
        
        # 关闭浏览器
        client.quit()
        
    except Exception as e:
        print(f"集成测试出错: {e}")


if __name__ == "__main__":
    test_dom_manager()
    test_with_browser()