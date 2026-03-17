#!/usr/bin/env python3
"""
Amazon Visual Architect - 商品智能分析器
基于商品图片自动分析生成核心卖点，降低用户输入门槛
"""

import json
import sys
import base64
import requests
from typing import Dict, List, Optional
from datetime import datetime

class ProductAnalyzer:
    """商品智能分析器 - 通过图片识别商品特征和卖点"""
    
    def __init__(self):
        self.version = "1.0"
        self.analysis_prompt = """
# Role: 跨境电商全栈产品经理 (Amazon Full-Stack Product Manager)
## Profile
- Author: OneStar x Linkfox AI
- Version: 5.1
- Language: 中文 (Chinese)
- Description: 你是资深产品体验设计师，能通过观察商品图精准推导出交互逻辑、操作方式及核心卖点，用于撰写亚马逊 Listing。

## Skills
- **视觉解码**: 识别材质、风格、颜色
- **交互推理**: 通过按钮、把手、接口、形态，反推用户如何操作
- **卖点提炼**: 将视觉特征转化为商业卖点 (Feature to Benefit)

## Constraints
1. **深度推理**: 使用方法必须具体，如"长按侧面圆形按钮3秒"，不能只写"打开开关"
2. **语言规范**: 关键词用英文（SEO），描述用中文

## Output Rules (严格遵守)
1. **只输出 JSON**，不要有任何前言、解释或后缀文字
2. **不要使用 markdown 代码块**，直接输出纯 JSON
3. **必须完全匹配下方的 JSON Schema 结构**
4. **所有字段都必须填写**，不能省略任何字段

## JSON Schema (必须严格遵循此结构)
{
  "product_name": "string - 产品纯中文名称",
  "target_audience": "string - 具体适用场景 (when & where)",
  "selling_points_description": "string - 结合视觉细节证明的核心卖点",
  "craftsmanship_details": "string - 材质推测、颜色描述、形态特征",
  "usage_method": "string - 详细操作步骤，必须具体到按钮位置和操作动作",
  "category_path": "string - Amazon类目路径 (Level 1 > Level 2 > Level 3)"
}

## Example Output (输出示例)
{
  "product_name": "便携式LED野营灯笼",
  "target_audience": "户外露营爱好者，适用于夜间帐篷照明、停电应急、庭院烧烤等场景",
  "selling_points_description": "采用可折叠设计，收纳后仅手掌大小；底部磁吸设计可吸附于金属表面；IPX4防水等级适合户外使用",
  "craftsmanship_details": "ABS工程塑料外壳，磨砂质感，军绿色配色；顶部配有不锈钢挂钩；灯罩为乳白色PC材质，光线柔和不刺眼",
  "usage_method": "1. 向上拉伸灯体展开灯罩即可开灯；2. 按压顶部圆形按钮切换亮度（高/中/低/SOS四档）；3. 向下压缩灯体即可关闭；4. 使用底部Micro-USB接口充电，红灯亮起表示充电中，绿灯表示充满",
  "category_path": "Sports & Outdoors > Outdoor Recreation > Camping & Hiking > Lanterns"
}

现在请仔细观察这张商品图片，按照以上要求分析产品特征并输出JSON格式的结果。
"""
    
    def analyze_product_image(self, image_data: str, api_key: str = "", model: str = "gpt-4-vision-preview") -> Dict:
        """分析商品图片，提取产品信息和卖点"""
        
        try:
            # 构建API请求
            if model.startswith("gpt-"):
                # OpenAI Vision API
                return self._analyze_with_openai(image_data, api_key)
            elif "claude" in model.lower():
                # Anthropic Claude Vision
                return self._analyze_with_claude(image_data, api_key)
            else:
                # 默认使用模拟分析
                return self._mock_analysis()
                
        except Exception as e:
            return {
                "success": False,
                "error": f"商品分析失败: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
    
    def _analyze_with_openai(self, image_data: str, api_key: str) -> Dict:
        """使用OpenAI GPT-4V分析商品图片"""
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        payload = {
            "model": "gpt-4-vision-preview",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": self.analysis_prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_data}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 1000
        }
        
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            
            # 解析JSON响应
            try:
                product_info = json.loads(content)
                return {
                    "success": True,
                    "product_info": product_info,
                    "model": "gpt-4-vision",
                    "timestamp": datetime.now().isoformat()
                }
            except json.JSONDecodeError:
                return {
                    "success": False,
                    "error": f"JSON解析失败: {content}",
                    "raw_response": content
                }
        else:
            return {
                "success": False,
                "error": f"API调用失败: {response.status_code} - {response.text}"
            }
    
    def _analyze_with_claude(self, image_data: str, api_key: str) -> Dict:
        """使用Anthropic Claude Vision分析商品图片"""
        
        headers = {
            "Content-Type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01"
        }
        
        payload = {
            "model": "claude-3-sonnet-20240229",
            "max_tokens": 1000,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": self.analysis_prompt
                        },
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/jpeg",
                                "data": image_data
                            }
                        }
                    ]
                }
            ]
        }
        
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result["content"][0]["text"]
            
            try:
                product_info = json.loads(content)
                return {
                    "success": True,
                    "product_info": product_info,
                    "model": "claude-3-sonnet",
                    "timestamp": datetime.now().isoformat()
                }
            except json.JSONDecodeError:
                return {
                    "success": False,
                    "error": f"JSON解析失败: {content}",
                    "raw_response": content
                }
        else:
            return {
                "success": False,
                "error": f"API调用失败: {response.status_code} - {response.text}"
            }
    
    def _mock_analysis(self) -> Dict:
        """模拟商品分析结果（用于测试）"""
        
        mock_product = {
            "product_name": "智能蓝牙降噪耳机",
            "target_audience": "商务人士和通勤族，适用于办公室、地铁、飞机等嘈杂环境中的高质量音频体验",
            "selling_points_description": "主动降噪技术有效阻隔环境噪音；40小时超长续航满足长途旅行需求；快充15分钟获得5小时播放时间；触控操作简单便捷",
            "craftsmanship_details": "高级磨砂质感塑料外壳，深空灰配色显得专业低调；头梁采用软质PU皮革包裹，佩戴舒适；耳罩使用记忆海绵，贴合度好",
            "usage_method": "1. 长按右耳罩下方电源键3秒开机；2. 双击电源键进入蓝牙配对模式；3. 轻触左耳罩可暂停/播放音乐；4. 上下滑动右耳罩调节音量；5. 按压降噪键切换降噪模式",
            "category_path": "Electronics > Audio > Headphones > Over-Ear Headphones"
        }
        
        return {
            "success": True,
            "product_info": mock_product,
            "model": "mock-analysis",
            "timestamp": datetime.now().isoformat(),
            "note": "这是模拟分析结果，请上传真实图片并提供API密钥获得准确分析"
        }
    
    def extract_selling_points(self, product_info: Dict) -> List[str]:
        """从商品分析结果中提取核心卖点列表"""
        
        selling_points = []
        
        if "selling_points_description" in product_info:
            # 按分号或句号分割卖点
            descriptions = product_info["selling_points_description"].replace('；', ';').replace('。', ';')
            points = [point.strip() for point in descriptions.split(';') if point.strip()]
            
            # 提取关键词作为卖点
            for point in points:
                if '降噪' in point:
                    selling_points.append('降噪功能')
                elif '续航' in point or '电池' in point:
                    selling_points.append('长续航')
                elif '快充' in point:
                    selling_points.append('快速充电')
                elif '防水' in point:
                    selling_points.append('防水功能')
                elif '便携' in point or '轻便' in point:
                    selling_points.append('便携设计')
                elif '舒适' in point:
                    selling_points.append('舒适佩戴')
                elif '智能' in point:
                    selling_points.append('智能控制')
                elif '高清' in point or '音质' in point:
                    selling_points.append('高音质')
                else:
                    # 提取前几个关键词作为卖点
                    key_words = point[:10].replace('采用', '').replace('具备', '')
                    if key_words:
                        selling_points.append(key_words)
        
        # 如果没有提取到卖点，使用产品名称推断
        if not selling_points and "product_name" in product_info:
            name = product_info["product_name"]
            if '蓝牙' in name:
                selling_points.append('无线连接')
            if '智能' in name:
                selling_points.append('智能功能')
            if '便携' in name:
                selling_points.append('便携设计')
        
        # 确保至少有3个卖点
        if len(selling_points) < 3:
            selling_points.extend(['优质材料', '人性化设计', '多功能应用'][:3-len(selling_points)])
        
        return selling_points[:6]  # 最多6个卖点
    
    def infer_target_region_and_audience(self, product_info: Dict) -> Dict:
        """从商品信息推断销售区域和目标受众"""
        
        # 默认值
        region = "美国"
        audience = "普通消费者"
        
        if "target_audience" in product_info:
            audience_text = product_info["target_audience"]
            
            # 推断目标受众
            if "商务" in audience_text:
                audience = "25-45岁商务人士"
            elif "户外" in audience_text:
                audience = "户外运动爱好者"
            elif "学生" in audience_text:
                audience = "18-25岁学生群体"
            elif "家庭" in audience_text:
                audience = "家庭用户"
            elif "专业" in audience_text:
                audience = "专业用户"
            else:
                audience = "25-40岁都市人群"
        
        if "category_path" in product_info:
            category = product_info["category_path"]
            
            # 根据类目推断主要销售区域
            if "Sports" in category or "Outdoor" in category:
                region = "美国"  # 户外用品美国市场大
            elif "Beauty" in category or "Fashion" in category:
                region = "欧洲"  # 时尚美妆欧洲市场成熟
            elif "Electronics" in category:
                region = "美国"  # 电子产品美国创新市场
            elif "Home" in category:
                region = "美国"  # 家居用品美国消费力强
        
        return {
            "salesRegion": region,
            "目标受众": audience
        }

