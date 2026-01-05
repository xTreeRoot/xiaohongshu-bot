"""DOM元素管理模块"""
import json
from pathlib import Path
from typing import List, Optional, Dict, Any

from core.dom_mapper import DOMElementMapper
from core.logger import logger
from core.models import DOMElement


class DOMCacheManager:
    """DOM元素缓存管理类（二级缓存）"""
    
    def __init__(self, cache_dir: str = "cache", cache_file: str = "dom_cache.json"):
        """初始化缓存管理器
        
        Args:
            cache_dir: 缓存目录
            cache_file: 缓存文件名
        """
        self.cache_dir = Path(cache_dir)
        self.cache_file = self.cache_dir / cache_file
        self.cache_data: Dict[str, Any] = {}
        
        # 确保缓存目录存在
        self.cache_dir.mkdir(exist_ok=True)
        self.load_cache()
    
    def load_cache(self):
        """从文件加载缓存"""
        try:
            if self.cache_file.exists():
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    self.cache_data = json.load(f)
                logger.debug(f"DOM缓存已加载: {len(self.cache_data)}个元素")
            else:
                self.cache_data = {}
        except Exception as e:
            logger.error(f"加载DOM缓存失败: {e}")
            self.cache_data = {}
    
    def save_cache(self):
        """保存缓存到文件"""
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.cache_data, f, ensure_ascii=False, indent=2)
            logger.debug(f"DOM缓存已保存: {len(self.cache_data)}个元素")
        except Exception as e:
            logger.error(f"保存DOM缓存失败: {e}")
    
    def get_from_cache(self, key: str) -> Optional[Dict[str, Any]]:
        """从缓存获取数据
        
        Args:
            key: 缓存键
            
        Returns:
            缓存的数据，如果不存在则返回None
        """
        return self.cache_data.get(key)
    
    def set_to_cache(self, key: str, value: Dict[str, Any]):
        """设置缓存数据
        
        Args:
            key: 缓存键
            value: 缓存值
        """
        self.cache_data[key] = value
        self.save_cache()
    
    def delete_from_cache(self, key: str) -> bool:
        """从缓存删除数据
        
        Args:
            key: 缓存键
            
        Returns:
            是否删除成功
        """
        if key in self.cache_data:
            del self.cache_data[key]
            self.save_cache()
            return True
        return False
    
    def clear_cache(self):
        """清空缓存"""
        self.cache_data = {}
        self.save_cache()
        logger.info("DOM缓存已清空")
    
    def get_element_by_selector(self, selector: str) -> Optional[DOMElement]:
        """根据选择器从缓存获取DOM元素
        
        Args:
            selector: CSS选择器或XPath
            
        Returns:
            DOM元素对象，如果不存在则返回None
        """
        cache_key = f"selector:{selector}"
        cached_data = self.get_from_cache(cache_key)
        if cached_data:
            return DOMElement.from_dict(cached_data)
        return None
    
    def set_element_by_selector(self, selector: str, element: DOMElement):
        """根据选择器设置DOM元素到缓存
        
        Args:
            selector: CSS选择器或XPath
            element: DOM元素对象
        """
        cache_key = f"selector:{selector}"
        self.set_to_cache(cache_key, element.to_dict())
    
    def delete_element_by_selector(self, selector: str) -> bool:
        """根据选择器从缓存删除DOM元素
        
        Args:
            selector: CSS选择器或XPath
            
        Returns:
            是否删除成功
        """
        cache_key = f"selector:{selector}"
        return self.delete_from_cache(cache_key)


class DOMManager:
    """DOM元素管理器 - 统一管理数据库和缓存"""
    
    def __init__(self, db_path: str = "dom_elements.db", cache_dir: str = "cache"):
        """初始化DOM管理器
        
        Args:
            db_path: 数据库文件路径
            cache_dir: 缓存目录
        """
        self.mapper = DOMElementMapper(db_path)
        self.cache_manager = DOMCacheManager(cache_dir)
    
    def get_element(self, selector: str) -> Optional[DOMElement]:
        """获取DOM元素，优先从缓存获取，缓存没有则从数据库获取
        
        Args:
            selector: CSS选择器或XPath
            
        Returns:
            DOM元素对象，如果不存在则返回None
        """
        # 先从缓存获取
        element = self.cache_manager.get_element_by_selector(selector)
        if element:
            logger.debug(f"从缓存获取DOM元素: {selector}")
            return element
        
        # 缓存没有，从数据库获取
        element = self.mapper.find_by_selector(selector)
        if element:
            logger.debug(f"从数据库获取DOM元素: {selector}")
            # 存入缓存
            self.cache_manager.set_element_by_selector(selector, element)
            return element
        
        logger.debug(f"未找到DOM元素: {selector}")
        return None
    
    def insert_element(self, element: DOMElement) -> bool:
        """插入DOM元素到数据库并更新缓存
        
        Args:
            element: DOM元素对象
            
        Returns:
            是否插入成功
        """
        # 插入数据库
        success = self.mapper.insert(element)
        if success:
            # 更新缓存
            self.cache_manager.set_element_by_selector(element.selector, element)
            logger.debug(f"DOM元素已插入: {element.element_id}")
        return success
    
    def update_element(self, element: DOMElement) -> bool:
        """更新DOM元素并清除相关缓存
        
        Args:
            element: DOM元素对象
            
        Returns:
            是否更新成功
        """
        # 更新数据库
        success = self.mapper.update(element)
        if success:
            # 清除缓存（下次获取时会重新从数据库加载）
            self.cache_manager.delete_element_by_selector(element.selector)
            logger.debug(f"DOM元素已更新: {element.element_id}")
        return success
    
    def batch_insert_initial_elements(self, selectors: Dict[str, str], page_url: str = ""):
        """批量插入初始DOM元素到数据库
        
        Args:
            selectors: 选择器字典
            page_url: 页面URL
        """
        elements = []
        for element_id, selector in selectors.items():
            element = DOMElement(
                element_id=element_id,
                selector=selector,
                element_type="selector",
                page_url=page_url,
                description=f"初始选择器: {element_id}"
            )
            elements.append(element)
        
        if elements:
            success = self.mapper.batch_insert(elements)
            if success:
                # 清空缓存，让后续获取从数据库加载
                self.cache_manager.clear_cache()
                logger.info(f"已批量插入初始DOM元素: {len(elements)}个")
