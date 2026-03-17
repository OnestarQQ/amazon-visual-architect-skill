#!/usr/bin/env python3
"""
Amazon Visual Architect Skill - 安装脚本
自动安装依赖库并配置环境
"""

import subprocess
import sys
import os

def install_dependencies():
    """安装必需的依赖库"""
    
    print("🔧 Amazon Visual Architect - 安装依赖库")
    print("=" * 50)
    
    # 必需的依赖库
    required_packages = [
        "aiohttp>=3.8.0",
        "asyncio",
        "requests>=2.25.0"
    ]
    
    print("📦 安装以下依赖库:")
    for package in required_packages:
        print(f"  - {package}")
    print()
    
    # 安装依赖
    for package in required_packages:
        try:
            print(f"⏳ 正在安装 {package}...")
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", package
            ])
            print(f"✅ {package} 安装成功")
        except subprocess.CalledProcessError as e:
            print(f"❌ {package} 安装失败: {e}")
            return False
    
    print("\n🎉 所有依赖库安装完成!")
    return True

def create_config_template():
    """创建配置模板文件"""
    
    config_content = """# Amazon Visual Architect 配置文件
# 将你的API密钥填入下方

# Stability AI API Key (推荐)
STABILITY_API_KEY=sk-your-stability-api-key-here

# OpenAI API Key  
OPENAI_API_KEY=sk-your-openai-api-key-here

# Replicate API Key
REPLICATE_API_KEY=your-replicate-token-here

# 智谱清言 API Key
ZHIPU_API_KEY=your-zhipu-api-key-here

# 默认设置
DEFAULT_PLATFORM=stability
DEFAULT_IMAGE_SIZE=1024x1024
DEFAULT_QUALITY=high
"""
    
    try:
        with open("config.env", "w", encoding="utf-8") as f:
            f.write(config_content)
        print("📝 配置模板已创建: config.env")
        print("   请编辑此文件添加你的API密钥")
        return True
    except Exception as e:
        print(f"❌ 配置文件创建失败: {e}")
        return False

def test_installation():
    """测试安装是否成功"""
    
    print("\n🧪 测试安装...")
    
    try:
        # 测试导入
        import aiohttp
        import asyncio
        import json
        print("✅ 依赖库导入测试通过")
        
        # 测试脚本
        if os.path.exists("scripts/image_generator.py"):
            print("✅ 图片生成模块存在")
        else:
            print("⚠️ 图片生成模块未找到")
        
        if os.path.exists("run_architect.py"):
            print("✅ 主调用脚本存在")
        else:
            print("⚠️ 主调用脚本未找到")
            
        return True
        
    except ImportError as e:
        print(f"❌ 导入测试失败: {e}")
        return False

def show_usage_guide():
    """显示使用指南"""
    
    print("\n" + "=" * 50)
    print("🎉 Amazon Visual Architect v8.1 安装完成!")
    print("=" * 50)
    
    print("\n📋 快速开始:")
    print("1. 编辑 config.env 文件，添加你的API密钥")
    print("2. 使用技能:")
    
    print("""
    # 仅生成Prompt
    请使用亚马逊全案视觉架构师技能：
    - 核心卖点: 防水、轻便、大容量
    - 销售区域: 美国
    - 目标受众: 户外爱好者
    
    # 直接生成图片  
    请使用亚马逊全案视觉架构师技能生成图片：
    - 核心卖点: 降噪、长续航、舒适佩戴
    - generate_images: true
    - image_platform: stability
    - api_key: sk-xxxxxxxx
    """)
    
    print("\n💡 支持的AI绘图平台:")
    print("  - stability: Stability AI (推荐商用)")
    print("  - openai: OpenAI DALL-E 3 (文字理解强)")  
    print("  - replicate: Replicate (性价比高)")
    print("  - zhipu: 智谱清言 (国内快速)")
    
    print("\n📖 详细文档:")
    print("  - README.md - 完整使用指南")
    print("  - examples.md - 丰富使用示例")
    print("  - prompts.md - 完整prompt系统")
    
    print("\n🔗 获取API密钥:")
    print("  - Stability AI: https://platform.stability.ai/")
    print("  - OpenAI: https://platform.openai.com/api-keys")
    print("  - Replicate: https://replicate.com/account/api-tokens")
    print("  - 智谱清言: https://open.bigmodel.cn/")

def main():
    """主安装函数"""
    
    print("🎨 Amazon Visual Architect v8.1 - 安装程序")
    print("专业电商视觉设计 + 直接AI生图功能")
    print("=" * 60)
    
    # 1. 安装依赖
    if not install_dependencies():
        print("❌ 依赖安装失败，请检查网络连接和权限")
        return
    
    # 2. 创建配置模板
    create_config_template()
    
    # 3. 测试安装
    if test_installation():
        print("✅ 安装测试通过")
    else:
        print("⚠️ 安装测试未完全通过，但基础功能可用")
    
    # 4. 显示使用指南
    show_usage_guide()

if __name__ == "__main__":
    main()