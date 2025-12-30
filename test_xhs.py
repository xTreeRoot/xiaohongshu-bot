"""小红书自动化测试脚本"""
from core.exceptions import XHSPublisherException
from core.logger import logger
from core.models import PublishContent
from utils import CommentParser
from core.xhs_client import XHSClient


def test_comment_and_reply():
    """测试：搜索笔记、获取评论并回复"""
    client = XHSClient()
    
    try:
        logger.info("=" * 60)
        logger.info("测试场景：搜索笔记 -> 获取评论 -> 自动回复")
        logger.info("=" * 60)
        
        # 1. 搜索并打开笔记
        keyword = "室友吃的东西不卫生"  # 替换为你想搜索的关键词
        note_info = client.search_and_open_note(keyword=keyword)
        
        if not note_info:
            logger.warning("未找到匹配的笔记，测试终止")
            return
        
        logger.info(f"✓ 成功打开笔记: {note_info.title}")
        
        # 2. 获取评论（启用滚动加载）
        comments = client.get_comments(
            enable_scroll=True,  # 启用自动滚动
            scroll_count=5       # 滚动 5 次
        )
        
        if not comments:
            logger.warning("未获取到评论")
            return
        
        # 3. 打印评论
        client.print_comments(comments)
        
        # 4. 格式化输出（使用工具类）
        formatted_output = CommentParser.format_comments(comments)
        logger.info(f"\n格式化后的评论列表:")
        print(formatted_output)
        
        # 5. 回复第一条评论
        if len(comments) > 0:
            test_comment_id = comments[0].comment_id
            test_reply_text = "666"  # 回复内容（可以后续换成AI生成）
            
            print(f"\n{'=' * 80}")
            print(f"将使用 AI 自动回复评论...")
            print(f"{'=' * 80}")
            
            success = client.reply_comment(
                comment_id=test_comment_id,
                reply_text=test_reply_text
            )
            
            if success:
                print(f"\n✓ 自动回复完成！")
            else:
                print(f"\n✗ 自动回复失败")
        
        # 保持浏览器不退出
        input("\n按回车键退出...")
        
    except XHSPublisherException as e:
        logger.error(f"业务异常: {e}")
    except Exception as e:
        logger.exception(f"程序异常: {e}")
    finally:
        client.quit()


def test_publish():
    """测试：发布内容"""
    client = XHSClient()
    
    try:
        logger.info("=" * 60)
        logger.info("测试场景：发布内容")
        logger.info("=" * 60)
        
        # 创建发布内容
        publish_content = PublishContent(
            content="selenium测试",
            title="我是标题"
        )
        
        # 发布
        success = client.publish_content(publish_content)
        
        if success:
            logger.info("✓ 发布成功")
        else:
            logger.error("✗ 发布失败")
        
        # 保持浏览器不退出
        input("\n按回车键退出...")
        
    except XHSPublisherException as e:
        logger.error(f"业务异常: {e}")
    except Exception as e:
        logger.exception(f"程序异常: {e}")
    finally:
        client.quit()


def test_only_fetch_comments():
    """测试：仅获取评论（不回复）"""
    client = XHSClient()
    
    try:
        logger.info("=" * 60)
        logger.info("测试场景：仅获取评论")
        logger.info("=" * 60)
        
        # 搜索并打开笔记
        keyword = "室友吃的东西不卫生"
        note_info = client.search_and_open_note(keyword=keyword)
        
        if not note_info:
            return
        
        # 获取评论（不滚动）
        comments = client.get_comments(enable_scroll=False)
        
        # 打印评论
        client.print_comments(comments)
        
        # 保持浏览器不退出
        input("\n按回车键退出...")
        
    except Exception as e:
        logger.exception(f"程序异常: {e}")
    finally:
        client.quit()


if __name__ == "__main__":
    """主程序入口 - 选择要运行的测试"""
    
    print("\n" + "=" * 60)
    print("小红书自动化测试")
    print("=" * 60)
    print("\n请选择要运行的测试:")
    print("1. 搜索笔记 -> 获取评论 -> 自动回复")
    print("2. 发布内容")
    print("3. 仅获取评论（不回复）")
    print("0. 退出")
    print()
    
    choice = input("请输入选项 (0-3): ").strip()
    
    if choice == "1":
        test_comment_and_reply()
    elif choice == "2":
        test_publish()
    elif choice == "3":
        test_only_fetch_comments()
    elif choice == "0":
        print("退出程序")
    else:
        print("无效选项，退出程序")
