# Amazon Image Skill v1.0 - 使用示例

## 🤖 智能模式示例

### 示例1：完全自动化（推荐）
```
请使用亚马逊商品套图技能智能分析商品：

**智能分析**:
- 商品图片: bluetooth_headphones.jpg
- vision_api_key: sk-xxxxxxxxxxxxxx
- 输出数量: 8
- 语言: 英语
```

**AI自动完成**:
✅ 识别产品：智能蓝牙降噪耳机  
✅ 提取卖点：降噪功能、长续航、舒适佩戴、快速配对  
✅ 推断受众：25-35岁商务通勤族  
✅ 建议区域：美国市场  
✅ 生成8个专业prompt

### 示例2：模拟模式（无API密钥）
```
请使用亚马逊商品套图技能分析商品图片：

**产品信息**:
- 商品图片: camping_lantern.jpg  
- 输出数量: 6
- 语言: 中文
```

**AI处理**:
✅ 使用模拟分析（基于产品类型推断）  
✅ 生成示例卖点和受众定位  
✅ 输出6个中文prompt

### 示例3：混合模式
```
请使用亚马逊商品套图技能分析以下产品：

**智能分析**:
- 商品图片: smartwatch.jpg
- vision_api_key: sk-ant-xxxxxxxx (Claude)

**手动补充**:
- 目标受众: 健身爱好者和科技达人
- 销售区域: 欧洲
- 输出数量: 10
```

**AI处理**:
✅ Claude Vision分析产品特征  
✅ 自动提取智能手表卖点  
✅ 结合用户指定的受众和区域  
✅ 生成欧洲市场定位的10个prompt

## 📝 传统模式示例

### 示例4：完全手动输入
```
请使用亚马逊商品套图技能分析以下产品：

**产品信息**:
- 核心卖点: 防水功能、轻便设计、大容量存储、快速充电
- 销售区域: 美国
- 目标受众: 25-40岁户外运动爱好者  
- 发布平台: Amazon
- 输出数量: 8
- 语言: 英语

**设置**:
- GenerateAPlus: true
- ListingUserSelectedSize: --ar 1:1
- UserSelectedSize: --ar 1464:610
```

## 📊 输出结果示例

### 智能分析结果
```json
{
  "product_analysis": {
    "product_name": "便携式LED野营灯笼",
    "target_audience": "户外露营爱好者，适用于夜间帐篷照明、停电应急",
    "selling_points_description": "可折叠设计，收纳后仅手掌大小；底部磁吸设计；IPX4防水等级",
    "extracted_selling_points": ["便携设计", "磁吸功能", "防水功能", "LED照明"],
    "model_used": "gpt-4-vision-preview"
  },
  "prompts": [
    {
      "selling_point": "便携设计",
      "prompt": "Professional Amazon e-commerce photography...",
      "optimized_for": ["Midjourney", "DALL-E 3", "Stability AI"]
    }
  ]
}
```

### 品牌基因报告
```json
{
  "brandColor": "户外运动 #4CAF50",
  "字体风格": "硬朗无衬线体",
  "背景策略": "美国本土化现代生活场景",
  "PURE_GRAPHICS_CODE": "实心圆图标系统"
}
```

## 🔧 高级配置

### API密钥配置
```
# OpenAI GPT-4V (推荐商业产品)
vision_api_key: sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Anthropic Claude-3 Sonnet (推荐创意产品)  
vision_api_key: sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# 无密钥（模拟模式，适合测试）
# 不提供密钥，AI将使用模拟分析
```

### 裂变模式触发
```
**产品信息**:
- 核心卖点: 防水、快充、智能  # 3个卖点
- 输出数量: 10                # 超过卖点数量

**AI自动扩展**:
✅ 防水 → IPX7防水、生活防水、雨天防护
✅ 快充 → 闪充技术、快充协议、充电速度  
✅ 智能 → AI智能、智能识别、智能控制
```

### 品牌基因自定义
```
**高级设置**:
- brandKey: {
    "brandColor": "#2196F3",
    "fontStyle": "几何无衬线体",
    "iconStyle": "实心圆"
  }
```

## 🎨 平台使用指南

### Midjourney
```
# 直接复制prompt
/imagine [生成的完整prompt] --ar 1:1 --v 6

# 调整风格
/imagine [prompt] --ar 1:1 --style raw --stylize 300
```

### DALL-E 3
```
# OpenAI ChatGPT Plus
直接粘贴完整prompt，DALL-E 3会自动优化

# API调用
{
  "model": "dall-e-3",
  "prompt": "[生成的prompt]",
  "size": "1024x1024",
  "quality": "hd"
}
```

### Stability AI
```
# Stability AI API
curl -X POST \
  "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image" \
  -d '{
    "text_prompts": [{"text": "[生成的prompt]"}],
    "cfg_scale": 7,
    "width": 1024,
    "height": 1024
  }'
```

### Leonardo AI
```
# 界面操作
1. 选择模型: Leonardo Diffusion XL
2. 粘贴prompt到文本框
3. 设置尺寸: 1024x1024 
4. 点击Generate
```

## ❓ 常见问题

### Q: 没有API密钥能用吗？
A: 可以！不提供API密钥时会使用模拟分析模式，虽然准确性不如真实分析，但仍能生成高质量prompt。

### Q: 支持哪些图片格式？
A: 支持jpg、png、webp等常见格式。建议使用清晰的产品图片，避免背景过于复杂。

### Q: Claude和GPT-4V哪个更好？
A: GPT-4V在商业产品理解上更强，Claude在创意产品分析上表现更好。建议根据产品类型选择。

### Q: 生成的卖点不准确怎么办？
A: 可以使用混合模式，让AI分析后手动调整卖点，或直接使用传统模式手动输入所有信息。

### Q: 如何获得更好的分析结果？
A: 
- 使用高质量产品图片
- 提供清晰的产品主体
- 避免过于复杂的背景
- 使用真实API密钥而非模拟模式

## 🚀 最佳实践

1. **图片准备**: 使用白底产品图或清晰实拍图
2. **API选择**: 商业产品用GPT-4V，创意产品用Claude  
3. **结果验证**: 检查自动生成的卖点是否准确
4. **手动微调**: 必要时补充或修正AI分析结果
5. **平台优化**: 根据目标平台特点调整prompt参数

---

*🎯 Amazon Image Skill v1.0 - 让AI理解你的产品，让商品套图生成更加智能！*