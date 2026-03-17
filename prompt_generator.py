#!/usr/bin/env python3
"""
Amazon Visual Architect v8.3 - 智能Prompt生成器  
集成商品图片分析，自动生成卖点，专业prompt一键生成
"""

import json
import sys
import os
import base64
from datetime import datetime
from typing import Dict, List, Optional

# 导入商品分析器
try:
    from product_analyzer import analyze_product_from_image
    PRODUCT_ANALYZER_AVAILABLE = True
except ImportError:
    PRODUCT_ANALYZER_AVAILABLE = False

class AmazonVisualArchitectPrompts:
    """亚马逊全案视觉架构师 - 智能Prompt生成器"""
    
    def __init__(self):
        self.version = "8.3"
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.product_analysis_result = None
        
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
            "我的侵权词": []
        }
        
        # 简单的参数提取逻辑
        lines = user_message.split('\n')
        for line in lines:
            if '核心卖点:' in line or 'customer_keywords:' in line:
                keywords = line.split(':')[1].strip()
                params["customer_keywords"] = [k.strip() for k in keywords.replace('、', ',').split(',') if k.strip()]
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
            elif 'GenerateAPlus:' in line:
                params["GenerateAPlus"] = 'true' in line.lower()
            elif any(keyword in line.lower() for keyword in ['商品图片:', 'product_image:', '图片分析:', 'analyze_image:']):
                params["has_product_image"] = True
                # 提取图片路径或base64数据
                content = line.split(':')[-1].strip()
                if content and content != '[上传图片或描述]':
                    params["image_input"] = content
            elif 'api_key:' in line.lower() or 'vision_api:' in line.lower():
                params["vision_api_key"] = line.split(':')[-1].strip()
        
        return params
        
    def analyze_product_image(self, params: Dict) -> Dict:
        """分析商品图片，提取产品信息和卖点"""
        
        if not PRODUCT_ANALYZER_AVAILABLE:
            return {
                "success": False,
                "error": "商品分析器未安装",
                "suggestion": "使用模拟模式或手动输入卖点"
            }
        
        # 获取图片和API配置
        image_input = params.get("image_input", "")
        api_key = params.get("vision_api_key", "")
        
        # 确定使用的模型
        if api_key.startswith("sk-"):
            model = "gpt-4-vision-preview"
        elif api_key.startswith("sk-ant-"):
            model = "claude-3-sonnet"
        else:
            model = "mock"  # 使用模拟模式
        
        # 分析商品
        if os.path.exists(image_input):
            # 本地文件路径
            result = analyze_product_from_image(image_path=image_input, api_key=api_key, model=model)
        elif image_input.startswith("data:image"):
            # base64图片数据
            base64_data = image_input.split(',')[1] if ',' in image_input else image_input
            result = analyze_product_from_image(image_base64=base64_data, api_key=api_key, model=model)
        else:
            # 模拟模式
            result = analyze_product_from_image(model="mock")
        
        return result
    
    def generate_brand_dna(self, params: Dict) -> Dict:
        """生成品牌基因报告"""
        
        # 品牌色彩映射
        brand_colors = {
            "科技产品": "#2196F3",
            "美容护肤": "#E8B4CB", 
            "户外运动": "#4CAF50",
            "家居生活": "#FF9800",
            "时尚配饰": "#9C27B0",
            "健康食品": "#4CAF50",
            "儿童用品": "#FF5722"
        }
        
        # 根据关键词推断产品类型
        keywords = " ".join(params.get("customer_keywords", []))
        keywords_lower = keywords.lower()
        
        if any(word in keywords_lower for word in ["防水", "运动", "户外", "登山", "健身"]):
            product_type = "户外运动"
        elif any(word in keywords_lower for word in ["蓝牙", "充电", "智能", "无线", "数字", "科技"]):
            product_type = "科技产品"
        elif any(word in keywords_lower for word in ["护肤", "美容", "滋润", "美白", "抗衰", "化妆"]):
            product_type = "美容护肤"
        elif any(word in keywords_lower for word in ["家居", "厨房", "卫浴", "装饰", "清洁"]):
            product_type = "家居生活"
        elif any(word in keywords_lower for word in ["时尚", "饰品", "包包", "手表", "首饰"]):
            product_type = "时尚配饰"
        elif any(word in keywords_lower for word in ["食品", "营养", "保健", "维生素", "健康"]):
            product_type = "健康食品"
        elif any(word in keywords_lower for word in ["儿童", "宝宝", "婴儿", "玩具", "学习"]):
            product_type = "儿童用品"
        else:
            product_type = "科技产品"  # 默认
        
        # 字体风格映射
        font_styles = {
            "科技产品": "几何无衬线体",
            "美容护肤": "经典优雅衬线体",
            "户外运动": "硬朗无衬线体", 
            "家居生活": "圆润童趣字体",
            "时尚配饰": "俏皮手写风格",
            "健康食品": "几何无衬线体",
            "儿童用品": "圆润童趣字体"
        }
        
        brand_dna = {
            "category": "Brand DNA Profile",
            "brandColor (品牌主色)": f"{product_type} {brand_colors[product_type]}",
            "背景策略-风格定义": f"{params['salesRegion']}本土化现代生活场景",
            "背景策略-场景关键词": f"{product_type}相关的真实使用场景",
            "背景策略-光影": "自然光线，专业摄影级别",
            "Brand Injection（品牌植入）": f"基于{product_type}的品牌美学体系",
            "字体策略": font_styles[product_type],
            "字体风格": self._get_specific_font(font_styles[product_type]),
            "颜色策略-Heading": self._adjust_color(brand_colors[product_type], darker=True),
            "颜色策略-Body/Sub": "#424242",
            "灵活反白": "深色背景自动切换白色文字", 
            "排版": "非斜体，适中行距，现代简约",
            "PURE_GRAPHICS_CODE（纯图形代码）": "实心圆图标系统",
            "形状": "圆形容器",
            "质感": "实心填充",
            "描边": "无描边"
        }
        
        return brand_dna
    
    def _get_specific_font(self, font_category: str) -> str:
        """获取具体字体名称"""
        font_map = {
            "几何无衬线体": "Montserrat",
            "硬朗无衬线体": "Bebas Neue",
            "经典优雅衬线体": "Playfair Display",
            "圆润童趣字体": "Nunito",
            "俏皮手写风格": "Pacifico"
        }
        return font_map.get(font_category, "Montserrat")
    
    def _adjust_color(self, hex_color: str, darker: bool = False) -> str:
        """调整颜色深浅"""
        # 简化的颜色调整
        if darker:
            return hex_color.replace("96F3", "76D2").replace("B4CB", "94AB").replace("AF50", "8F30")
        return hex_color
    
    def generate_prompts(self, params: Dict, brand_dna: Dict) -> List[Dict]:
        """生成专业prompt列表"""
        
        prompts = []
        keywords = params.get("customer_keywords", [])
        total_prompts = params["outputNum"]
        
        # 如果输出数量大于卖点数量，启用裂变模式
        if total_prompts > len(keywords):
            keywords = self._expand_keywords(keywords, total_prompts)
        
        # 按比例分配Listing和A+
        listing_count = total_prompts // 2 if params["GenerateAPlus"] else total_prompts
        aplus_count = total_prompts - listing_count if params["GenerateAPlus"] else 0
        
        # 生成Listing prompts
        for i in range(listing_count):
            keyword = keywords[i % len(keywords)]
            layout_num = (i % 7) + 1
            
            prompt_data = self._create_listing_prompt(
                i + 1, keyword, f"L{layout_num}", params, brand_dna
            )
            prompts.append(prompt_data)
        
        # 生成A+ prompts
        for i in range(aplus_count):
            keyword = keywords[i % len(keywords)]
            layout_num = (i % 9) + 1
            
            prompt_data = self._create_aplus_prompt(
                listing_count + i + 1, keyword, f"A{layout_num}", params, brand_dna
            )
            prompts.append(prompt_data)
        
        return prompts
    
    def _expand_keywords(self, keywords: List[str], target_count: int) -> List[str]:
        """裂变模式：扩展关键词"""
        expanded = keywords.copy()
        
        # 扩展策略
        extensions = {
            "防水": ["IPX7防水", "生活防水", "雨天防护"],
            "轻便": ["便携设计", "轻量化", "易携带"],
            "大容量": ["超大容量", "海量存储", "容量升级"],
            "快速充电": ["闪充技术", "快充协议", "充电速度"],
            "降噪": ["主动降噪", "环境降噪", "通话降噪"],
            "续航": ["超长续航", "持久电力", "电池寿命"],
            "舒适": ["人体工学", "佩戴舒适", "长时间舒适"],
            "智能": ["AI智能", "智能识别", "智能控制"]
        }
        
        while len(expanded) < target_count:
            for keyword in keywords:
                if keyword in extensions:
                    for ext in extensions[keyword]:
                        if ext not in expanded:
                            expanded.append(ext)
                            if len(expanded) >= target_count:
                                break
                    if len(expanded) >= target_count:
                        break
                else:
                    # 通用扩展
                    expanded.append(f"{keyword}特写")
                    if len(expanded) >= target_count:
                        break
            if len(expanded) == len(keywords):  # 防止无限循环
                break
        
        return expanded[:target_count]
    
    def _create_listing_prompt(self, id: int, keyword: str, layout: str, params: Dict, brand_dna: Dict) -> Dict:
        """创建Listing类型的prompt"""
        
        # 布局描述映射
        layout_descriptions = {
            "L1": "文本叠加面板布局，产品主体占70%，侧边品牌色信息面板",
            "L2": "卖点特征块布局，使用场景图配多个功能模块展示",
            "L3": "极简主义布局，大面积场景配醒目主标题", 
            "L4": "元素衍生物形态布局，色块形状源于产品功能特性",
            "L5": "圆形细节特写布局，主体配2-3个圆形特写细节",
            "L6": "结构分层解析布局，3D分解展示内部结构层次",
            "L7": "使用场景搭配布局，Flat Lay俯拍风格"
        }
        
        # 构建专业prompt
        base_prompt = f"""Professional Amazon e-commerce product photography, aspect ratio {params['ListingUserSelectedSize']}, commercial photography style. 

LAYOUT: {layout_descriptions.get(layout, '专业布局')} showcasing {keyword}.

BRAND SYSTEM: Core color {brand_dna['brandColor (品牌主色)'].split()[-1]}, {brand_dna['字体风格']} typography, {brand_dna['PURE_GRAPHICS_CODE（纯图形代码）']}.

SCENE: {params['目标受众']} in {params['salesRegion']} lifestyle context, demonstrating {keyword} in realistic usage environment, professional lighting, clean composition.

VISUAL STYLE: Modern commercial aesthetic, high-end product photography, marketing-ready image, {params['platform']} compliant.

TEXT LANGUAGE: All text elements in {params['language']}.

TECHNICAL: High resolution, sharp details, professional color grading, studio lighting quality."""
        
        return {
            "id": id,
            "category": f"📦 Listing Image (卖点图 {params['ListingUserSelectedSize']})",
            "selling_point": keyword,
            "layout_model": f"{layout} - {layout_descriptions.get(layout, '专业布局')}",
            "visual_logic": "✅ ACTIVE (启用品牌基因)",
            "language": params['language'],
            "salesRegion": params['salesRegion'],
            "目标受众": params['目标受众'],
            "prompt": base_prompt.strip(),
            "optimized_for": ["Midjourney", "Stability AI", "DALL-E 3", "Leonardo AI"]
        }
    
    def _create_aplus_prompt(self, id: int, keyword: str, layout: str, params: Dict, brand_dna: Dict) -> Dict:
        """创建A+类型的prompt"""
        
        # A+布局描述映射
        layout_descriptions = {
            "A1": "主图+悬浮式图文详解，沉浸场景配半透明信息面板",
            "A2": "对角线叙事切片，斜线分割多功能展示",
            "A3": "序列化卡片阵列，标准化信息矩阵展示",
            "A4": "极简摄影自然景深留白，杂志级构图",
            "A5": "结构化拼图Bento布局，非对称三格分割", 
            "A6": "线性流程进化图，电影式广角构图",
            "A7": "核心辐射式全景分析，产品中心四周信息块",
            "A8": "沉浸式性能感知全景，电影级景深效果",
            "A9": "场景分解图多视窗特写，双场景对比展示"
        }
        
        # 构建A+专业prompt
        base_prompt = f"""Amazon A+ content image, aspect ratio {params['UserSelectedSize']}, premium brand storytelling visual.

LAYOUT: {layout_descriptions.get(layout, '品牌叙事布局')} focusing on {keyword} brand narrative.

BRAND SYSTEM: Core color {brand_dna['brandColor (品牌主色)'].split()[-1]}, {brand_dna['字体风格']} typography, sophisticated brand aesthetic.

STORYTELLING: Emotional connection with {params['目标受众']}, {keyword} as lifestyle enhancement, aspirational yet accessible.

SCENE: Premium {params['salesRegion']} lifestyle environment, cinematic composition, brand values visualization.

VISUAL STYLE: High-end commercial photography, magazine quality, brand premium positioning, marketing excellence.

TEXT LANGUAGE: All text elements in {params['language']}.

TECHNICAL: Ultra-high resolution, professional color grading, cinematic lighting, brand-grade visual standards."""
        
        return {
            "id": id,
            "category": f"🎬 A+ Image (品牌图 {params['UserSelectedSize']})",
            "selling_point": keyword,
            "layout_model": f"{layout} - {layout_descriptions.get(layout, '品牌叙事布局')}",
            "visual_logic": "🔴 DISABLED (留白美学)",
            "language": params['language'],
            "salesRegion": params['salesRegion'],
            "目标受众": params['目标受众'],
            "prompt": base_prompt.strip(),
            "optimized_for": ["Midjourney", "Stability AI", "DALL-E 3", "Adobe Firefly"]
        }
    
    def generate_complete_solution(self, user_message: str) -> Dict:
        """生成完整的prompt解决方案（包含可选的商品图片分析）"""
        
        print(f"🎨 Amazon Visual Architect v{self.version} - 智能Prompt生成器")
        print(f"📋 会话ID: {self.session_id}")
        
        # 1. 解析用户输入
        params = self.parse_user_input(user_message)
        
        # 2. 可选：分析商品图片
        product_analysis = None
        if params.get("has_product_image") or params.get("image_input"):
            print("🔍 检测到商品图片，开始智能分析...")
            analysis_result = self.analyze_product_image(params)
            
            if analysis_result.get("success"):
                product_analysis = analysis_result
                self.product_analysis_result = product_analysis
                
                # 使用分析结果更新参数
                recommended_params = analysis_result["recommended_params"]
                
                # 如果用户没有手动输入卖点，使用自动提取的卖点
                if not params["customer_keywords"]:
                    params["customer_keywords"] = recommended_params["customer_keywords"]
                    print(f"🤖 自动提取卖点: {', '.join(params['customer_keywords'])}")
                
                # 自动推荐参数（如果用户未指定）
                if not params.get("目标受众"):
                    params["目标受众"] = recommended_params["目标受众"]
                if params["salesRegion"] == "美国":  # 默认值
                    params["salesRegion"] = recommended_params["salesRegion"]
                if params["language"] == "英语":  # 默认值
                    params["language"] = recommended_params["language"]
                
                print(f"✅ 商品分析完成 ({analysis_result.get('model_used', 'unknown')})")
                print(f"📝 产品: {analysis_result['product_analysis']['product_name']}")
                print(f"🎯 受众: {params['目标受众']}")
            else:
                print(f"⚠️ 商品分析失败: {analysis_result.get('error', '未知错误')}")
                print("🔄 将使用用户输入的卖点继续...")
        
        print(f"✅ 参数准备完成: {len(params['customer_keywords'])}个卖点")
        
        # 3. 生成品牌基因
        brand_dna = self.generate_brand_dna(params)
        print(f"🎨 品牌基因提取: {brand_dna['brandColor (品牌主色)']}")
        
        # 4. 生成prompt列表
        prompts = self.generate_prompts(params, brand_dna)
        print(f"📝 生成 {len(prompts)} 个专业prompt")
        
        # 5. 准备结果
        results = {
            "session_id": self.session_id,
            "version": self.version,
            "timestamp": datetime.now().isoformat(),
            "product_analysis": product_analysis,  # 新增：商品分析结果
            "brand_dna": brand_dna,
            "prompts": prompts,
            "parameters": params,
            "summary": {
                "total_prompts": len(prompts),
                "listing_prompts": len([p for p in prompts if "Listing" in p["category"]]),
                "aplus_prompts": len([p for p in prompts if "A+" in p["category"]]),
                "brand_color": brand_dna["brandColor (品牌主色)"],
                "supported_platforms": ["Midjourney", "Stability AI", "DALL-E 3", "Leonardo AI", "Adobe Firefly"]
            },
            "usage_guide": {
                "step1": "复制所需的prompt到你喜欢的AI绘图平台",
                "step2": "根据平台特点微调参数（如宽高比、风格权重）",
                "step3": "生成图片并根据需要进行后期调整",
                "platforms": {
                    "Midjourney": "直接粘贴prompt，添加 --ar 参数调整比例",
                    "Stability AI": "适合商业用途，注意版权友好",
                    "DALL-E 3": "文字理解强，复杂描述效果好",
                    "Leonardo AI": "界面友好，风格选择丰富",
                    "Adobe Firefly": "商业安全，无版权风险"
                }
            }
        }
        
        # 保存结果到JSON文件
        output_file = f"prompts_{self.session_id}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print(f"💾 完整结果已保存: {output_file}")
        if product_analysis:
            print("🔍 包含商品智能分析结果")
        print("🚀 prompt已生成完成，可复制到任何AI绘图平台使用！")
        
        return results