# 集成函数
def analyze_product_from_image(image_path: str = "", image_base64: str = "", 
                             api_key: str = "", model: str = "mock") -> Dict:
    """分析商品图片的主函数"""
    
    analyzer = ProductAnalyzer()
    
    # 处理图片输入
    if image_path:
        try:
            with open(image_path, 'rb') as f:
                image_data = base64.b64encode(f.read()).decode()
        except Exception as e:
            return {"success": False, "error": f"图片读取失败: {str(e)}"}
    elif image_base64:
        image_data = image_base64
    else:
        # 使用模拟分析
        return analyzer._mock_analysis()
    
    # 分析商品
    analysis_result = analyzer.analyze_product_image(image_data, api_key, model)
    
    if analysis_result.get("success"):
        product_info = analysis_result["product_info"]
        
        # 提取卖点
        selling_points = analyzer.extract_selling_points(product_info)
        
        # 推断区域和受众
        region_audience = analyzer.infer_target_region_and_audience(product_info)
        
        # 整合结果
        result = {
            "success": True,
            "product_analysis": product_info,
            "extracted_selling_points": selling_points,
            "recommended_params": {
                "customer_keywords": selling_points,
                "salesRegion": region_audience["salesRegion"],
                "目标受众": region_audience["目标受众"],
                "platform": "Amazon",
                "language": "英语" if region_audience["salesRegion"] in ["美国", "英国"] else "中文"
            },
            "model_used": analysis_result.get("model", "unknown"),
            "timestamp": analysis_result.get("timestamp")
        }
        
        return result
    
    else:
        return analysis_result

# 使用示例
def example_usage():
    """使用示例"""
    
    print("🔍 商品智能分析器测试")
    print("=" * 40)
    
    # 模拟分析
    result = analyze_product_from_image(model="mock")
    
    if result["success"]:
        print("✅ 分析成功!")
        print(f"📝 产品名称: {result['product_analysis']['product_name']}")
        print(f"🎯 目标受众: {result['product_analysis']['target_audience']}")
        print(f"💡 提取卖点: {', '.join(result['extracted_selling_points'])}")
        print(f"🌍 推荐区域: {result['recommended_params']['salesRegion']}")
        print(f"👥 受众群体: {result['recommended_params']['目标受众']}")
    else:
        print(f"❌ 分析失败: {result['error']}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # 命令行使用
        image_path = sys.argv[1]
        api_key = sys.argv[2] if len(sys.argv) > 2 else ""
        model = sys.argv[3] if len(sys.argv) > 3 else "mock"
        
        result = analyze_product_from_image(image_path, "", api_key, model)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        # 示例模式
        example_usage()