# Amazon Visual Architect - 使用示例

## 示例1：蓝牙耳机产品

### 输入参数
```json
{
  "GenerateAPlus": "true",
  "outputNum": 6,
  "ListingUserSelectedSize": "--ar 1:1",
  "UserSelectedSize": "--ar 1464:610", 
  "language": "英语",
  "customer_keywords": ["降噪功能", "长续航", "舒适佩戴", "快速配对"],
  "salesRegion": "美国",
  "platform": "Amazon",
  "目标受众": "25-35岁通勤族",
  "我的侵权词": []
}
```

### 输出示例

#### 品牌基因报告
```json
{
  "category": "Brand DNA Profile",
  "brandColor (品牌主色)": "Tech Blue #2196F3",
  "背景策略-风格定义": "现代科技感生活场景",
  "背景策略-场景关键词": "通勤、办公、运动",
  "背景策略-光影": "自然光与科技感结合",
  "Brand Injection（品牌植入）": "科技蓝主导的现代数码美学",
  "字体策略": "几何无衬线体",
  "字体风格": "Montserrat",
  "颜色策略-Heading": "#1976D2",
  "颜色策略-Body/Sub": "#424242", 
  "灵活反白": "深色背景自动切换白色文字",
  "排版": "非斜体，适中行距",
  "PURE_GRAPHICS_CODE（纯图形代码）": "实心圆图标系统",
  "形状": "圆形容器",
  "质感": "实心填充",
  "描边": "无描边"
}
```

#### Prompt列表示例
```json
[
  {
    "id": 1,
    "category": "📦 Listing Image (卖点图 1:1)",
    "selling_point": "降噪功能",
    "layout_model": "L2 - 卖点特征块布局",
    "visual_logic": "✅ ACTIVE (启用变量三)",
    "language": "英语",
    "salesRegion": "美国",
    "目标受众": "25-35岁通勤族",
    "prompt": "不允许文字中出现色值，例如\"#688967\"。ABSOLUTE LANGUAGE LOCK: ALL on-screen text must be in English不能影响商品上的文字. Amazon e-commerce diagram, aspect ratio 1:1, Keep the product structure intact. Horizontal layout with product on left side, feature blocks on right side showcasing noise cancellation technology. Core color:#2196F3, modern tech aesthetic with clean geometric lines. Typography: Montserrat font family, heading color #1976D2. Icons are minimalist Pure White (#FFFFFF) glyphs centered inside Solid Circular Container filled with #2196F3. Demographic: 25-35 American commuters. Scene: Professional wearing earbuds in busy subway station, peaceful expression showing noise isolation effect. Title: \"NOISE CANCELLATION\" Text: \"Advanced ANC Technology\" \"Crystal Clear Audio\" \"Focus Mode\""
  },
  {
    "id": 2, 
    "category": "🎬 A+ Image (品牌图 1464:610)",
    "selling_point": "通勤场景",
    "layout_model": "A4 - 极简摄影-自然景深留白",
    "visual_logic": "🔴 DISABLED (禁用变量三)",
    "language": "英语",
    "salesRegion": "美国", 
    "目标受众": "25-35岁通勤族",
    "prompt": "不允许文字中出现色值，例如\"#688967\"。ABSOLUTE LANGUAGE LOCK: ALL on-screen text must be in English不能影响商品上的文字. Amazon A+ content image, aspect ratio 1464:610, commercial infographic design. Horizontal layout with extreme asymmetrical composition, earbuds positioned at 1/3 of frame. Core color:#2196F3, natural window lighting creating soft focus zen atmosphere. Typography: Montserrat font family, heading color #1976D2. Photorealistic commuter scene with professional using earbuds, natural depth of field. Background: continuous photographic scene of modern train interior. Title: \"COMMUTE IN COMFORT\" Text: \"Your Perfect Travel Companion\""
  }
]
```

## 示例2：户外背包产品

### 输入参数
```json
{
  "GenerateAPlus": "false",
  "outputNum": 4,
  "ListingUserSelectedSize": "--ar 1:1",
  "language": "中文",
  "customer_keywords": ["防水透气", "大容量", "轻便舒适", "多口袋设计"],
  "salesRegion": "中国",
  "platform": "Amazon",
  "目标受众": "18-30岁户外运动爱好者",
  "我的侵权词": []
}
```

