"""AI 模块使用示例"""
import sys
from pathlib import Path

# 添加项目根目录到路径
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

from business.ai_manager import AIManager
from core.models import Comment, UserInfo
from core.logger import logger


def example_1_generate_fairy_post():
    """示例 1: 生成小仙女风格文案"""
    logger.info("\n" + "="*60)
    logger.info("示例 1: 生成小仙女风格文案")
    logger.info("="*60)
    
    ai_manager = AIManager()
    
    # 生成春季穿搭文案
    post = ai_manager.generate_xiaohongshu_post(
        topic="春季穿搭",
        style="fairy",
        word_count=100
    )
    
    logger.info(f"\n{post}\n")


def example_2_generate_controversial_post():
    """示例 2: 生成逆天言论"""
    logger.info("\n" + "="*60)
    logger.info("示例 2: 生成逆天言论")
    logger.info("="*60)
    
    ai_manager = AIManager()
    
    # 生成关于恋爱观的逆天言论
    post = ai_manager.generate_xiaohongshu_post(
        topic="现代恋爱观",
        style="controversial",
        word_count=100
    )
    
    logger.info(f"\n{post}\n")


def example_3_reply_to_comment():
    """示例 3: 回复评论"""
    logger.info("\n" + "="*60)
    logger.info("示例 3: 智能回复评论")
    logger.info("="*60)
    
    ai_manager = AIManager()
    
    # 模拟一条负面评论
    comment = Comment(
        comment_id="123",
        content="这也太假了吧，一看就是摆拍的",
        user_info=UserInfo(user_id="hater123", nickname="杠精小王子")
    )
    
    logger.info(f"\n原评论: {comment.content}")
    logger.info(f"评论者: {comment.user_info.nickname}\n")
    
    # 生成斗争性回复
    reply = ai_manager.generate_comment_reply(comment, style="aggressive")
    logger.info(f"回复风格: 斗争性")
    logger.info(f"生成回复: {reply}\n")


def example_4_batch_generate():
    """示例 4: 批量生成文案"""
    logger.info("\n" + "="*60)
    logger.info("示例 4: 批量生成文案")
    logger.info("="*60)
    
    ai_manager = AIManager()
    
    # 批量生成 3 篇不同主题的文案
    topics = ["护肤心得", "减肥日记", "周末Vlog"]
    posts = ai_manager.batch_generate_posts(
        count=3,
        style="fairy",
        topics=topics
    )
    
    for i, (topic, post) in enumerate(zip(topics, posts), 1):
        logger.info(f"\n【文案 {i} - {topic}】")
        logger.info(post)
        logger.info("-" * 60)


def example_5_different_reply_styles():
    """示例 5: 不同回复风格对比"""
    logger.info("\n" + "="*60)
    logger.info("示例 5: 不同回复风格对比")
    logger.info("="*60)
    
    ai_manager = AIManager()
    
    comment = Comment(
        comment_id="456",
        content="你这穿搭真的不行，审美堪忧",
        user_info=UserInfo(user_id="critic456", nickname="时尚评论家")
    )
    
    logger.info(f"\n原评论: {comment.content}\n")
    
    styles = {
        "aggressive": "斗争性回复",
        "sarcastic": "讽刺回复",
        "defensive": "防御反击",
        "dismissive": "不屑回复"
    }
    
    for style_code, style_name in styles.items():
        reply = ai_manager.generate_comment_reply(comment, style=style_code)
        logger.info(f"【{style_name}】")
        logger.info(f"{reply}\n")


if __name__ == "__main__":
    logger.info("\nAI 模块使用示例")
    logger.info("提示：请确保已配置 config_personal.py 中的 AI API Key\n")
    
    try:
        # 运行所有示例
        example_1_generate_fairy_post()
        example_2_generate_controversial_post()
        example_3_reply_to_comment()
        example_4_batch_generate()
        example_5_different_reply_styles()
        
        logger.info("\n所有示例运行完成！")
        
    except Exception as e:
        logger.error(f"\n运行出错: {e}")
        logger.info("\n请检查：")
        logger.info("1. 是否已安装依赖: pip install -r requirements.txt")
        logger.info("2. 是否已配置 config_personal.py")
        logger.info("3. AI API Key 是否有效")
