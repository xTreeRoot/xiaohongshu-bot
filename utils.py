"""工具函数模块"""
import json
import re
from typing import List, Optional
from core.models import Comment
from core.logger import logger


class CommentParser:
    """评论解析器"""
    
    @staticmethod
    def parse_response(response_body: str) -> List[Comment]:
        """解析评论接口响应
        
        Args:
            response_body: 响应体JSON字符串
            
        Returns:
            评论对象列表
        """
        try:
            data = json.loads(response_body)
            
            # 检查数据是否在 data 字段中
            if 'data' in data:
                data = data['data']
            
            if 'comments' not in data:
                return []
            
            comments_data = data.get('comments', [])
            comments = []
            
            for comment_data in comments_data:
                try:
                    comment = Comment.from_dict(comment_data)
                    comments.append(comment)
                except Exception as e:
                    logger.warning(f"解析评论失败: {e}")
                    continue
            
            return comments
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON解析失败: {e}")
            return []
        except Exception as e:
            logger.error(f"评论解析出错: {e}")
            return []
    
    @staticmethod
    def format_comment(comment: Comment, indent: int = 0) -> str:
        """格式化单条评论为字符串
        
        Args:
            comment: 评论对象
            indent: 缩进级别
            
        Returns:
            格式化后的字符串
        """
        prefix = "  " * indent
        lines = []
        
        lines.append(f"{prefix}用户: {comment.user_info.nickname}")
        lines.append(f"{prefix}内容: {comment.content}")
        lines.append(f"{prefix}点赞数: {comment.like_count}")
        lines.append(f"{prefix}IP归属地: {comment.ip_location}")
        lines.append(f"{prefix}回复数: {comment.sub_comment_count}")
        lines.append(f"{prefix}评论ID: {comment.comment_id}")
        
        # 语音评论
        if comment.audio_info:
            lines.append(f"{prefix}[语音评论] {comment.audio_info.tag_text}")
            lines.append(f"{prefix}识别文本: {comment.audio_info.asr_text}")
        
        # 图片
        if comment.pictures:
            lines.append(f"{prefix}[图片] {len(comment.pictures)} 张图片")
            for idx, pic_url in enumerate(comment.pictures, 1):
                lines.append(f"{prefix}  图片{idx}: {pic_url}")
        
        return "\n".join(lines)
    
    @staticmethod
    def format_comments(comments: List[Comment]) -> str:
        """格式化评论列表为字符串
        
        Args:
            comments: 评论列表
            
        Returns:
            格式化后的字符串
        """
        if not comments:
            return "暂无评论"
        
        lines = [f"\n{'='*80}", f"共获取到 {len(comments)} 条评论", f"{'='*80}\n"]
        
        for idx, comment in enumerate(comments, 1):
            lines.append(f"[评论 {idx}]")
            lines.append(CommentParser.format_comment(comment))
            
            # 子评论
            if comment.sub_comments:
                lines.append(f"\n  --- 回复列表 ({len(comment.sub_comments)} 条) ---")
                for sub_idx, sub_comment in enumerate(comment.sub_comments, 1):
                    lines.append(f"\n  [回复 {sub_idx}]")
                    lines.append(CommentParser.format_comment(sub_comment, indent=2))
                    if sub_comment.target_comment:
                        if sub_comment.target_comment.user_info:
                            target_name = sub_comment.target_comment.user_info.nickname
                        else:
                            target_name = "?"
                        target_id = sub_comment.target_comment.comment_id if sub_comment.target_comment.comment_id else "未知"
                        lines.append(f"    回复给: @{target_name} (ID: {target_id})")
            
            lines.append(f"\n{'-'*80}\n")
        
        return "\n".join(lines)


class URLExtractor:
    """URL提取器"""
    
    @staticmethod
    def extract_note_id(url: str) -> Optional[str]:
        """从URL中提取笔记ID
        
        Args:
            url: 笔记URL
            
        Returns:
            笔记ID或None
        """
        match = re.search(r'/explore/([a-f0-9]+)', url)
        if match:
            return match.group(1)
        return None


class DataValidator:
    """数据验证器"""
    
    @staticmethod
    def validate_publish_content(content: str, title: str) -> bool:
        """验证发布内容
        
        Args:
            content: 内容
            title: 标题
            
        Returns:
            是否有效
        """
        if not content or not content.strip():
            logger.error("内容不能为空")
            return False
        
        if not title or not title.strip():
            logger.error("标题不能为空")
            return False
        
        if len(title) > 100:
            logger.error("标题长度不能超过100字符")
            return False
        
        return True