### 期望输出结构
- 全部4张图均为Listing主图格式(1:1)
- 品牌基因提取户外运动风格色彩
- 针对中国市场和年轻户外群体设计
- 中文文字内容

## 示例3：美容护肤产品

### 输入参数
```json
{
  "GenerateAPlus": "true",
  "outputNum": 8,
  "ListingUserSelectedSize": "--ar 1:1",
  "UserSelectedSize": "--ar 1464:610",
  "language": "英语",
  "customer_keywords": ["天然有机", "抗衰老", "深层滋润", "敏感肌适用"],
  "brandKey": {
    "brandColor": "#E8B4CB",
    "fontStyle": "经典优雅衬线体",
    "iconStyle": "描边圆"
  },
  "salesRegion": "欧洲",
  "platform": "Amazon", 
  "目标受众": "30-50岁女性",
  "我的侵权词": ["医疗", "治疗", "药物"]
}
```

### 特色功能展示
- 使用预设品牌基因(粉色系+优雅衬线体)
- 4张Listing主图 + 4张A+图片
- 针对欧洲成熟女性市场
- 侵权词过滤(医疗相关词汇)

## 示例4：智能家居产品

### 输入参数
```json
{
  "GenerateAPlus": "true", 
  "outputNum": 10,
  "ListingUserSelectedSize": "--ar 1:1",
  "UserSelectedSize": "--ar 1464:610",
  "language": "英语",
  "customer_keywords": ["智能控制", "节能环保", "语音助手", "远程监控", "安全防护"],
  "salesRegion": "美国",
  "platform": "Amazon",
  "目标受众": "25-45岁科技达人家庭",
  "我的侵权词": []
}
```

### 裂变模式展示
- 输出数量(10)超过卖点数量(5)
- 自动触发裂变模式
- 确保每张图的selling_point唯一
- 智能扩展相关卖点和场景

## 使用技巧

### 1. 参数优化建议

#### 卖点数量规划
- **建议3-6个核心卖点**: 太少显单薄，太多难聚焦
- **卖点要有差异化**: 避免功能重复
- **考虑用户购买决策因素**: 功能、品质、价格、体验

#### 输出数量设置
- **6-12张为最佳**: 既保证覆盖全面又避免冗余
- **建议开启A+模式**: 获得更全面的视觉资产
- **考虑平台要求**: Amazon主图5张+A+内容

#### 区域和受众定位
- **销售区域影响**: 模特人种、场景风格、文化元素
- **目标受众影响**: 年龄段、生活方式、审美偏好
- **要具体描述**: "25-35岁职场女性"比"年轻女性"更精准

### 2. 品牌基因定制

#### 何时使用brandKey
- **已有品牌规范**: 使用brandKey锁定现有视觉系统
- **系列产品**: 确保视觉一致性
- **品牌升级**: 在现有基础上微调

#### 色彩选择策略
- **产品属性匹配**: 科技产品用蓝色系，美容产品用粉色系
- **目标市场偏好**: 考虑文化色彩喜好
- **差异化竞争**: 避免与主要竞品色彩雷同

### 3. 常见问题解决

#### Q: 生成的图片场景重复
A: 增加卖点多样性，明确不同的使用场景和功能重点

#### Q: 文字内容过于简单
A: 在customer_keywords中提供更详细的卖点描述

#### Q: 品牌色彩不理想
A: 通过brandKey手动指定，或调整产品描述引导AI选择

#### Q: 布局选择不合适
A: 卖点分类要准确，功能类→L系列，品牌类→A系列

### 4. 最佳实践

#### 输入准备清单
- [ ] 高质量产品图片(白底图+实拍图)
- [ ] 3-6个明确差异化卖点
- [ ] 详细目标受众描述
- [ ] 明确销售区域和平台
- [ ] 整理侵权词清单

#### 输出质量检查
- [ ] 每张图selling_point唯一
- [ ] 文字语言符合设置
- [ ] 视觉风格统一
- [ ] 布局选择合理
- [ ] 无侵权词汇

#### 后续优化
- [ ] A/B测试不同风格
- [ ] 根据转化数据调整
- [ ] 季节性更新视觉
- [ ] 竞品分析优化