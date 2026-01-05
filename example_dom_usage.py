"""DOM管理器使用示例"""
from core.dom_manager import DOMManager
from core.dom_mapper import DOMElementMapper
from core.models import DOMElement
from datetime import datetime


def example_basic_usage():
    """基本使用示例"""
    print("=== DOM管理器基本使用示例 ===")
    
    # 创建DOM管理器实例
    dom_manager = DOMManager()
    
    # 创建一个DOM元素
    element = DOMElement(
        element_id="example_button",
        selector="#example-btn",
        element_type="button",
        position="top-left",
        text_content="示例按钮",
        updated_at=datetime.now(),
        page_url="https://example.com",
        description="这是一个示例DOM元素"
    )
    
    # 插入元素到数据库
    success = dom_manager.insert_element(element)
    print(f"插入元素成功: {success}")
    
    # 从数据库获取元素（会自动缓存）
    retrieved_element = dom_manager.get_element("#example-btn")
    if retrieved_element:
        print(f"获取元素成功: {retrieved_element.element_id}")
        print(f"元素描述: {retrieved_element.description}")
    
    # 更新元素
    element.text_content = "更新后的示例按钮"
    update_success = dom_manager.update_element(element)
    print(f"更新元素成功: {update_success}")


def example_with_config_selectors():
    """使用配置中的选择器示例"""
    print("\n=== 使用配置中选择器的示例 ===")
    
    from core.config import config
    dom_manager = DOMManager()
    
    # 获取配置中的选择器
    selectors = config.xhs.selectors
    print(f"配置中包含 {len(selectors)} 个选择器")
    
    # 批量插入配置中的选择器到数据库
    dom_manager.batch_insert_initial_elements(selectors, "https://creator.xiaohongshu.com")
    print("已将配置中的选择器批量插入到数据库")
    
    # 显示部分插入的元素
    inserted_elements = dom_manager.mapper.find_by_type("selector")
    print(f"数据库中找到 {len(inserted_elements)} 个选择器元素")
    
    for element in inserted_elements[:5]:  # 只显示前5个
        print(f"  - {element.element_id}: {element.selector}")


def example_batch_operations():
    """批量操作示例"""
    print("\n=== 批量操作示例 ===")
    
    dom_manager = DOMManager()
    
    # 模拟一些选择器
    selectors = {
        "login_form": "form#login-form",
        "username_field": "input#username",
        "password_field": "input#password", 
        "remember_me": "input#remember-me",
        "login_button": "button#login-btn"
    }
    
    # 批量插入初始元素
    dom_manager.batch_insert_initial_elements(selectors, "https://example.com/login")
    print("批量插入登录页面元素完成")
    
    # 搜索特定类型的元素
    login_elements = dom_manager.mapper.find_by_type("input")
    print(f"找到 {len(login_elements)} 个input类型的元素")
    
    for element in login_elements:
        print(f"  - {element.element_id}: {element.selector}")


def example_cache_behavior():
    """缓存行为示例"""
    print("\n=== 缓存行为示例 ===")
    
    dom_manager = DOMManager()
    
    # 首次获取元素（从数据库）
    element = DOMElement(
        element_id="cache_test",
        selector="#cache-test",
        element_type="div",
        text_content="缓存测试元素",
        updated_at=datetime.now(),
        page_url="https://example.com",
        description="用于测试缓存行为"
    )
    
    dom_manager.insert_element(element)
    print("1. 插入元素到数据库")
    
    # 第一次获取（会从数据库加载并存入缓存）
    first_get = dom_manager.get_element("#cache-test")
    print(f"2. 首次获取: {first_get.element_id if first_get else 'None'}")
    
    # 第二次获取（应该从缓存获取）
    second_get = dom_manager.get_element("#cache-test")
    print(f"3. 二次获取: {second_get.element_id if second_get else 'None'}")
    
    # 更新元素后获取（应该获取到更新后的数据）
    element.text_content = "更新后的缓存测试元素"
    dom_manager.update_element(element)
    print("4. 更新元素到数据库")
    
    updated_get = dom_manager.get_element("#cache-test")
    print(f"5. 更新后获取: {updated_get.text_content if updated_get else 'None'}")


if __name__ == "__main__":
    print("DOM管理器使用示例")
    print("=" * 50)
    
    example_basic_usage()
    example_with_config_selectors()
    example_batch_operations()
    example_cache_behavior()
    
    print("\n" + "=" * 50)
    print("所有示例执行完成！")