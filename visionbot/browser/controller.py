#!/usr/bin/env python3
"""
Browser Controller - کنترل مرورگر با Playwright
"""

from playwright.async_api import async_playwright
from typing import Optional
import os

class BrowserController:
    """کنترل مرورگر و تعامل با آن"""
    
    def __init__(self, headless: bool = False):
        self.headless = headless
        self.browser = None
        self.page = None
        self.playwright = None
    
    async def start(self):
        """راه‌اندازی مرورگر"""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=self.headless)
        self.page = await self.browser.new_page(viewport={"width": 1920, "height": 1080})
    
    async def open(self, url: str):
        """باز کردن یک URL"""
        if not self.page:
            await self.start()
        await self.page.goto(url)
        await self.page.wait_for_load_state("networkidle")
    
    async def screenshot(self) -> bytes:
        """گرفتن اسکرین‌شات"""
        return await self.page.screenshot(full_page=True)
    
    async def click(self, coordinates: dict):
        """کلیک در مختصات مشخص"""
        x = coordinates.get('x', 0)
        y = coordinates.get('y', 0)
        await self.page.mouse.click(x, y)
    
    async def type_text(self, coordinates: dict, text: str):
        """تایپ متن در مختصات مشخص"""
        x = coordinates.get('x', 0)
        y = coordinates.get('y', 0)
        await self.page.mouse.click(x, y)
        await self.page.keyboard.type(text)
    
    async def extract_text(self, selector: str) -> str:
        """استخراج متن با سلکتور"""
        element = await self.page.query_selector(selector)
        if element:
            return await element.inner_text()
        return ""
    
    async def close(self):
        """بستن مرورگر"""
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
