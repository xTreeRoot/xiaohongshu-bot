# 小红书自动化工具

##  免责声明

- 本项目仅供学习和研究Selenium自动化技术使用
- 使用本项目前请确保遵守小红书平台的相关规定和条款
- 因使用本项目导致的任何问题，作者不承担任何责任
- 请勿将本项目用于任何非法用途

项目结构详情请参见 [STRUCTURE.md](md/STRUCTURE.md)。

## 项目待办事项

参考 [TODO.md](TODO.md) 了解项目当前的开发状态、计划中的功能和已完成的工作。


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

#### 1. 个人配置文件

创建个人配置文件：

```bash
cp config_personal_example.py config_personal.py
```

编辑 `config_personal.py`，填写你的个人信息：

```python
PERSONAL_CONFIG = {
    # ========== 小红书配置 ==========
    # 你的小红书个人主页 URL
    "user_profile_url": "https://www.xiaohongshu.com/user/profile/YOUR_USER_ID",  # 替换为你的用户ID

    # ========== 浏览器配置 ==========
    # Chrome 用户数据目录（用于保存登录状态）
    "chrome_user_data_dir": "~/selenium_chrome_data",
    # 是否使用无头模式（无界面运行）
    "headless": False,

    # ========== 等待时间配置 ==========
    "wait_timeout": 10,        # 默认等待超时时间（秒）
    "page_load_timeout": 3,    # 页面加载超时时间（秒）

    # ========== AI 配置 ==========
    # AI API Key（必填）
    "ai_api_key": "your-api-key-here",  # 你的API密钥

    # AI API Base URL（可选）
    "ai_base_url": "https://open.bigmodel.cn/api/paas/v4/",

    # AI 模型（可选）
    "ai_model": "glm-4",

    # AI 温度参数（可选，范围 0-2，控制生成内容的随机性和创造性）
    "ai_temperature": 0.9,
}
```

#### 2. 配置说明

你的小红书用户ID可以从个人主页URL获取：
```
https://www.xiaohongshu.com/user/profile/YOUR_USER_ID
```


## 注意事项

1. **首次运行**：需要手动登录小红书账号，后续会自动复用登录状态
2. **浏览器数据**：使用独立的Chrome用户数据目录，不会影响你的主浏览器
3. **配置修改**：请在 `config_personal.py` 中替换 `YOUR_USER_ID` 为你的小红书用户ID
4. **遵守规则**：请遵守小红书平台规则，避免频繁操作
5. **日志追踪**：建议配置日志文件，便于问题追踪
6. **仅供学习**：本项目仅供学习和研究目的，请勿用于商业目的或恶意行为

##  贡献

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

##  License

MIT License