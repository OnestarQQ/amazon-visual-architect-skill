#!/usr/bin/env python3
"""
Amazon Visual Architect - 主要调用接口
集成prompt生成和图片生成的完整工作流
"""

import json
import os
import zipfile
from datetime import datetime
from typing import Dict, List, Optional
from .image_generator import BatchImageGenerator

class AmazonVisualArchitect:
    """亚马逊全案视觉架构师主类"""
    
    def __init__(self):
        self.version = "8.1"  # 升级版本号
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.results = []
    
    def parse_user_input(self, user_message: str) -> Dict:
        """解析用户输入，提取参数"""
        
        # 默认参数
        params = {
            "GenerateAPlus": True,
            "outputNum": 6,
            "ListingUserSelectedSize": "--ar 1:1",
            "UserSelectedSize": "--ar 1464:610",
            "language": "英语",
            "customer_keywords": [],
            "salesRegion": "美国", 
            "platform": "Amazon",
            "目标受众": "",
            "我的侵权词": [],
            # 新增图片生成参数
            "generate_images": False,
            "image_platform": "stability",
            "api_key": "",
            "image_size": "1024x1024",
            "quality": "high"
        }
        
        # 简单的参数提取逻辑 (实际实现中可以用更复杂的NLP解析)
        lines = user_message.split('\n')
        for line in lines:
            if '核心卖点:' in line or 'customer_keywords:' in line:
                keywords = line.split(':')[1].strip()
                params["customer_keywords"] = [k.strip() for k in keywords.split('、') if k.strip()]
            elif '销售区域:' in line or 'salesRegion:' in line:
                params["salesRegion"] = line.split(':')[1].strip()
            elif '目标受众:' in line:
                params["目标受众"] = line.split(':')[1].strip()
            elif '语言:' in line or 'language:' in line:
                params["language"] = line.split(':')[1].strip()
            elif '输出数量:' in line or 'outputNum:' in line:
                try:
                    params["outputNum"] = int(line.split(':')[1].strip())
                except:
                    pass
            elif 'generate_images:' in line:
                params["generate_images"] = 'true' in line.lower()
            elif 'image_platform:' in line:
                params["image_platform"] = line.split(':')[1].strip()
            elif 'api_key:' in line:
                params["api_key"] = line.split(':')[1].strip()
            elif 'image_size:' in line:
                params["image_size"] = line.split(':')[1].strip()
            elif 'quality:' in line:
                params["quality"] = line.split(':')[1].strip()
        
        return params
    
    def generate_brand_dna(self, params: Dict) -> Dict:
        """生成品牌基因报告"""
        
        # 简化的品牌基因生成逻辑
        # 实际中这里会有更复杂的AI分析
        
        brand_colors = {
            "科技产品": "#2196F3",
            "美容护肤": "#E8B4CB", 
            "户外运动": "#4CAF50",
            "家居生活": "#FF9800",
            "时尚配饰": "#9C27B0"
        }
        
        # 根据关键词推断产品类型
        keywords = " ".join(params.get("customer_keywords", []))
        if any(word in keywords for word in ["防水", "运动", "户外"]):
            product_type = "户外运动"
        elif any(word in keywords for word in ["蓝牙", "充电", "智能"]):
            product_type = "科技产品"
        elif any(word in keywords for word in ["护肤", "美容", "滋润"]):
            product_type = "美容护肤"
        else:
            product_type = "科技产品"  # 默认
        
        brand_dna = {
            "category": "Brand DNA Profile",
            "brandColor (品牌主色)": f"{product_type} {brand_colors[product_type]}",
            "背景策略-风格定义": "现代生活场景融合",
            "背景策略-场景关键词": f"{params['salesRegion']}本土化场景",
            "背景策略-光影": "自然光线，专业摄影",
            "Brand Injection（品牌植入）": f"基于{product_type}的品牌美学",
            "字体策略": "几何无衬线体",
            "字体风格": "Montserrat",
            "颜色策略-Heading": brand_colors[product_type].replace("#", "#1976"),
            "颜色策略-Body/Sub": "#424242",
            "灵活反白": "深色背景自动切换白色文字", 
            "排版": "非斜体，适中行距",
            "PURE_GRAPHICS_CODE（纯图形代码）": "实心圆图标系统",
            "形状": "圆形容器",
            "质感": "实心填充",
            "描边": "无描边"
        }
        
        return brand_dna
    
    def generate_prompts(self, params: Dict, brand_dna: Dict) -> List[Dict]:
        """生成prompt列表"""
        
        prompts = []
        keywords = params.get("customer_keywords", [])
        
        # 简化的prompt生成逻辑
        for i, keyword in enumerate(keywords[:params["outputNum"]]):
            
            # 判断是Listing还是A+
            if params["GenerateAPlus"] and i >= len(keywords) // 2:
                category = "🎬 A+ Image (品牌图 " + params["UserSelectedSize"] + ")"
                layout = f"A{(i % 4) + 1} - 品牌叙事布局"
            else:
                category = "📦 Listing Image (卖点图 " + params["ListingUserSelectedSize"] + ")"
                layout = f"L{(i % 3) + 1} - 功能展示布局"
            
            # 构建基础prompt
            base_prompt = f"""不允许文字中出现色值，例如"#688967"。ABSOLUTE LANGUAGE LOCK: ALL on-screen text must be in {params['language']}不能影响商品上的文字. 
Amazon e-commerce diagram, aspect ratio {params['ListingUserSelectedSize'] if 'Listing' in category else params['UserSelectedSize']}, Keep the product structure intact. 
{layout} layout showcasing {keyword}. 
Core color:{brand_dna['brandColor (品牌主色)'].split()[-1]}, modern commercial aesthetic. 
Typography: {brand_dna['字体风格']} font family. 
{brand_dna['PURE_GRAPHICS_CODE（纯图形代码）']}. 
Demographic: {params['目标受众']} in {params['salesRegion']}. 
Scene: Professional lifestyle photography showing {keyword} in real-world usage context."""
            
            prompt_data = {
                "id": i + 1,
                "category": category,
                "selling_point": keyword,
                "layout_model": layout,
                "visual_logic": "🔴 DISABLED (禁用变量三)",
                "language": params['language'],
                "salesRegion": params['salesRegion'],
                "目标受众": params['目标受众'],
                "prompt": base_prompt
            }
            
            prompts.append(prompt_data)
        
        return prompts
    
    async def generate_complete_solution(self, user_message: str) -> Dict:
        """生成完整解决方案 (prompt + 可选图片生成)"""
        
        print(f"🎨 Amazon Visual Architect v{self.version} 启动")
        print(f"📋 会话ID: {self.session_id}")
        
        # 1. 解析用户输入
        params = self.parse_user_input(user_message)
        print(f"✅ 参数解析完成: {len(params['customer_keywords'])}个卖点")
        
        # 2. 生成品牌基因
        brand_dna = self.generate_brand_dna(params)
        print(f"🎨 品牌基因提取完成: {brand_dna['brandColor (品牌主色)']}")
        
        # 3. 生成prompt列表
        prompts = self.generate_prompts(params, brand_dna)
        print(f"📝 生成 {len(prompts)} 个专业prompt")
        
        # 4. 准备结果
        results = {
            "session_id": self.session_id,
            "version": self.version,
            "timestamp": datetime.now().isoformat(),
            "brand_dna": brand_dna,
            "prompts": prompts,
            "parameters": params
        }
        
        # 5. 可选: 图片生成
        if params.get("generate_images") and params.get("api_key"):
            print(f"🖼️ 开始图片生成 (平台: {params['image_platform'].upper()})")
            
            try:
                batch_generator = BatchImageGenerator(
                    platform=params["image_platform"],
                    api_key=params["api_key"]
                )
                
                image_results = await batch_generator.generate_batch(
                    prompts=prompts,
                    size=params["image_size"],
                    quality=params["quality"],
                    max_concurrent=3
                )
                
                results["image_generation"] = image_results
                print(f"✅ 图片生成完成: {image_results['successful_images']}/{image_results['total_prompts']}")
                
                # 创建打包文件
                zip_path = self.create_result_package(results)
                results["download_package"] = zip_path
                print(f"📦 结果已打包: {zip_path}")
                
            except Exception as e:
                print(f"❌ 图片生成失败: {str(e)}")
                results["image_generation"] = {
                    "success": False,
                    "error": str(e)
                }
        
        self.results = results
        return results
    
    def create_result_package(self, results: Dict) -> str:
        """创建结果打包文件"""
        
        package_name = f"amazon_visual_architect_{self.session_id}.zip"
        
        with zipfile.ZipFile(package_name, 'w') as zipf:
            
            # 1. 保存prompt文件
            prompts_json = json.dumps(results["prompts"], ensure_ascii=False, indent=2)
            zipf.writestr("prompts.json", prompts_json)
            
            # 2. 保存品牌基因报告
            brand_dna_json = json.dumps(results["brand_dna"], ensure_ascii=False, indent=2)
            zipf.writestr("brand_dna.json", brand_dna_json)
            
            # 3. 保存参数配置
            params_json = json.dumps(results["parameters"], ensure_ascii=False, indent=2)
            zipf.writestr("parameters.json", params_json)
            
            # 4. 如果有生成的图片，添加到压缩包
            if "image_generation" in results and results["image_generation"].get("results"):
                for result in results["image_generation"]["results"]:
                    if isinstance(result, dict) and result.get("success") and result.get("local_path"):
                        if os.path.exists(result["local_path"]):
                            zipf.write(result["local_path"], f"images/{os.path.basename(result['local_path'])}")
            
            # 5. 创建README说明文件
            readme_content = self.create_readme(results)
            zipf.writestr("README.md", readme_content)
        
        return package_name
    
    def create_readme(self, results: Dict) -> str:
        """创建README说明文件"""
        
        readme = f"""# Amazon Visual Architect 生成结果

## 项目信息
- **生成时间**: {results['timestamp']}
- **会话ID**: {results['session_id']}
- **版本**: v{results['version']}

## 品牌基因
- **品牌主色**: {results['brand_dna']['brandColor (品牌主色)']}
- **字体风格**: {results['brand_dna']['字体风格']}
- **图标系统**: {results['brand_dna']['PURE_GRAPHICS_CODE（纯图形代码）']}

## 生成结果
- **Prompt总数**: {len(results['prompts'])}
- **Listing主图**: {len([p for p in results['prompts'] if 'Listing' in p['category']])}张
- **A+品牌图**: {len([p for p in results['prompts'] if 'A+' in p['category']])}张

"""
        
        if "image_generation" in results:
            img_gen = results["image_generation"]
            readme += f"""## 图片生成
- **生成平台**: {img_gen.get('platform', 'unknown').upper()}
- **成功率**: {img_gen.get('success_rate', 0):.1f}%
- **总费用**: ${img_gen.get('total_cost', 0):.3f}
- **成功数量**: {img_gen.get('successful_images', 0)}/{img_gen.get('total_prompts', 0)}

"""
        
        readme += """## 文件说明
- `prompts.json` - 所有生成的prompt数据
- `brand_dna.json` - 品牌基因报告
- `parameters.json` - 生成参数配置
- `images/` - 生成的图片文件 (如有)

## 使用方式
1. 查看`brand_dna.json`了解品牌视觉基因
2. 使用`prompts.json`中的prompt进行AI绘图
3. 或直接使用`images/`中的生成图片

---
*Generated by Amazon Visual Architect v""" + self.version + "*"
        
        return readme

# 主要调用函数
async def run_visual_architect(user_message: str) -> Dict:
    """主要调用函数"""
    architect = AmazonVisualArchitect()
    return await architect.generate_complete_solution(user_message)

# 使用示例
async def example_complete_workflow():
    """完整工作流示例"""
    
    user_input = """
    请使用亚马逊全案视觉架构师技能分析以下产品：

    **产品信息**:
    - 核心卖点: 防水功能、长续航、舒适佩戴、快速配对
    - 销售区域: 美国
    - 目标受众: 25-35岁通勤族
    - 发布平台: Amazon
    - 输出数量: 6
    - 语言: 英语

    **生图设置**:
    - generate_images: true
    - image_platform: stability
    - api_key: sk-xxxxxxxxxxxxxxx
    - image_size: 1024x1024
    - quality: high
    """
    
    results = await run_visual_architect(user_input)
    
    print("="*50)
    print("🎉 生成完成!")
    print(f"📁 下载包: {results.get('download_package', '仅prompt模式')}")
    print("="*50)
    
    return results

if __name__ == "__main__":
    import asyncio
    # asyncio.run(example_complete_workflow())
    print("Amazon Visual Architect - Main Interface Ready!")
    print("Usage: from visual_architect import run_visual_architect")