# 主要调用函数
def generate_amazon_prompts(user_message: str) -> Dict:
    """主要调用函数"""
    generator = AmazonVisualArchitectPrompts()
    return generator.generate_complete_solution(user_message)

# 使用示例
def example_usage():
    """使用示例"""
    
    # 示例1：传统模式（手动输入卖点）
    user_input_manual = """
    请使用亚马逊全案视觉架构师技能分析以下产品：

    **产品信息**:
    - 核心卖点: 防水功能、长续航、舒适佩戴、快速配对
    - 销售区域: 美国
    - 目标受众: 25-35岁通勤族
    - 发布平台: Amazon
    - 输出数量: 6
    - 语言: 英语
    """
    
    # 示例2：智能模式（图片分析）
    user_input_smart = """
    请使用亚马逊全案视觉架构师技能智能分析商品：

    **智能分析**:
    - 商品图片: product.jpg
    - vision_api_key: sk-xxxxxxxx (可选，不提供则使用模拟分析)
    - 输出数量: 8
    - 语言: 英语
    """
    
    print("📝 示例1: 传统手动模式")
    print("=" * 40)
    results1 = generate_amazon_prompts(user_input_manual)
    
    print("\n🤖 示例2: 智能分析模式")  
    print("=" * 40)
    results2 = generate_amazon_prompts(user_input_smart)
    
    print("\n" + "="*50)
    print("🎉 Prompt生成完成!")
    print(f"📁 结果文件: prompts_{results['session_id']}.json")
    print(f"📊 品牌主色: {results['summary']['brand_color']}")
    print(f"📝 总prompt数: {results['summary']['total_prompts']}")
    print("🚀 现在可以复制prompt到AI绘图平台使用了!")
    print("="*50)
    
    return results

if __name__ == "__main__":
    if len(sys.argv) > 1:
        user_message = " ".join(sys.argv[1:])
        generate_amazon_prompts(user_message)
    else:
        print("Amazon Visual Architect v8.2 - 专业Prompt生成器")
        print("用法: python prompt_generator.py \"用户消息\"")
        print("或直接调用: from prompt_generator import generate_amazon_prompts")