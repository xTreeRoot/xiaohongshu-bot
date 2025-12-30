# 小红书自动化工具

## 📁 项目结构

```
./
├── business/                 # 业务管理器
│   ├── __init__.py
│   ├── comment_manager.py    # 评论管理模块
│   ├── note_manager.py       # 笔记管理模块
│   └── publish_manager.py    # 发布管理模块
├── core/                     # 核心模块
│   ├── __init__.py
│   ├── browser_manager.py    # 浏览器管理模块
│   ├── config.py             # 配置管理模块
│   ├── decorators.py         # 装饰器模块
│   ├── exceptions.py         # 自定义异常类
│   ├── logger.py             # 日志管理模块
│   ├── models.py             # 数据模型定义
│   └── xhs_client.py         # 小红书客户端 - 整合所有管理器
├── md/                       # 文档目录
│   ├── ARCHITECTURE.md
│   ├── MIGRATION.md
│   └── REFACTORING_SUMMARY.md
├── LICENSE
├── README.md                 # 项目文档
├── README.md.backup
├── config_personal.py
├── config_personal.py.copy
├── install.ps1               # Windows安装脚本
├── install.sh*               # Linux/macOS安装脚本
├── requirements.txt          # 依赖列表
├── test_xhs.py               # 小红书自动化测试脚本
├── update_readme_tree.sh*    # 更新目录树脚本
├── utils.py                  # 工具函数模块
└── validate_docstrings.py

4 directories, 27 files
```

## ✨ 核心特性

### 1. 模块化架构（重构亮点）
- **分层设计**：浏览器管理 → 功能管理器 → 统一客户端
- **职责分离**：
  - `BrowserManager`: 浏览器初始化、元素查找、基础操作
  - `NoteManager`: 笔记搜索、打开
  - `CommentManager`: 评论获取、解析、回复
  - `PublishManager`: 内容发布流程
  - `XHSClient`: 统一API入口
- **易于扩展**：新增功能只需创建新的管理器
- **依赖注入**：管理器通过构造函数接收浏览器实例

### 2. 代码质量提升
- **类型提示**：完整的类型注解，提高代码可读性
- **装饰器**：重试机制和日志记录自动化
- **单一职责**：每个类和函数职责明确
- **工具类**：通用功能封装，代码复用性强

### 3. 开发体验优化
- **统一接口**：通过 `XHSClient` 提供简洁的API
- **测试友好**：独立的测试脚本，支持多种测试场景
- **配置分离**：硬编码配置全部移至配置文件
- **日志追踪**：详细的日志记录，便于调试

## 🚀 快速开始

### 环境要求

- Python 3.7+
- Chrome 浏览器
- 小红书账号

### 安装依赖

#### 方式1：使用安装脚本（推荐）

**Linux/macOS:**
```bash
# 克隆项目
git clone https://github.com/YOUR_USERNAME/xiaohongshu-bot.git
cd xiaohongshu-bot

# 运行安装脚本
chmod +x install.sh
./install.sh
```

**Windows:**
```powershell
# 克隆项目
git clone https://github.com/YOUR_USERNAME/xiaohongshu-bot.git
cd xiaohongshu-bot

# 运行安装脚本
.\install.ps1
```

#### 方式2：手动安装

```bash
# 克隆项目
git clone https://github.com/YOUR_USERNAME/xiaohongshu-bot.git
cd xiaohongshu-bot

# 创建虚拟环境（可选）
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

### 配置

在运行之前，请修改 `core/config.py` 中的个人信息：

```python
# core/config.py
user_profile_url: str = "https://www.xiaohongshu.com/user/profile/YOUR_USER_ID"  # 替换为你的个人主页URL
```

### 基本使用

#### 方式1: 直接运行测试脚本（推荐）

```bash
python test_xhs.py
```

然后根据菜单选择要执行的测试场景。

#### 方式2: 编程调用

```python
from core.xhs_client import XHSClient
from core.models import PublishContent

# 创建客户端
client = XHSClient()

