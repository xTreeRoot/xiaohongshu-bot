"""AI 模块测试脚本"""
import sys
from pathlib import Path

# 添加项目根目录到路径
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

from business import AIManager
from core.models import Comment, UserInfo
from core.logger import logger


def test_fairy_style():
    """测试小仙女风格文案"""
    logger.info("\n" + "="*60)
    logger.info("测试 1: 小仙女风格文案生成")
    logger.info("="*60)
    
    ai_manager = AIManager()
    
    try:
        # 生成随机主题
        post1 = ai_manager.generate_xiaohongshu_post(style="fairy")
        logger.info(f"\n【随机主题-小仙女风格】\n{post1}\n")
        
        # 指定主题
        post2 = ai_manager.generate_xiaohongshu_post(
            topic="春季穿搭",
            style="fairy",
            word_count=100
        )
        logger.info(f"\n【春季穿搭-小仙女风格】\n{post2}\n")
        
    except Exception as e:
        logger.error(f"测试失败: {e}")


def test_controversial_style():
    """测试逆天言论风格"""
    logger.info("\n" + "="*60)
    logger.info("测试 2: 逆天言论风格文案生成")
    logger.info("="*60)
    
    ai_manager = AIManager()
    
    try:
        post = ai_manager.generate_xiaohongshu_post(
            topic="恋爱观",
            style="controversial",
            word_count=100
        )
        logger.info(f"\n【恋爱观-逆天言论】\n{post}\n")
        
    except Exception as e:
        logger.error(f"测试失败: {e}")


def test_provocative_style():
    """测试引战风格"""
    logger.info("\n" + "="*60)
    logger.info("测试 3: 引战风格文案生成")
    logger.info("="*60)
    
    ai_manager = AIManager()
    
    try:
        post = ai_manager.generate_xiaohongshu_post(
            style="provocative",
            word_count=100
        )
        logger.info(f"\n【引战风格】\n{post}\n")
        
    except Exception as e:
        logger.error(f"测试失败: {e}")


def test_comment_reply():
    """测试评论回复"""
    logger.info("\n" + "="*60)
    logger.info("测试 4: 智能评论回复")
    logger.info("="*60)
    
    ai_manager = AIManager()
    
    # 模拟几条评论
    test_comments = [
        Comment(
            comment_id="1",
            content="这也太假了吧，肯定是P的",
            user_info=UserInfo(user_id="user1", nickname="路人甲")
        ),
        Comment(
            comment_id="2",
            content="你这样穿真的不好看",
            user_info=UserInfo(user_id="user2", nickname="路人乙")
        ),
        Comment(
            comment_id="3",
            content="又来骗钱了，这些东西根本不值这个价",
            user_info=UserInfo(user_id="user3", nickname="路人丙")
        ),
    ]
    
    styles = ["aggressive", "sarcastic", "defensive", "dismissive"]
    
    try:
        for i, comment in enumerate(test_comments):
            style = styles[i % len(styles)]
            reply = ai_manager.generate_comment_reply(comment, style=style)
            logger.info(f"\n原评论: {comment.content}")
            logger.info(f"回复风格: {style}")
            logger.info(f"生成回复: {reply}\n")
            logger.info("-" * 60)
        
    except Exception as e:
        logger.error(f"测试失败: {e}")


def test_batch_generate():
    """测试批量生成"""
    logger.info("\n" + "="*60)
    logger.info("测试 5: 批量生成文案")
    logger.info("="*60)
    
    ai_manager = AIManager()
    
    try:
        topics = ["护肤", "减肥", "旅行"]
        posts = ai_manager.batch_generate_posts(
            count=3,
            style="fairy",
            topics=topics
        )
        
        for i, post in enumerate(posts, 1):
            logger.info(f"\n【文案 {i}】\n{post}\n")
            logger.info("-" * 60)
        
    except Exception as e:
        logger.error(f"测试失败: {e}")


def main():
    """主函数"""
    logger.info("\nAI 模块测试开始")
    logger.info("提示：确保已配置 config_personal.py 中的 ai_api_key")
    
    tests = [
        ("1", "小仙女风格", test_fairy_style),
        ("2", "逆天言论风格", test_controversial_style),
        ("3", "引战风格", test_provocative_style),
        ("4", "智能评论回复", test_comment_reply),
        ("5", "批量生成", test_batch_generate),
        ("all", "全部测试", None),
    ]
    
    logger.info("\n请选择要测试的功能：")
    for code, name, _ in tests:
        logger.info(f"  {code}. {name}")
    
    choice = input("\n请输入选项（1-5 或 all）: ").strip()
    
    if choice == "all":
        for code, name, func in tests[:-1]:  # 排除 "all" 选项本身
            if func:
                func()
    else:
        for code, name, func in tests:
            if code == choice and func:
                func()
                break
        else:
            logger.warning("无效的选项")
    
    logger.info("\n测试完成")


if __name__ == "__main__":
    main()
