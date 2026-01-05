"""
个人配置文件模板

使用步骤：
1. 复制此文件并重命名为 config_personal.py
   cp config_personal.py.copy config_personal.py
   
2. 编辑 config_personal.py，填写你的个人信息

3. config_personal.py 会被 .gitignore 忽略，不会被提交到仒库
"""

# 个人配置示例文件
# 复制此文件为 config_personal.py 并填入你的配置

PERSONAL_CONFIG = {
    # ========== 小红书配置 ==========
    # 你的小红书个人主页 URL
    "user_profile_url": "https://www.xiaohongshu.com/user/profile/YOUR_USER_ID",

    # ========== 浏览器配置 ==========
    # Chrome 用户数据目录
    "chrome_user_data_dir": "~/selenium_chrome_data",
    # 是否使用无头模式
    "headless": False,

    # ========== 等待时间配置 ==========
    "wait_timeout": 10,
    "page_load_timeout": 3,

    # ========== AI 配置 ==========
    # AI API Key（必填）
    # 智谱 AI (GLM-4)：在 https://open.bigmodel.cn/ 获取
    # OpenAI: 以 sk- 开头
    "ai_api_key": "your-api-key-here",

    # AI API Base URL（可选）
    # 默认使用智谱 AI，不需要配置此项
    # 如果使用 OpenAI 或第三方 API，可以配置：
    # "ai_base_url": "https://api.openai.com/v1",
    # "ai_base_url": "https://api.openai-proxy.com/v1",  # 国内中转
    # "ai_base_url": "http://localhost:11434/v1",  # Ollama 本地
    # "ai_base_url": "https://api.openai.com/v1",

    # AI 模型（可选）
    # 智谱 AI 模型：
    # - glm-4 （推荐，智能度高）
    # - glm-3-turbo （快速便宜）
    # OpenAI 模型：
    # - gpt-3.5-turbo （快速便宜）
    # - gpt-4 （质量更高）
    # - gpt-4-turbo （更快的 GPT-4）
    "ai_model": "glm-4",

    # AI 温度参数（可选，范围 0-2，控制生成内容的随机性和创造性）
    # 温度值说明：
    #   0.0-0.3: 非常确定、保守，适合代码生成、翻译、数学计算
    #   0.4-0.7: 较为稳定可靠，适合日常对话、客服、问答系统
    #   0.8-1.2: 平衡创造性和准确性，适合通用场景、文章写作
    #   1.3-2.0: 非常随机、创造性强，适合创意写作、头脑风暴
    # 
    # 小红书场景推荐：
    #   小仙女风格: 0.9-1.1 （甜美有个性）
    #   逆天言论/引战: 1.0-1.3 （争议性和话题性）
    #   评论回复: 0.8-1.0 （针对性和创意平衡）
    "ai_temperature": 0.9,
}