try:
    # 示例1: 发布内容
    publish_content = PublishContent(
        content="这是文字内容",
        title="这是标题"
    )
    client.publish_content(publish_content)

    # 示例2: 搜索并获取评论
    note_info = client.search_and_open_note(keyword="关键词")
    if note_info:
        comments = client.get_comments(enable_scroll=True, scroll_count=5)
        client.print_comments(comments)

    # 示例3: 回复评论
    if comments:
        client.reply_comment(
            comment_id=comments[0].comment_id,
            reply_text="你好！"
        )

finally:
    # 关闭浏览器
    client.quit()
```

### 配置自定义

```python
from core.config import config

# 修改浏览器配置
config.browser.headless = True  # 无头模式
config.browser.user_data_dir = "~/my_chrome_data"

# 修改等待时间
config.wait.default_timeout = 15
config.wait.page_load_timeout = 5

# 修改小红书URL
config.xhs.user_profile_url = "你的个人主页URL"
```

## 📚 模块说明

### 核心模块

#### browser_manager.py - 浏览器管理器
- `BrowserManager`: 浏览器管理核心类
  - `find_element()`: 查找元素（支持重试）
  - `click_element()`: 点击元素
  - `input_text()`: 输入文本
  - `navigate_to()`: 页面导航
  - `get_network_logs()`: 获取网络日志
  - `execute_script()`: 执行JS脚本

#### note_manager.py - 笔记管理器
- `NoteManager`: 笔记操作管理
  - `open_user_profile()`: 打开个人主页
  - `search_and_open_note()`: 搜索并打开笔记

#### comment_manager.py - 评论管理器
- `CommentManager`: 评论操作管理
  - `fetch_comments()`: 获取评论列表
  - `print_comments()`: 格式化打印评论
  - `reply_to_comment()`: 回复评论
  - `_scroll_page()`: 滚动加载更多评论

#### publish_manager.py - 发布管理器
- `PublishManager`: 发布操作管理
  - `open_publish_page()`: 打开发布页
  - `create_text_to_image()`: 文字生成图片
  - `proceed_to_publish_page()`: 进入发布页
  - `fill_and_publish()`: 填写并发布
  - `publish_workflow()`: 完整发布流程

#### xhs_client.py - 统一客户端
- `XHSClient`: 小红书客户端（统一API入口）
  - 笔记相关: `search_and_open_note()`
  - 评论相关: `get_comments()`, `print_comments()`, `reply_comment()`
  - 发布相关: `publish_content()`

### 支持模块

#### config.py - 配置管理
- `BrowserConfig`: 浏览器相关配置
- `WaitConfig`: 等待时间配置
- `XHSConfig`: 小红书平台配置
- `AppConfig`: 应用总配置

#### logger.py - 日志管理
- 单例模式的日志管理器
- 支持控制台和文件输出

#### models.py - 数据模型
- `UserInfo`: 用户信息
- `Comment`: 评论数据
- `NoteInfo`: 笔记信息
- `PublishContent`: 发布内容

#### exceptions.py - 异常定义
- `BrowserInitError`: 浏览器初始化失败
- `ElementNotFoundError`: 元素未找到
- `PublishError`: 发布失败

#### decorators.py - 装饰器
- `@retry`: 自动重试装饰器
- `@log_execution`: 日志记录装饰器

#### utils.py - 工具函数
- `CommentParser`: 评论解析器
- `URLExtractor`: URL提取器
- `DataValidator`: 数据验证器

#### test_xhs.py - 测试脚本
- `test_comment_and_reply()`: 测试评论和回复
- `test_publish()`: 测试发布内容
- `test_only_fetch_comments()`: 仅测试获取评论

## 🔧 高级用法

### 自定义重试策略

```python
from core.decorators import retry
from core.exceptions import ElementNotFoundError

@retry(max_attempts=5, delay=2.0, exceptions=(ElementNotFoundError,))
def custom_click(element):
    element.click()
```

### 日志配置

```python
from core.logger import Logger

