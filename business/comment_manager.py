"""评论管理模块"""
import json
import re
import time
from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from core.browser_manager import BrowserManager
from core.decorators import log_execution
from core.logger import logger
from utils import CommentParser


class CommentManager:
    """评论管理器 - 负责评论相关操作（获取、回复等）"""

    def __init__(self, browser_manager: BrowserManager):
        """初始化评论管理器
        
        Args:
            browser_manager: 浏览器管理器实例
        """
        self.browser = browser_manager

    def _extract_comments_from_response(self, response_body):
        """从响应数据中提取并解析评论列表
        
        Args:
            response_body: API响应体
            
        Returns:
            Comment对象列表
        """
        try:
            comments = CommentParser.parse_response(response_body)

            # 调试: 打印第一条评论的原始数据
            if comments:
                try:
                    data = json.loads(response_body)
                    if 'data' in data and 'comments' in data['data']:
                        first_comment = data['data']['comments'][0] if data['data']['comments'] else None
                        if first_comment and 'pictures' in first_comment:
                            logger.debug(
                                f"\n第一条评论的pictures字段结构: {json.dumps(first_comment.get('pictures', []), indent=2, ensure_ascii=False)}")
                except:
                    pass

            return comments
        except Exception as e:
            logger.error(f"提取评论列表失败: {e}")
            return []

    def _scroll_page(self, scroll_count=3, scroll_pause=2, note_id=None):
        """滚动页面以加载更多评论，并实时收集评论接口响应
        
        Args:
            scroll_count: 滚动次数
            scroll_pause: 每次滚动后的等待时间（秒）
            note_id: 帖子ID，用于过滤评论接口
            
        Returns:
            收集到的所有评论列表
        """
        logger.info(f"\n开始滚动加载更多评论...")

        all_comments = []
        processed_request_ids = set()

        try:
            # 等待评论区域加载
            time.sleep(2)

            # 尝试找到真正可滚动的评论容器
            scroll_element = None
            scroll_method = None

            # 方法1: 尝试找到外层可滚动的评论容器
            try:
                possible_containers = self.browser.driver.find_elements(
                    By.CSS_SELECTOR,
                    "div.list-container, div.comment-container, div[class*='comment'], div[class*='scroll']"
                )

                for container in possible_containers:
                    info = self.browser.execute_script("""
                        const elem = arguments[0];
                        return {
                            scrollHeight: elem.scrollHeight,
                            clientHeight: elem.clientHeight,
                            hasScroll: elem.scrollHeight > elem.clientHeight,
                            overflow: window.getComputedStyle(elem).overflow,
                            overflowY: window.getComputedStyle(elem).overflowY,
                            className: elem.className
                        };
                    """, container)

                    # 找到第一个可滚动的容器
                    if info['hasScroll'] and info['overflowY'] in ['auto', 'scroll']:
                        scroll_element = container
                        scroll_method = 'container'
                        logger.info(f"找到可滚动容器: {info['className'][:50]}")
                        logger.debug(f"  容器高度: {info['clientHeight']}px, 可滚动高度: {info['scrollHeight']}px")
                        break
            except Exception as e:
                logger.warning(f"查找可滚动容器失败: {e}")

            # 方法2: 如果没找到可滚动容器,使用整页滚动
            if not scroll_element:
                scroll_method = 'window'
                logger.info("未找到可滚动容器,将使用整页滚动")
                try:
                    comment_area = self.browser.driver.find_element(By.CSS_SELECTOR, "div.list-container")
                    self.browser.execute_script("arguments[0].scrollIntoView({block: 'start'});", comment_area)
                    time.sleep(1)
                    logger.info("已定位到评论区域")
                except:
                    logger.warning("  未找到评论区域")

            # 开始滚动
            for i in range(scroll_count):
                logs_before = len(self.browser.get_network_logs())

                if scroll_method == 'container':
                    # 滚动容器元素
                    scroll_top_before = self.browser.execute_script("return arguments[0].scrollTop;", scroll_element)
                    self.browser.execute_script("arguments[0].scrollTop += 1200;", scroll_element)
                    time.sleep(0.5)
                    scroll_top_after = self.browser.execute_script("return arguments[0].scrollTop;", scroll_element)
                    scroll_distance = scroll_top_after - scroll_top_before
                else:
                    # 滚动窗口
                    scroll_top_before = self.browser.execute_script(
                        "return document.documentElement.scrollTop || document.body.scrollTop;"
                    )
                    self.browser.execute_script("""
                        const currentScroll = document.documentElement.scrollTop || document.body.scrollTop;
                        window.scrollTo({
                            top: currentScroll + 1200,
                            behavior: 'smooth'
                        });
                    """)
                    time.sleep(0.5)
                    scroll_top_after = self.browser.execute_script(
                        "return document.documentElement.scrollTop || document.body.scrollTop;"
                    )
                    scroll_distance = scroll_top_after - scroll_top_before

                logger.info(f"第 {i + 1}/{scroll_count} 次滚动 (距离: {scroll_distance}px, 位置: {scroll_top_after}px)")

                # 等待接口请求
                time.sleep(1.5)

                # 检查并处理评论接口
                logs_after = self.browser.get_network_logs()
                new_comment_requests = 0

                for log in logs_after[logs_before:]:
                    try:
                        message = json.loads(log['message'])['message']
                        if message['method'] == 'Network.responseReceived':
                            response_url = message['params']['response']['url']
                            if 'api/sns/web/v2/comment/page' in response_url:
                                new_comment_requests += 1
                                request_id = message['params']['requestId']

                                # 检查note_id是否匹配
                                if note_id and f'note_id={note_id}' not in response_url:
                                    continue

                                # 避免重复处理
                                if request_id in processed_request_ids:
                                    continue

                                logger.debug(f"    检测到评论接口: {response_url[:80]}...")

                                # 立即获取响应体
                                try:
                                    response_body = self.browser.execute_cdp_cmd(
                                        'Network.getResponseBody',
                                        {'requestId': request_id}
                                    )

                                    if 'body' in response_body:
                                        processed_request_ids.add(request_id)
                                        logger.info(f"    成功获取响应体 (ID: {request_id[:8]}...)")

                                        # 提取评论
                                        comments = self._extract_comments_from_response(response_body['body'])
                                        all_comments.extend(comments)
                                        logger.info(f"    本次获取 {len(comments)} 条评论，累计 {len(all_comments)} 条")

                                except Exception as e:
                                    error_msg = str(e)
                                    if 'No resource with given identifier found' not in error_msg:
                                        logger.error(f"    获取失败: {error_msg}")
                    except:
                        continue

                if new_comment_requests > 0:
                    logger.info(f"  本次滚动检测到 {new_comment_requests} 个评论接口请求")
                else:
                    if scroll_distance == 0:
                        logger.debug(f"    滚动距离为0且无新接口，已到底部")
                        logger.info(f"  提前结束滚动")
                        break
                    else:
                        logger.warning(f"  未检测到新的评论接口请求（可能正在加载中）")

                # 等待剩余时间
                remaining_time = scroll_pause - 2.0
                if remaining_time > 0:
                    time.sleep(remaining_time)

            logger.info(f"\n滚动完成，共收集到 {len(all_comments)} 条评论\n")
            return all_comments

        except Exception as e:
            logger.error(f"滚动时出错: {e}")
            import traceback
            traceback.print_exc()
            return all_comments

    def fetch_comments(self, note_id=None, enable_scroll=False, scroll_count=3):
        """获取帖子评论
        
        Args:
            note_id: 帖子ID，如果不提供则从当前URL中提取
            enable_scroll: 是否启用自动滚动加载更多评论
            scroll_count: 滚动次数（如果启用滚动）
            
        Returns:
            评论列表，失败返回空列表
        """
        try:
            # 如果没有提供note_id，从当前URL中提取
            if not note_id:
                current_url = self.browser.get_current_url()
                match = re.search(r'/explore/([a-f0-9]+)', current_url)
                if match:
                    note_id = match.group(1)
                    logger.info(f"从URL中提取到帖子ID: {note_id}")
                else:
                    logger.error("无法从URL中提取帖子ID")
                    return []

            logger.info(f"\n开始获取帖子 {note_id} 的评论...")

            all_comments = []
            processed_request_ids = set()

            # 先等待1秒让页面初始化
            time.sleep(1)

            # 立即处理初始加载的评论
            logger.info("\n处理页面初始加载的评论...")
            logs = self.browser.get_network_logs()
            initial_comment_count = 0

            for log in logs:
                try:
                    message = json.loads(log['message'])['message']
                    if message['method'] == 'Network.responseReceived':
                        response_url = message['params']['response']['url']

                        if 'api/sns/web/v2/comment/page' in response_url:
                            request_id = message['params']['requestId']

                            # 检查note_id是否匹配
                            if note_id and f'note_id={note_id}' not in response_url:
                                continue

                            # 避免重复处理
                            if request_id in processed_request_ids:
                                continue

                            # 立即获取响应体
                            try:
                                response_body = self.browser.execute_cdp_cmd(
                                    'Network.getResponseBody',
                                    {'requestId': request_id}
                                )

                                if 'body' in response_body:
                                    processed_request_ids.add(request_id)
                                    logger.info(f"  获取初始评论接口响应 (ID: {request_id[:8]}...)")

                                    # 提取评论
                                    comments = self._extract_comments_from_response(response_body['body'])
                                    all_comments.extend(comments)
                                    initial_comment_count += len(comments)
                                    logger.info(f"  获取 {len(comments)} 条初始评论")
                            except Exception as e:
                                error_msg = str(e)
                                if 'No resource with given identifier found' not in error_msg:
                                    logger.error(f"  获取失败: {error_msg}")
                except:
                    continue

            logger.info(f"初始加载完成，获取到 {initial_comment_count} 条评论\n")

            # 再等待2秒让页面稳定
            time.sleep(2)

            # 如果启用滚动，滚动时收集更多评论
            if enable_scroll:
                scroll_comments = self._scroll_page(scroll_count=scroll_count, note_id=note_id)
                all_comments.extend(scroll_comments)

            logger.info(f"\n统计信息:")
            logger.info(f"  - 初始加载获取 {initial_comment_count} 条评论")
            logger.info(f"  - 滚动加载获取 {len(all_comments) - initial_comment_count} 条评论")
            logger.info(f"  - 总共获取到 {len(all_comments)} 条评论\n")

            return all_comments

        except Exception as e:
            logger.error(f"\n获取评论时出错: {e}")
            import traceback
            traceback.print_exc()
            return []

    def print_comments(self, comments: List):
        """格式化打印评论列表
        
        Args:
            comments: 评论列表
        """
        if not comments:
            logger.warning("\n未找到评论")
            return

        logger.info(f"\n{'=' * 80}")
        logger.info(f"总共获取到 {len(comments)} 条评论")
        logger.info(f"{'=' * 80}\n")

        for comment in comments:
            logger.info(f"\n[评论]")
            logger.info(f"  用户: {comment.user_info.nickname}")
            logger.info(f"  内容: {comment.content}")
            logger.info(f"  点赞数: {comment.like_count}")
            logger.info(f"  IP归属地: {comment.ip_location}")
            logger.info(f"  回复数: {comment.sub_comment_count}")
            logger.info(f"  评论ID: {comment.comment_id}")

            # 打印语音评论
            if comment.audio_info:
                logger.info(f"  [语音评论] {comment.audio_info.tag_text}")
                logger.info(f"  识别文本: {comment.audio_info.asr_text}")

            # 打印图片
            if comment.pictures:
                logger.info(f"  [图片评论] {len(comment.pictures)} 张图片")
                for idx, pic_url in enumerate(comment.pictures, 1):
                    logger.debug(f"    图片{idx}: {pic_url}")

            # 打印子评论
            if comment.sub_comments:
                logger.info(f"\n  --- 回复列表 ({len(comment.sub_comments)} 条) ---")
                for idx, sub in enumerate(comment.sub_comments, 1):
                    logger.info(f"\n  [回复 {idx}]")
                    logger.info(f"    用户: {sub.user_info.nickname}")
                    logger.info(f"    内容: {sub.content}")
                    logger.info(f"    点赞数: {sub.like_count}")
                    logger.info(f"    IP归属地: {sub.ip_location}")
                    logger.info(f"    评论ID: {sub.comment_id}")

                    # 子评论的图片
                    if sub.pictures:
                        logger.info(f"    [图片回复] {len(sub.pictures)} 张图片")
                        for pic_idx, pic_url in enumerate(sub.pictures, 1):
                            logger.debug(f"      图片{pic_idx}: {pic_url}")

                    if sub.target_comment:
                        target_name = sub.target_comment.user_info.nickname if sub.target_comment.user_info else "?"
                        target_id = sub.target_comment.comment_id if sub.target_comment.comment_id else "未知"
                        logger.info(f"    回复给: @{target_name} (ID: {target_id})")
            logger.info(f"\n{'-' * 80}")

    @log_execution
    def reply_to_comment(self, comment_id: str, reply_text: str) -> bool:
        """回复评论
        
        Args:
            comment_id: 评论ID
            reply_text: 回复内容
            
        Returns:
            bool: 是否成功
        """
        try:
            logger.info(f"\n开始回复评论 ID: {comment_id}")
            logger.info(f"回复内容: {reply_text}")

            # 1. 找到评论元素
            comment_selector = f"#comment-{comment_id}"
            logger.debug(f"  查找评论元素: {comment_selector}")

            try:
                comment_element = self.browser.find_element(
                    By.CSS_SELECTOR,
                    comment_selector,
                    timeout=5
                )
                logger.info(f"  找到评论元素")
            except:
                logger.error(f"  未找到评论ID: {comment_id}")
                return False

            # 2. 滚动到评论可见
            self.browser.execute_script(
                "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                comment_element
            )
            time.sleep(1)

            # 3. 找到并点击回复按钮
            reply_button_selector = f"{comment_selector} .reply.icon-container"
            logger.debug(f"  查找回复按钮: {reply_button_selector}")

            try:
                reply_button = self.browser.find_element(
                    By.CSS_SELECTOR,
                    reply_button_selector,
                    timeout=5,
                    clickable=True
                )
                logger.info(f"  找到回复按钮")

                reply_button.click()
                logger.info(f"  已点击回复按钮")
                time.sleep(1.5)

            except Exception as e:
                logger.error(f"  找不到回复按钮: {e}")
                return False

            # 4. 等待回复输入框出现
            input_selector = "p#content-textarea.content-input"
            logger.debug(f"  等待输入框出现...")

            try:
                input_element = self.browser.find_element(
                    By.CSS_SELECTOR,
                    input_selector,
                    timeout=5,
                    clickable=True
                )
                logger.info(f"  输入框已出现")
            except:
                logger.error(f"  输入框未出现")
                return False

            # 5. 点击输入框并输入内容
            input_element.click()
            time.sleep(0.5)

            # 使用 JavaScript 设置 contenteditable 元素的内容
            self.browser.execute_script("""
                const elem = arguments[0];
                const text = arguments[1];
                
                elem.textContent = text;
                elem.focus();
                
                const inputEvent = new Event('input', { bubbles: true });
                elem.dispatchEvent(inputEvent);
                
                const changeEvent = new Event('change', { bubbles: true });
                elem.dispatchEvent(changeEvent);
            """, input_element, reply_text)

            logger.info(f"  已输入回复内容: {reply_text}")
            time.sleep(1.5)

            # 6. 点击发送按钮
            logger.debug(f"  查找发送按钮...")

            try:
                send_button_selector = ".engage-bar .right-btn-area button.btn.submit"

                send_button = WebDriverWait(self.browser.driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, send_button_selector))
                )
                logger.info(f"  找到发送按钮")

                # 检查按钮是否可用
                is_disabled = send_button.get_attribute('disabled')
                logger.info(f"  按钮状态: {'禁用' if is_disabled else '可用'}")

                # 如果按钮被禁用，等待最多3秒直到可用
                if is_disabled:
                    logger.debug(f"  等待按钮变为可用...")
                    send_button = WebDriverWait(self.browser.driver, 3).until(
                        lambda d: d.find_element(By.CSS_SELECTOR, send_button_selector)
                                  and not d.find_element(By.CSS_SELECTOR, send_button_selector).get_attribute(
                            'disabled')
                    )
                    logger.info(f"  按钮已可用")

                # 点击发送按钮
                send_button.click()
                logger.info(f"  已点击发送按钮")
                time.sleep(2)

                logger.info(f"\n 回复成功！")
                return True

            except Exception as e:
                logger.error(f"  发送按钮处理失败: {e}")

                # 尝试找到取消按钮关闭输入框
                try:
                    cancel_button = self.browser.driver.find_element(
                        By.CSS_SELECTOR,
                        ".engage-bar .right-btn-area button.btn.cancel"
                    )
                    cancel_button.click()
                    logger.info(f"  已点击取消按钮")
                except:
                    pass

                return False

        except Exception as e:
            logger.error(f"\n[ERROR] 回复评论失败: {e}")
            import traceback
            traceback.print_exc()
            return False
