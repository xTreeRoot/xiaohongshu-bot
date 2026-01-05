# 项目结构

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
│   ├── MIGRATION.md
│   └── STRUCTURE.md          # 项目结构文档
├── test/                     # 测试脚本
│   ├── test_ai.py
│   └── test_xhs.py
├── LICENSE
├── README.md                 # 项目文档
├── TODO.md                   # 待办事项
├── config_personal.py        # 个人配置文件
├── config_personal_example.py # 配置文件示例
├── example/custom_ai_example.py      # 自定义 AI 客户端示例
├── example/example_ai_usage.py       # AI 功能使用示例
├── install.ps1               # Windows 安装脚本
├── install.sh*               # Linux/macOS 安装脚本
├── requirements.txt          # 依赖列表
├── setup_ollama.bat          # Ollama 本地模型安装脚本 (Windows)
├── setup_ollama.sh*          # Ollama 本地模型安装脚本 (macOS/Linux)
├── update_readme_tree.sh*    # 更新目录树脚本
├── utils.py                  # 工具函数模块
└── validate_docstrings.py    # Docstring 校验工具
```