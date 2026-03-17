#!/usr/bin/env python3
"""
Amazon Visual Architect - Image Generation Module
支持多平台AI绘图API调用和批量图片生成
"""

import asyncio
import aiohttp
import json
import os
import time
from datetime import datetime
from typing import Dict, List, Optional, Union
import base64
from pathlib import Path

class ImageGenerator:
    """多平台AI绘图API调用器"""
    
    def __init__(self, platform: str, api_key: str):
        self.platform = platform.lower()
        self.api_key = api_key
        self.session = None
        
        # 平台配置
        self.platform_config = {
            "stability": {
                "url": "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image",
                "headers": {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                "cost_per_image": 0.032
            },
            "openai": {
                "url": "https://api.openai.com/v1/images/generations",
                "headers": {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                "cost_per_image": 0.060
            },
            "replicate": {
                "url": "https://api.replicate.com/v1/predictions",
                "headers": {
                    "Authorization": f"Token {api_key}",
                    "Content-Type": "application/json"
                },
                "cost_per_image": 0.020
            },
            "zhipu": {
                "url": "https://open.bigmodel.cn/api/paas/v4/images/generations",
                "headers": {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                "cost_per_image": 0.025
            }
        }
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    def estimate_cost(self, prompt_count: int, quality: str = "high") -> float:
        """预估生成成本"""
        base_cost = self.platform_config[self.platform]["cost_per_image"]
        quality_multiplier = {"low": 0.7, "medium": 1.0, "high": 1.3}.get(quality, 1.0)
        return prompt_count * base_cost * quality_multiplier
    
    async def generate_image(self, prompt_data: Dict, size: str = "1024x1024", 
                           quality: str = "high") -> Dict:
        """生成单张图片"""
        try:
            if self.platform == "stability":
                return await self._stability_generate(prompt_data, size, quality)
            elif self.platform == "openai":
                return await self._openai_generate(prompt_data, size, quality)
            elif self.platform == "replicate":
                return await self._replicate_generate(prompt_data, size, quality)
            elif self.platform == "zhipu":
                return await self._zhipu_generate(prompt_data, size, quality)
            else:
                raise ValueError(f"Unsupported platform: {self.platform}")
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "prompt_id": prompt_data.get("id", "unknown"),
                "timestamp": datetime.now().isoformat()
            }
    
    async def _stability_generate(self, prompt_data: Dict, size: str, quality: str) -> Dict:
        """Stability AI API调用"""
        width, height = map(int, size.split('x'))
        steps = {"low": 20, "medium": 30, "high": 50}[quality]
        
        payload = {
            "text_prompts": [{"text": prompt_data["prompt"]}],
            "cfg_scale": 7,
            "height": height,
            "width": width,
            "samples": 1,
            "steps": steps
        }
        
        config = self.platform_config["stability"]
        
        async with self.session.post(config["url"], 
                                   json=payload, 
                                   headers=config["headers"]) as response:
            if response.status == 200:
                data = await response.json()
                
                # 保存图片
                image_data = data["artifacts"][0]["base64"]
                filename = f"{prompt_data['category'].replace(' ', '_')}_{prompt_data['id']}_{prompt_data['selling_point'][:10]}.png"
                filepath = await self._save_image(image_data, filename, "base64")
                
                return {
                    "success": True,
                    "prompt_id": prompt_data["id"],
                    "category": prompt_data["category"],
                    "selling_point": prompt_data["selling_point"],
                    "image_url": None,  # Stability返回base64
                    "local_path": filepath,
                    "size": size,
                    "platform": "stability",
                    "generation_time": datetime.now().isoformat(),
                    "cost": config["cost_per_image"],
                    "original_prompt": prompt_data["prompt"]
                }
            else:
                error_text = await response.text()
                raise Exception(f"Stability API Error {response.status}: {error_text}")
    
    async def _openai_generate(self, prompt_data: Dict, size: str, quality: str) -> Dict:
        """OpenAI DALL-E 3 API调用"""
        # DALL-E 3 支持的尺寸
        dalle_size = size if size in ["1024x1024", "1024x1792", "1792x1024"] else "1024x1024"
        
        payload = {
            "model": "dall-e-3",
            "prompt": prompt_data["prompt"],
            "n": 1,
            "size": dalle_size,
            "quality": "hd" if quality == "high" else "standard"
        }
        
        config = self.platform_config["openai"]
        
        async with self.session.post(config["url"],
                                   json=payload,
                                   headers=config["headers"]) as response:
            if response.status == 200:
                data = await response.json()
                image_url = data["data"][0]["url"]
                
                # 下载并保存图片
                filename = f"{prompt_data['category'].replace(' ', '_')}_{prompt_data['id']}_{prompt_data['selling_point'][:10]}.png"
                filepath = await self._download_and_save(image_url, filename)
                
                return {
                    "success": True,
                    "prompt_id": prompt_data["id"],
                    "category": prompt_data["category"], 
                    "selling_point": prompt_data["selling_point"],
                    "image_url": image_url,
                    "local_path": filepath,
                    "size": dalle_size,
                    "platform": "openai",
                    "generation_time": datetime.now().isoformat(),
                    "cost": config["cost_per_image"],
                    "original_prompt": prompt_data["prompt"]
                }
            else:
                error_text = await response.text()
                raise Exception(f"OpenAI API Error {response.status}: {error_text}")
    
    async def _replicate_generate(self, prompt_data: Dict, size: str, quality: str) -> Dict:
        """Replicate API调用 (使用SDXL模型)"""
        payload = {
            "version": "39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",  # SDXL
            "input": {
                "prompt": prompt_data["prompt"],
                "width": int(size.split('x')[0]),
                "height": int(size.split('x')[1]),
                "num_inference_steps": {"low": 20, "medium": 30, "high": 50}[quality],
                "guidance_scale": 7.5
            }
        }
        
        config = self.platform_config["replicate"]
        
        # 创建预测
        async with self.session.post(config["url"],
                                   json=payload,
                                   headers=config["headers"]) as response:
            if response.status == 201:
                prediction = await response.json()
                prediction_id = prediction["id"]
                
                # 轮询结果
                result = await self._poll_replicate_result(prediction_id)
                
                if result["success"]:
                    image_url = result["output"][0]
                    filename = f"{prompt_data['category'].replace(' ', '_')}_{prompt_data['id']}_{prompt_data['selling_point'][:10]}.png"
                    filepath = await self._download_and_save(image_url, filename)
                    
                    return {
                        "success": True,
                        "prompt_id": prompt_data["id"],
                        "category": prompt_data["category"],
                        "selling_point": prompt_data["selling_point"], 
                        "image_url": image_url,
                        "local_path": filepath,
                        "size": size,
                        "platform": "replicate",
                        "generation_time": datetime.now().isoformat(),
                        "cost": config["cost_per_image"],
                        "original_prompt": prompt_data["prompt"]
                    }
                else:
                    raise Exception(f"Replicate generation failed: {result.get('error', 'Unknown error')}")
            else:
                error_text = await response.text()
                raise Exception(f"Replicate API Error {response.status}: {error_text}")
    
    async def _zhipu_generate(self, prompt_data: Dict, size: str, quality: str) -> Dict:
        """智谱清言 CogView API调用"""
        payload = {
            "model": "cogview-3",
            "prompt": prompt_data["prompt"],
            "size": size,
            "quality": quality,
            "n": 1
        }
        
        config = self.platform_config["zhipu"]
        
        async with self.session.post(config["url"],
                                   json=payload,
                                   headers=config["headers"]) as response:
            if response.status == 200:
                data = await response.json()
                image_url = data["data"][0]["url"]
                
                filename = f"{prompt_data['category'].replace(' ', '_')}_{prompt_data['id']}_{prompt_data['selling_point'][:10]}.png"
                filepath = await self._download_and_save(image_url, filename)
                
                return {
                    "success": True,
                    "prompt_id": prompt_data["id"],
                    "category": prompt_data["category"],
                    "selling_point": prompt_data["selling_point"],
                    "image_url": image_url, 
                    "local_path": filepath,
                    "size": size,
                    "platform": "zhipu",
                    "generation_time": datetime.now().isoformat(),
                    "cost": config["cost_per_image"],
                    "original_prompt": prompt_data["prompt"]
                }
            else:
                error_text = await response.text()
                raise Exception(f"ZhiPu API Error {response.status}: {error_text}")
    
    async def _poll_replicate_result(self, prediction_id: str, max_wait: int = 300) -> Dict:
        """轮询Replicate结果"""
        url = f"https://api.replicate.com/v1/predictions/{prediction_id}"
        headers = self.platform_config["replicate"]["headers"]
        
        start_time = time.time()
        while time.time() - start_time < max_wait:
            async with self.session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    status = data["status"]
                    
                    if status == "succeeded":
                        return {"success": True, "output": data["output"]}
                    elif status == "failed":
                        return {"success": False, "error": data.get("error", "Unknown error")}
                    else:
                        await asyncio.sleep(2)  # 等待2秒后重试
                else:
                    return {"success": False, "error": f"HTTP {response.status}"}
        
        return {"success": False, "error": "Timeout waiting for result"}
    
    async def _save_image(self, image_data: str, filename: str, format_type: str = "base64") -> str:
        """保存图片到本地"""
        os.makedirs("generated_images", exist_ok=True)
        filepath = os.path.join("generated_images", filename)
        
        if format_type == "base64":
            with open(filepath, "wb") as f:
                f.write(base64.b64decode(image_data))
        
        return filepath
    
    async def _download_and_save(self, url: str, filename: str) -> str:
        """从URL下载图片并保存"""
        os.makedirs("generated_images", exist_ok=True)
        filepath = os.path.join("generated_images", filename)
        
        async with self.session.get(url) as response:
            if response.status == 200:
                with open(filepath, "wb") as f:
                    async for chunk in response.content.iter_chunked(8192):
                        f.write(chunk)
                return filepath
            else:
                raise Exception(f"Failed to download image: HTTP {response.status}")

class BatchImageGenerator:
    """批量图片生成器"""
    
    def __init__(self, platform: str, api_key: str):
        self.platform = platform
        self.api_key = api_key
    
    async def generate_batch(self, prompts: List[Dict], size: str = "1024x1024", 
                           quality: str = "high", max_concurrent: int = 3) -> Dict:
        """批量生成图片"""
        
        # 成本预估
        async with ImageGenerator(self.platform, self.api_key) as generator:
            estimated_cost = generator.estimate_cost(len(prompts), quality)
            
            print(f"🎨 开始批量生成 {len(prompts)} 张图片")
            print(f"💰 预估费用: ${estimated_cost:.3f}")
            print(f"🖥️ 使用平台: {self.platform.upper()}")
            
            # 创建信号量控制并发数
            semaphore = asyncio.Semaphore(max_concurrent)
            
            async def generate_with_semaphore(prompt_data):
                async with semaphore:
                    return await generator.generate_image(prompt_data, size, quality)
            
            # 批量执行
            tasks = [generate_with_semaphore(prompt) for prompt in prompts]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # 统计结果
            successful = [r for r in results if isinstance(r, dict) and r.get("success")]
            failed = [r for r in results if not (isinstance(r, dict) and r.get("success"))]
            
            total_cost = sum(r.get("cost", 0) for r in successful)
            
            summary = {
                "total_prompts": len(prompts),
                "successful_images": len(successful),
                "failed_images": len(failed),
                "success_rate": len(successful) / len(prompts) * 100,
                "total_cost": total_cost,
                "platform": self.platform,
                "generation_time": datetime.now().isoformat(),
                "results": results
            }
            
            print(f"✅ 生成完成! 成功: {len(successful)}/{len(prompts)} ({summary['success_rate']:.1f}%)")
            print(f"💵 实际费用: ${total_cost:.3f}")
            
            return summary

# 使用示例和测试函数
async def example_usage():
    """使用示例"""
    
    # 示例prompt数据
    sample_prompts = [
        {
            "id": 1,
            "category": "📦 Listing Image",
            "selling_point": "防水功能",
            "prompt": "Amazon e-commerce product photo, waterproof bluetooth headphones, lifestyle scene with person jogging in rain, modern tech aesthetic, core color:#2196F3, professional photography, clean background, product focus"
        },
        {
            "id": 2, 
            "category": "🎬 A+ Image",
            "selling_point": "长续航",
            "prompt": "Amazon A+ content image, aspect ratio 1464:610, bluetooth earbuds battery life demonstration, split scene showing morning to evening usage, modern tech aesthetic, core color:#2196F3, lifestyle photography"
        }
    ]
    
    # 批量生成 (使用Stability AI)
    batch_generator = BatchImageGenerator(
        platform="stability",  # 可选: stability, openai, replicate, zhipu
        api_key="your-stability-api-key-here"
    )
    
    results = await batch_generator.generate_batch(
        prompts=sample_prompts,
        size="1024x1024", 
        quality="high",
        max_concurrent=2
    )
    
    return results

if __name__ == "__main__":
    # 运行示例
    # asyncio.run(example_usage())
    print("Amazon Visual Architect - Image Generation Module Ready!")
    print("Usage: from image_generator import BatchImageGenerator")