#!/usr/bin/env python3
"""
Demo Login Script - نمونه‌ی اسکریپت ورود خودکار
"""

async def run(browser, vision):
    """اجرای اسکریپت ورود خودکار"""
    
    print("🔐 Running demo login automation...")
    
    # ۱. باز کردن سایت
    await browser.open("https://example.com/login")
    
    # ۲. گرفتن اسکرین‌شات
    screenshot = await browser.screenshot()
    
    # ۳. پیدا کردن فیلدهای ورود
    username_field = vision.locate_element(screenshot, "Username input field")
    password_field = vision.locate_element(screenshot, "Password input field")
    login_button = vision.locate_element(screenshot, "Login button")
    
    # ۴. تایپ اطلاعات
    if username_field:
        await browser.type_text(username_field, "demo_user")
    if password_field:
        await browser.type_text(password_field, "demo_password")
    
    # ۵. کلیک روی دکمه ورود
    if login_button:
        await browser.click(login_button)
    
    # ۶. گرفتن اسکرین‌شات از نتیجه
    final_screenshot = await browser.screenshot()
    
    print("✅ Login automation completed!")
    return final_screenshot
