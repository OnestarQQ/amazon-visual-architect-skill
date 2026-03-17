#!/usr/bin/env python3
"""
Amazon Visual Architect v8.2 - OpenClaw集成脚本
专注于生成高质量AI绘图prompt
"""

import sys
import json
import os
from datetime import datetime

try:
    from prompt_generator import AmazonVisualArchitectPrompts
    DEPENDENCIES_OK = True
except ImportError as e:
    DEPENDENCIES_OK = False
    IMPORT_ERROR = str(e)

def parse_architect_request(message):
    """解析用户的视觉架构师请求"""
    
    # 检查是否是视觉架构师技能请求
    trigger_keywords = [
        "亚马逊全案视觉架构师",
        "amazon visual architect", 
        "电商视觉设计",
        "listing主图",
        "a+图片"
    ]
    
    if not any(keyword in message.lower() for keyword in trigger_keywords):
        return None
    
    # 提取关键参数
    params = {
        "customer_keywords": [],
        "generate_images": False,
        "image_platform": "stability", 
        "api_key": "",
        "salesRegion": "美国",
        "language": "英语"
    }
    
    # 简化的参数提取
    lines = message.split('\n')
    for line in lines:
        line = line.strip()
        if any(keyword in line for keyword in ['卖点:', '核心卖点:', 'customer_keywords:']):
            content = line.split(':')[-1].strip()
            params["customer_keywords"] = [k.strip() for k in content.replace('、', ',').split(',') if k.strip()]

        elif '销售区域:' in line or 'salesRegion:' in line:
            params["salesRegion"] = line.split(':')[-1].strip()
        elif '语言:' in line or 'language:' in line:
            params["language"] = line.split(':')[-1].strip()
    
    return params

def run_amazon_visual_architect(user_message):
    """运行亚马逊全案视觉架构师"""
    
    if not DEPENDENCIES_OK:
        return {
            "error": f"模块加载失败: {IMPORT_ERROR}",
            "solution": "请确保prompt_generator.py文件存在"
        }
    
    try:
        architect = AmazonVisualArchitectPrompts()
        results = architect.generate_complete_solution(user_message)
        
        # 格式化输出
        output = {
            "success": True,
            "session_id": results["session_id"],
            "brand_dna": results["brand_dna"],
            "prompts": results["prompts"],
            "summary": {
                "total_prompts": len(results["prompts"]),
                "listing_images": len([p for p in results["prompts"] if "Listing" in p["category"]]),
                "aplus_images": len([p for p in results["prompts"] if "A+" in p["category"]]),
                "brand_color": results["brand_dna"]["brandColor (品牌主色)"]
            }
        }
        
        # 添加使用指南
        if "usage_guide" in results:
            output["usage_guide"] = results["usage_guide"]
        
        return output
        
    except Exception as e:
        return {
            "error": f"生成失败: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }

def format_output_for_chat(result):
    """格式化输出用于聊天显示"""
    
    if "error" in result:
        return f"❌ **错误**: {result['error']}\n\n{result.get('solution', '')}"
    
    output = []
    output.append(f"🎨 **Amazon Visual Architect v8.1** - 生成完成!")
    output.append(f"📋 **会话ID**: `{result['session_id']}`")
    output.append("")
    
    # 品牌基因
    brand_dna = result["brand_dna"]
    output.append("## 🎨 品牌基因报告")
    output.append(f"- **品牌主色**: {brand_dna['brandColor (品牌主色)']}")
    output.append(f"- **字体风格**: {brand_dna['字体风格']}")
    output.append(f"- **图标系统**: {brand_dna['PURE_GRAPHICS_CODE（纯图形代码）']}")
    output.append("")
    
    # 生成摘要
    summary = result["summary"]
    output.append("## 📊 生成摘要")
    output.append(f"- **总Prompt数**: {summary['total_prompts']}")
    output.append(f"- **Listing主图**: {summary['listing_images']}张")
    output.append(f"- **A+品牌图**: {summary['aplus_images']}张")
    output.append("")
    
    # Prompt列表
    output.append("## 📝 生成的Prompt")
    for i, prompt in enumerate(result["prompts"][:3], 1):  # 显示前3个
        output.append(f"### {i}. {prompt['selling_point']} ({prompt['category'].split('(')[0].strip()})")
        output.append(f"**布局**: {prompt['layout_model']}")
        output.append(f"**适配平台**: {', '.join(prompt.get('optimized_for', ['通用']))}")
        output.append(f"**Prompt预览**: `{prompt['prompt'][:100]}...`")
        output.append("")
    
    if len(result["prompts"]) > 3:
        output.append(f"*... 还有 {len(result['prompts'])-3} 个prompt*")
        output.append("")
    
    # 使用指南
    output.append("## 🚀 使用指南")
    if "usage_guide" in result:
        usage = result["usage_guide"]
        output.append("### 快速上手")
        output.append(f"1. {usage['step1']}")
        output.append(f"2. {usage['step2']}") 
        output.append(f"3. {usage['step3']}")
        output.append("")
        
        output.append("### 平台建议")
        for platform, tip in usage.get("platforms", {}).items():
            output.append(f"- **{platform}**: {tip}")
        output.append("")
    
    # 支持平台
    if "summary" in result and "supported_platforms" in result["summary"]:
        platforms = result["summary"]["supported_platforms"]
        output.append(f"## 🎨 支持平台")
        output.append(f"生成的prompt已针对以下平台优化: {', '.join(platforms)}")
    
    output.append("\n---")
    output.append("*🎨 Amazon Visual Architect v8.2 - 专业Prompt生成工具*")
    
    return "\n".join(output)

# OpenClaw技能主函数
def main():
    """主函数 - OpenClaw调用入口"""
    
    if len(sys.argv) < 2:
        print("❌ 缺少输入消息")
        print("用法: python run_architect.py \"用户消息\"")
        return
    
    user_message = " ".join(sys.argv[1:])
    
    # 检查是否是视觉架构师请求
    params = parse_architect_request(user_message)
    if not params:
        print("ℹ️ 这不是Amazon Visual Architect技能请求")
        return
    
    print("🎨 启动Amazon Visual Architect...")
    
    # 运行视觉架构师
    result = run_amazon_visual_architect(user_message)
    
    # 格式化输出
    formatted_output = format_output_for_chat(result)
    print(formatted_output)
    
    # 如果生成了完整结果，保存到JSON文件
    if result.get("success"):
        output_file = f"architect_result_{result['session_id']}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"\n💾 完整结果已保存到: {output_file}")

if __name__ == "__main__":
    main()