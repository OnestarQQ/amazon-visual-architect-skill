# Amazon Visual Architect - 图片生成功能

## 功能升级概览

在原有prompt生成基础上，新增**直接生图功能**，支持多个主流AI绘图平台API调用。

## 🎨 支持的生图平台

### 1. Stable Diffusion (推荐)
- **平台**: Stability AI Official API
- **优势**: 质量高，成本合理，商用友好
- **API**: https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image
- **费用**: ~$0.02-0.04/张

### 2. OpenAI DALL-E 3
- **平台**: OpenAI Official API  
- **优势**: 文字理解强，画面精准
- **API**: https://api.openai.com/v1/images/generations
- **费用**: $0.04-0.08/张

### 3. Replicate (多模型)
- **平台**: Replicate Cloud API
- **优势**: 支持多种开源模型，性价比高
- **API**: https://api.replicate.com/v1/predictions
- **费用**: ~$0.01-0.03/张

### 4. 智谱清言 (国内)
- **平台**: 智谱AI CogView API
- **优势**: 国内访问速度快，中文理解好
- **API**: https://open.bigmodel.cn/api/paas/v4/images/generations
- **费用**: ¥0.1-0.2/张

## 📋 升级后的工作流程

### 原流程
```
用户输入 → 品牌基因提取 → 智能分流 → 生成Prompts → 输出JSON
```

### 新流程
```
用户输入 → 品牌基因提取 → 智能分流 → 生成Prompts → 调用生图API → 返回图片URLs → 打包下载
```

## 🔧 新增参数配置

### 必需参数
```json
{
  "generate_images": true,          // 是否生成图片
  "image_platform": "stability",   // 生图平台选择
  "api_key": "your-api-key",       // 对应平台的API Key
  "image_size": "1024x1024"        // 图片尺寸
}
```

### 可选参数
```json
{
  "quality": "high",               // 图片质量 (low/medium/high)
  "batch_size": 1,                 // 每个prompt生成图片数量
  "save_prompts": true,            // 是否同时保存prompt文件
  "output_format": "zip"           // 输出格式 (zip/folder)
}
```

## 💻 技术实现架构

### 1. 平台适配器 (Platform Adapters)
```python
class ImagePlatform:
    def __init__(self, api_key, platform):
        self.api_key = api_key
        self.platform = platform
    
    def generate_image(self, prompt, size, quality):
        if self.platform == "stability":
            return self._stability_api(prompt, size, quality)
        elif self.platform == "openai":
            return self._openai_api(prompt, size, quality)
        elif self.platform == "replicate":
            return self._replicate_api(prompt, size, quality)
        elif self.platform == "zhipu":
            return self._zhipu_api(prompt, size, quality)
```

### 2. 批量处理引擎
```python
async def batch_generate_images(prompts, platform, api_key):
    tasks = []
    for prompt_data in prompts:
        task = generate_single_image(
            prompt=prompt_data['prompt'],
            platform=platform,
            api_key=api_key,
            metadata=prompt_data
        )
        tasks.append(task)
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return results
```

### 3. 结果打包系统
```python
def package_results(images, prompts, format="zip"):
    if format == "zip":
        return create_zip_package(images, prompts)
    elif format == "folder":
        return create_folder_structure(images, prompts)
```

## 🎯 用户交互流程

### 1. 基础使用
```bash
使用亚马逊全案视觉架构师技能生成图片：

**产品信息**:
- 商品图片: [上传]
- 核心卖点: 防水、轻便、大容量、快速充电
- 销售区域: 美国
- 目标受众: 25-40岁户外运动爱好者

**生图设置**:
- generate_images: true
- image_platform: stability
- api_key: sk-xxxxxxxxxxxx
- image_size: 1024x1024
- quality: high
```

### 2. 平台选择指南
```bash
# 推荐平台选择：
商业电商图片 → Stability AI (质量稳定)
创意概念图 → OpenAI DALL-E 3 (理解力强)  
批量测试 → Replicate (成本低)
国内项目 → 智谱清言 (速度快)
```

## 📊 输出格式升级

### 原输出 (仅Prompt)
```json
[
  {
    "id": 1,
    "category": "📦 Listing Image",
    "selling_point": "防水功能",
    "prompt": "Amazon e-commerce diagram..."
  }
]
```

### 新输出 (Prompt + 图片)
```json
[
  {
    "id": 1,
    "category": "📦 Listing Image",
    "selling_point": "防水功能", 
    "prompt": "Amazon e-commerce diagram...",
    "generated_image": {
      "url": "https://cdn.example.com/image1.png",
      "local_path": "/generated/listing_1_waterproof.png",
      "size": "1024x1024",
      "platform": "stability",
      "generation_time": "2026-03-17T15:10:23Z",
      "cost": "$0.032"
    }
  }
]
```

## 🔒 安全和成本控制

### API Key 安全
- 支持环境变量配置
- 本地加密存储选项
- 使用后不在日志中显示

### 成本控制
```python
# 成本预估
def estimate_cost(prompt_count, platform, quality):
    cost_map = {
        "stability": {"low": 0.02, "medium": 0.03, "high": 0.04},
        "openai": {"low": 0.04, "medium": 0.06, "high": 0.08},
        "replicate": {"low": 0.01, "medium": 0.02, "high": 0.03},
        "zhipu": {"low": 0.015, "medium": 0.02, "high": 0.025}
    }
    
    total_cost = prompt_count * cost_map[platform][quality]
    return f"预估费用: ${total_cost:.2f}"
```

### 错误处理
- API限流自动重试
- 失败图片标记和跳过
- 部分成功结果保存

## 🚀 实施步骤

### Phase 1: 基础架构 (Week 1)
- [x] 平台适配器框架
- [x] Stability AI API集成
- [x] 基础错误处理

### Phase 2: 多平台支持 (Week 2)  
- [ ] OpenAI DALL-E 3 集成
- [ ] Replicate API集成
- [ ] 智谱清言API集成

### Phase 3: 高级功能 (Week 3)
- [ ] 批量处理优化
- [ ] 成本控制和预估
- [ ] 结果打包和下载

### Phase 4: 用户体验 (Week 4)
- [ ] 进度显示和实时反馈
- [ ] 错误恢复和重试机制
- [ ] 性能监控和日志

## 💡 使用示例

### 示例1: 标准电商图片生成
```bash
# 输入
generate_images: true
image_platform: stability  
api_key: sk-xxxxxxxx
prompts: 6个 (3个Listing + 3个A+)

# 输出
6张高质量电商图片 + prompt文件 + 成本报告
预估费用: $0.18-0.24
生成时间: 2-3分钟
```

### 示例2: 批量A/B测试
```bash
# 输入  
generate_images: true
image_platform: replicate
batch_size: 2  # 每个prompt生成2张图
prompts: 4个

# 输出
8张图片 (每个卖点2个版本)
预估费用: $0.08-0.12  
适合A/B测试对比
```

## 📈 预期效果

### 效率提升
- **设计时间**: 从数小时缩短到数分钟
- **成本节省**: 相比人工设计节省80%+
- **质量保证**: AI生成质量稳定，风格统一

### 商业价值
- **快速迭代**: 支持快速A/B测试
- **规模化**: 支持批量产品视觉设计
- **标准化**: 确保品牌视觉一致性

这个升级将让Amazon Visual Architect从"prompt生成器"变成真正的"一站式电商视觉设计工具"！