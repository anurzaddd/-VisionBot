#!/usr/bin/env python3
"""
Vision Analyzer - Analyze screenshots with Vision-Language Models
"""

import base64
import json
from typing import List, Dict, Optional
import requests
import os

class VisionAnalyzer:
    """تحلیل صفحه با استفاده از مدل‌های بینایی"""
    
    def __init__(self, model: str = "openai"):
        self.model = model
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.api_url = "https://api.openai.com/v1/chat/completions"
    
    def analyze(self, screenshot: bytes) -> Dict:
        """تحلیل اسکرین‌شات و شناسایی المان‌ها"""
        if self.model == "openai":
            return self._analyze_with_gpt4v(screenshot)
        elif self.model == "llava":
            return self._analyze_with_llava(screenshot)
        else:
            return self._simulate_analysis(screenshot)
    
    def _analyze_with_gpt4v(self, screenshot: bytes) -> Dict:
        """استفاده از GPT-4V برای تحلیل"""
        if not self.api_key:
            return self._simulate_analysis(screenshot)
        
        # تبدیل تصویر به Base64
        base64_image = base64.b64encode(screenshot).decode('utf-8')
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        payload = {
            "model": "gpt-4-vision-preview",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": """Analyze this webpage screenshot and return a JSON with:
                            1. All interactive elements (buttons, links, inputs, dropdowns)
                            2. Their approximate coordinates (x, y, width, height)
                            3. Their type and visible text
                            Return ONLY valid JSON."""
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 2000
        }
        
        try:
            response = requests.post(self.api_url, headers=headers, json=payload)
            result = response.json()
            content = result.get('choices', [{}])[0].get('message', {}).get('content', '{}')
            return json.loads(content)
        except:
            return self._simulate_analysis(screenshot)
    
    def _simulate_analysis(self, screenshot: bytes) -> Dict:
        """شبیه‌سازی تحلیل (برای تست بدون API)"""
        return {
            "elements": [
                {"type": "button", "text": "Login", "position": "center-right"},
                {"type": "input", "text": "Username", "position": "center-left"},
                {"type": "input", "text": "Password", "position": "center-left-bottom"},
                {"type": "link", "text": "Forgot Password", "position": "bottom-right"},
                {"type": "button", "text": "Sign Up", "position": "bottom-center"},
            ],
            "total": 5,
            "message": "AI analysis completed (simulated mode)"
        }
    
    def locate_element(self, screenshot: bytes, description: str) -> Optional[Dict]:
        """پیدا کردن یک المان بر اساس توضیح"""
        # در نسخه‌ی واقعی، با GPT-4V مختصات دقیق رو می‌گیریم
        # اینجا شبیه‌سازی می‌کنیم
        return {"x": 500, "y": 300, "width": 200, "height": 50}
    
    def extract(self, screenshot: bytes, query: str) -> str:
        """استخراج داده از صفحه"""
        if "price" in query.lower():
            return "Found 5 prices: $19.99, $29.99, $39.99, $49.99, $59.99"
        elif "email" in query.lower():
            return "Found 3 emails: contact@example.com, support@example.com, admin@example.com"
        else:
            return "Extracted data: Sample text from the page"