# 创建带文件输出的日志
logger = Logger.get_logger(
    name="XHSPublisher",
    log_file="logs/xhs.log"
)
```

### 数据模型使用

```python
from core.models import Comment

# 从字典创建评论对象
comment_data = {...}
comment = Comment.from_dict(comment_data)

# 转换为字典
comment_dict = comment.to_dict()
```

## 📊 重构效果对比

| 指标 | 原始版本 | 重构版本 |
|------|---------|----------|
| 架构设计 | 单一类995行 | 分层架构，5个管理器 |
| 职责分离 | 混合在一起 | 浏览器/笔记/评论/发布独立 |
| 代码行数 | 995行 | BrowserManager 161行<br>NoteManager 109行<br>CommentManager 460行<br>PublishManager 172行<br>XHSClient 99行 |
| 配置方式 | 硬编码 | 配置文件 |
| 日志系统 | print混合 | 统一logging |
| 测试方式 | 混在__main__ | 独立test_xhs.py |
| API接口 | 直接调用内部方法 | XHSClient统一接口 |
| 可扩展性 | 低（需修改主类） | 高（新增管理器） |
| 可维护性 | 中 | 高 |
| 可测试性 | 低 | 高 |

## 🎯 最佳实践

1. **配置优先**：所有可变参数都应放在配置文件中
2. **日志记录**：关键步骤都应记录日志
3. **异常处理**：使用特定的异常类，便于问题定位
4. **类型提示**：添加类型注解，提高代码可读性
5. **单元测试**：为关键函数编写测试用例

## 📝 更新日志

### v3.0.0 (分层架构重构)
- ✨ 分层架构设计（浏览器层 → 管理器层 → 客户端层）
- ✨ 职责分离（5个独立管理器）
- ✨ 统一API接口（XHSClient）
- ✨ 独立测试脚本（test_xhs.py）
- ✨ 依赖注入模式
- ✨ 更好的代码复用

### v2.0.0 (工程化重构)
-  模块化架构设计
-  配置管理系统
-  统一日志管理
-  数据模型定义
-  自定义异常体系
-  装饰器支持
-  工具类封装
-  类型提示完善

## ️ 注意事项

1. **首次运行**：需要手动登录小红书账号，后续会自动复用登录状态
2. **浏览器数据**：使用独立的Chrome用户数据目录，不会影响你的主浏览器
3. **配置修改**：请在 `core/config.py` 中替换 `YOUR_USER_ID` 为你的小红书用户ID
4. **遵守规则**：请遵守小红书平台规则，避免频繁操作
5. **日志追踪**：建议配置日志文件，便于问题追踪
6. **仅供学习**：本项目仅供学习和研究目的，请勿用于商业目的或恶意行为

## 👥 贡献

欢迎贡献代码、报告问题或提出改进建议！

### 贡献流程

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. **确保所有Python文件包含docstring**
   ```bash
   # 运行docstring校验器
   python3 validate_docstrings.py
   ```
   - ✅ 校验通过后才能提交代码
   - ❌ 如果校验失败，会列出所有缺少docstring的文件
   - 每个Python文件的第一行必须包含模块说明，格式：`"""模块说明"""`
4. 提交你的修改 (`git commit -m 'Add some AmazingFeature'`)
5. 推送到分支 (`git push origin feature/AmazingFeature`)
6. 提交 Pull Request

### 代码规范

- **Docstring要求**：所有Python文件（除`__init__.py`外）必须在第一行包含docstring
- **格式示例**：
  ```python
  """用户管理模块"""
  import os
  # ... 其他代码
  ```
- **校验工具**：提交前运行 `python3 validate_docstrings.py` 确保通过校验

##  免责声明

- 本项目仅供学习和研究Selenium自动化技术使用
- 使用本项目前请确保遵守小红书平台的相关规定和条款
- 因使用本项目导致的任何问题，作者不承担任何责任
- 请勿将本项目用于任何非法用途

## 📄 License

MIT License
