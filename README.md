# 小红书自动化工具

##  免责声明

- 本项目仅供学习和研究Selenium自动化技术使用
- 使用本项目前请确保遵守小红书平台的相关规定和条款
- 因使用本项目导致的任何问题，作者不承担任何责任
- 请勿将本项目用于任何非法用途

## 项目结构

```
./
├── business/                 # 业务管理器
│   ├── __init__.py
│   ├── ai_manager.py         # AI 管理模块（文案生成、评论回复）
│   ├── comment_manager.py    # 评论管理模块
│   ├── note_manager.py       # 笔记管理模块
│   ├── publish_manager.py    # 发布管理模块
│   └── xhs_content_styles/   # 内容风格模块
│       ├── __init__.py
│       ├── base_style.py
│       ├── controversial_style.py
│       ├── fairy_style.py
│       ├── provocative_style.py
│       ├── style_factory.py
│       └── unreasonable_style.py
├── core/                     # 核心模块
│   ├── __init__.py
│   ├── ai_client.py          # AI 客户端（支持 OpenAI、智谱AI、Ollama）
│   ├── browser_manager.py    # 浏览器管理模块
│   ├── config.py             # 配置管理模块
│   ├── decorators.py         # 装饰器模块
│   ├── dom_manager.py        # DOM元素管理模块（数据库存储 + 缓存机制）
│   ├── exceptions.py         # 自定义异常类
│   ├── logger.py             # 日志管理模块（支持彩色输出）
│   ├── models/               # 数据模型定义
│   │   ├── __init__.py
│   │   ├── ai_config.py
│   │   ├── audio_info.py
│   │   ├── comment.py
│   │   ├── dom_element.py    # DOM元素数据模型
│   │   ├── note_info.py
│   │   ├── publish_content.py
│   │   └── user_info.py
│   └── xhs_client.py         # 小红书客户端 - 整合所有管理器
├── data/                     # 数据目录（用于存放训练数据）
├── md/                       # 文档目录
│   ├── ARCHITECTURE.md
│   └── MIGRATION.md
├── test/                     # 测试脚本
│   ├── test_ai.py
│   └── test_xhs.py
├── LICENSE
├── README.md                 # 项目文档
├── TODO.md                   # 待办事项
├── config_personal.py        # 个人配置文件
├── config_personal_example.py # 配置文件示例
├── custom_ai_example.py      # 自定义 AI 客户端示例
├── example_ai_usage.py       # AI 功能使用示例
├── install.ps1               # Windows 安装脚本
├── install.sh*               # Linux/macOS 安装脚本
├── requirements.txt          # 依赖列表
├── setup_ollama.bat          # Ollama 本地模型安装脚本 (Windows)
├── setup_ollama.sh*          # Ollama 本地模型安装脚本 (macOS/Linux)
├── update_readme_tree.sh*    # 更新目录树脚本
├── utils.py                  # 工具函数模块
└── validate_docstrings.py    # Docstring 校验工具
```

## 项目待办事项

参考 [TODO.md](TODO.md) 了解项目当前的开发状态、计划中的功能和已完成的工作。

## 核心功能

### DOM元素智能管理

新增DOM元素管理功能，提供以下特性：

- **数据库存储**: 使用SQLite数据库存储DOM元素信息（元素ID、选择器、类型、位置、文本内容、更新时间）
- **二级缓存机制**: 结合内存缓存和数据库缓存，提高页面操作效率
- **自动初始化**: 启动时自动将配置中的选择器初始化到数据库
- **智能查找**: 优先从缓存获取，缓存未命中时从数据库获取
- **动态更新**: 页面操作时自动更新DOM元素信息

## 快速开始

### 环境要求

- Python 3.7+
- Chrome 浏览器
- 小红书账号

### 安装依赖

#### 方式1：使用安装脚本（推荐）

**Linux/macOS:**
```bash
# 克隆项目
git clone https://github.com/xTreeRoot/xiaohongshu-bot.git
cd xiaohongshu-bot

# 运行安装脚本
chmod +x install.sh
./install.sh
```

**Windows:**
```powershell
# 克隆项目
git clone https://github.com/xTreeRoot/xiaohongshu-bot.git
cd xiaohongshu-bot

# 运行安装脚本
.\install.ps1
```

#### 方式2：手动安装

```bash
# 克隆项目
git clone https://github.com/xTreeRoot/xiaohongshu-bot.git
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

## 注意事项

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
   -  校验通过后才能提交代码
   -  如果校验失败，会列出所有缺少docstring的文件
   -  每个Python文件的第一行必须包含模块说明，格式：`"""模块说明"""`
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