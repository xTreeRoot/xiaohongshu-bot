"""DOM管理器与浏览器集成测试脚本"""
import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_integration():
    """测试DOM管理器与浏览器的集成"""
    print("开始DOM管理器与浏览器集成测试...")
    
    try:
        # 延迟导入，避免启动浏览器
        from core.dom_manager import DOMManager
        from core.dom_mapper import DOMElementMapper
        from core.models.dom_element import DOMElement
        from datetime import datetime
        
        print("\n1. 测试DOM管理器与浏览器的集成...")
        # 创建DOM管理器
        dom_manager = DOMManager()
        print("DOM管理器创建成功")
        
        # 验证数据库映射器和缓存管理器是否正确初始化
        print(f"数据库映射器: {dom_manager.mapper is not None}")
        print(f"缓存管理器: {dom_manager.cache_manager is not None}")
        
        # 测试初始元素插入
        print("\n2. 测试初始元素插入...")
        from core.config import config
        selectors = config.xhs.selectors
        print(f"配置中的选择器数量: {len(selectors) if selectors else 0}")
        
        if selectors:
            dom_manager.batch_insert_initial_elements(selectors, "https://creator.xiaohongshu.com")
            print("初始元素批量插入完成")
        
        # 测试搜索功能
        print("\n3. 测试搜索功能...")
        all_elements = dom_manager.mapper.find_all()
        print(f"数据库中总元素数量: {len(all_elements)}")
        
        selector_elements = dom_manager.mapper.find_by_type("selector")
        print(f"类型为'selector'的元素数量: {len(selector_elements)}")
        
        for element in selector_elements[:5]:  # 只显示前5个
            print(f"  - {element.element_id}: {element.selector}")
        
        # 测试单个元素的获取、更新、删除
        print("\n4. 测试单个元素操作...")
        if selector_elements:
            first_element = selector_elements[0]
            print(f"获取第一个元素: {first_element.element_id}")
            
            # 测试从缓存获取
            cached_element = dom_manager.get_element(first_element.selector)
            if cached_element:
                print(f"从缓存获取成功: {cached_element.element_id}")
            
            # 测试更新
            updated_element = DOMElement(
                element_id=first_element.element_id,
                selector=first_element.selector,
                element_type=first_element.element_type,
                position="updated_position",
                text_content=first_element.text_content,
                updated_at=datetime.now(),
                page_url=first_element.page_url,
                description=f"Updated: {first_element.description}"
            )
            
            update_success = dom_manager.update_element(updated_element)
            print(f"更新操作结果: {update_success}")
        
        print("\nDOM管理器与浏览器集成测试完成！")
        
    except Exception as e:
        print(f"集成测试出错: {e}")
        import traceback
        traceback.print_exc()


def test_browser_manager_dom_integration():
    """测试BrowserManager中DOM功能的集成"""
    print("\n开始BrowserManager DOM功能测试...")
    
    try:
        # 测试BrowserManager中的DOM功能而不实际启动浏览器
        from core.browser_manager import BrowserManager
        
        # 通过反射或直接方法测试DOM管理器的集成
        # 创建一个BrowserManager实例，但不启动浏览器
        bm = object.__new__(BrowserManager)  # 创建空实例
        
        # 手动初始化DOM管理器
        from core.dom_manager import DOMManager
        bm.dom_manager = DOMManager()
        
        # 测试DOM管理器是否正确初始化
        print(f"BrowserManager DOM管理器已初始化: {hasattr(bm, 'dom_manager')}")
        print(f"DOM管理器类型: {type(bm.dom_manager).__name__}")
        
        # 测试插入和获取元素
        from core.models.dom_element import DOMElement
        from datetime import datetime
        
        test_element = DOMElement(
            element_id="integration_test",
            selector=".integration-test",
            element_type="div",
            position="test_position",
            text_content="Integration test element",
            updated_at=datetime.now(),
            page_url="https://test.com",
            description="Test element for integration"
        )
        
        insert_result = bm.dom_manager.insert_element(test_element)
        print(f"插入测试元素结果: {insert_result}")
        
        get_result = bm.dom_manager.get_element(".integration-test")
        print(f"获取测试元素结果: {get_result is not None}")
        
        if get_result:
            print(f"获取的元素ID: {get_result.element_id}")
        
        print("BrowserManager DOM功能测试完成！")
        
    except Exception as e:
        print(f"BrowserManager DOM功能测试出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_integration()
    test_browser_manager_dom_integration()