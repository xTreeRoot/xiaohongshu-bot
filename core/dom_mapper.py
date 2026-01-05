"""DOM元素映射器 - 负责DOM元素与数据库之间的映射"""
import sqlite3
from datetime import datetime
from typing import List, Optional, Dict, Any

from core.logger import logger
from core.models import DOMElement


class DOMElementMapper:
    """DOM元素映射器 - 负责DOM元素与数据库之间的映射操作"""
    
    def __init__(self, db_path: str = "dom_elements.db"):
        """初始化映射器
        
        Args:
            db_path: 数据库文件路径
        """
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """初始化数据库表结构"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # 创建DOM元素表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS dom_elements (
                    element_id TEXT PRIMARY KEY,
                    selector TEXT NOT NULL,
                    element_type TEXT NOT NULL,
                    position TEXT,
                    text_content TEXT,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    page_url TEXT,
                    description TEXT
                )
            ''')
            
            # 创建索引以提高查询性能
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_selector ON dom_elements(selector)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_page_url ON dom_elements(page_url)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_element_type ON dom_elements(element_type)')
            
            conn.commit()
            logger.info(f"DOM元素数据库初始化完成: {self.db_path}")
    
    def insert(self, element: DOMElement) -> bool:
        """插入DOM元素
        
        Args:
            element: DOM元素对象
            
        Returns:
            是否插入成功
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT OR REPLACE INTO dom_elements 
                    (element_id, selector, element_type, position, text_content, updated_at, page_url, description)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    element.element_id,
                    element.selector,
                    element.element_type,
                    element.position,
                    element.text_content,
                    element.updated_at.isoformat() if element.updated_at else datetime.now().isoformat(),
                    element.page_url,
                    element.description
                ))
                
                conn.commit()
                logger.debug(f"DOM元素已插入/更新: {element.element_id}")
                return True
        except Exception as e:
            logger.error(f"插入DOM元素失败: {e}")
            return False
    
    def find_by_id(self, element_id: str) -> Optional[DOMElement]:
        """根据ID查找DOM元素
        
        Args:
            element_id: 元素ID
            
        Returns:
            DOM元素对象，如果不存在则返回None
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT element_id, selector, element_type, position, text_content, updated_at, page_url, description
                    FROM dom_elements WHERE element_id = ?
                ''', (element_id,))
                
                row = cursor.fetchone()
                if row:
                    return self._row_to_element(row)
                return None
        except Exception as e:
            logger.error(f"根据ID查找DOM元素失败: {e}")
            return None
    
    def find_by_selector(self, selector: str) -> Optional[DOMElement]:
        """根据选择器查找DOM元素
        
        Args:
            selector: CSS选择器或XPath
            
        Returns:
            DOM元素对象，如果不存在则返回None
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT element_id, selector, element_type, position, text_content, updated_at, page_url, description
                    FROM dom_elements WHERE selector = ?
                ''', (selector,))
                
                row = cursor.fetchone()
                if row:
                    return self._row_to_element(row)
                return None
        except Exception as e:
            logger.error(f"根据选择器查找DOM元素失败: {e}")
            return None
    
    def find_by_page_url(self, page_url: str) -> List[DOMElement]:
        """根据页面URL查找DOM元素列表
        
        Args:
            page_url: 页面URL
            
        Returns:
            DOM元素列表
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT element_id, selector, element_type, position, text_content, updated_at, page_url, description
                    FROM dom_elements WHERE page_url = ?
                ''', (page_url,))
                
                elements = []
                for row in cursor.fetchall():
                    element = self._row_to_element(row)
                    if element:
                        elements.append(element)
                return elements
        except Exception as e:
            logger.error(f"根据页面URL查找DOM元素失败: {e}")
            return []
    
    def find_all(self) -> List[DOMElement]:
        """查找所有DOM元素
        
        Returns:
            DOM元素列表
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT element_id, selector, element_type, position, text_content, updated_at, page_url, description
                    FROM dom_elements
                ''')
                
                elements = []
                for row in cursor.fetchall():
                    element = self._row_to_element(row)
                    if element:
                        elements.append(element)
                return elements
        except Exception as e:
            logger.error(f"查找所有DOM元素失败: {e}")
            return []
    
    def find_by_type(self, element_type: str) -> List[DOMElement]:
        """根据元素类型查找DOM元素
        
        Args:
            element_type: 元素类型
            
        Returns:
            DOM元素列表
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT element_id, selector, element_type, position, text_content, updated_at, page_url, description
                    FROM dom_elements WHERE element_type = ?
                ''', (element_type,))
                
                elements = []
                for row in cursor.fetchall():
                    element = self._row_to_element(row)
                    if element:
                        elements.append(element)
                return elements
        except Exception as e:
            logger.error(f"根据类型查找DOM元素失败: {e}")
            return []
    
    def update(self, element: DOMElement) -> bool:
        """更新DOM元素
        
        Args:
            element: DOM元素对象
            
        Returns:
            是否更新成功
        """
        return self.insert(element)  # 复用插入方法，使用INSERT OR REPLACE
    
    def delete(self, element_id: str) -> bool:
        """删除DOM元素
        
        Args:
            element_id: 元素ID
            
        Returns:
            是否删除成功
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM dom_elements WHERE element_id = ?', (element_id,))
                conn.commit()
                
                if cursor.rowcount > 0:
                    logger.debug(f"DOM元素已删除: {element_id}")
                    return True
                else:
                    logger.warning(f"未找到要删除的DOM元素: {element_id}")
                    return False
        except Exception as e:
            logger.error(f"删除DOM元素失败: {e}")
            return False
    
    def search(self, **kwargs) -> List[DOMElement]:
        """搜索DOM元素
        
        Args:
            **kwargs: 搜索条件，支持 element_type, page_url, description 等字段
            
        Returns:
            DOM元素列表
        """
        try:
            conditions = []
            params = []
            
            for key, value in kwargs.items():
                if value is not None:
                    conditions.append(f"{key} = ?")
                    params.append(value)
            
            query = "SELECT element_id, selector, element_type, position, text_content, updated_at, page_url, description FROM dom_elements"
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                
                elements = []
                for row in cursor.fetchall():
                    element = self._row_to_element(row)
                    if element:
                        elements.append(element)
                return elements
        except Exception as e:
            logger.error(f"搜索DOM元素失败: {e}")
            return []
    
    def batch_insert(self, elements: List[DOMElement]) -> bool:
        """批量插入DOM元素
        
        Args:
            elements: DOM元素列表
            
        Returns:
            是否批量插入成功
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                for element in elements:
                    cursor.execute('''
                        INSERT OR REPLACE INTO dom_elements 
                        (element_id, selector, element_type, position, text_content, updated_at, page_url, description)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        element.element_id,
                        element.selector,
                        element.element_type,
                        element.position,
                        element.text_content,
                        element.updated_at.isoformat() if element.updated_at else datetime.now().isoformat(),
                        element.page_url,
                        element.description
                    ))
                
                conn.commit()
                logger.info(f"批量插入DOM元素完成: {len(elements)}个")
                return True
        except Exception as e:
            logger.error(f"批量插入DOM元素失败: {e}")
            return False
    
    def _row_to_element(self, row: tuple) -> Optional[DOMElement]:
        """将数据库行转换为DOMElement对象
        
        Args:
            row: 数据库行数据
            
        Returns:
            DOMElement对象
        """
        try:
            return DOMElement(
                element_id=row[0],
                selector=row[1],
                element_type=row[2],
                position=row[3],
                text_content=row[4],
                updated_at=datetime.fromisoformat(row[5]) if row[5] else None,
                page_url=row[6],
                description=row[7]
            )
        except Exception as e:
            logger.error(f"转换数据库行到DOMElement失败: {e}")
            return None
