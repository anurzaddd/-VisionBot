#!/usr/bin/env python3
"""
VisionBot - Vision-Based Web Automation Bot
Author: Amir Hossein Nourzadeh
"""

import asyncio
import time
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.markdown import Markdown

from .browser.controller import BrowserController
from .vision.analyzer import VisionAnalyzer
from .actions.click import ClickAction
from .actions.type import TypeAction
from .actions.extract import ExtractAction
from .reporter.html import HTMLReporter
from .utils.animations import matrix_rain, hacker_typing, glow_effect

console = Console()

class VisionBotCLI:
    """VisionBot - رابط کاربری خط فرمان"""
    
    def __init__(self):
        self.browser = BrowserController()
        self.vision = VisionAnalyzer()
        self.clicker = ClickAction()
        self.typer = TypeAction()
        self.extractor = ExtractAction()
        self.results = []
        self.screenshots = []
    
    def show_banner(self):
        """نمایش بنر جذاب"""
        banner = """
        ╔═══════════════════════════════════════════════════════════╗
        ║                                                           ║
        ║   ██╗   ██╗██╗███████╗██╗ ██████╗ ███╗   ██╗ ██████╗ ████████╗
        ║   ██║   ██║██║██╔════╝██║██╔═══██╗████╗  ██║██╔═══██╗╚══██╔══╝
        ║   ██║   ██║██║███████╗██║██║   ██║██╔██╗ ██║██║   ██║   ██║   
        ║   ╚██╗ ██╔╝██║╚════██║██║██║   ██║██║╚██╗██║██║   ██║   ██║   
        ║    ╚████╔╝ ██║███████║██║╚██████╔╝██║ ╚████║╚██████╔╝   ██║   
        ║     ╚═══╝  ╚═╝╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝    ╚═╝   
        ║                                                           ║
        ║            👁️  Vision-Based Web Automation                ║
        ║         "See what others can't. Automate what others do."  ║
        ╚═══════════════════════════════════════════════════════════╝
        """
        console.print(banner, style="cyan")
        console.print("🤖 Your AI-Powered Browser Assistant", style="green bold")
        console.print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n", style="dim")
    
    def show_menu(self):
        """منوی اصلی"""
        menu = Panel(
            """
            [bold cyan]📋 MAIN MENU[/bold cyan]
            
            [1] 🌐 Open Website
            [2] 👁️  Analyze Page
            [3] 🖱️  Click on Element
            [4] ⌨️  Type Text
            [5] 📋 Extract Data
            [6] 🎬 Run Automation Script
            [7] 🎮 Demo Mode (Hacker Experience)
            [8] 📈 Generate Report
            [9] ❌ Exit
            
            [dim]💡 Enter the number of your choice:[/dim]
            """,
            title="VisionBot v2.0",
            border_style="cyan"
        )
        console.print(menu)
        return Prompt.ask("[bold green]Select option[/bold green]")
    
    async def open_website(self):
        """باز کردن وب‌سایت"""
        url = Prompt.ask("[bold cyan]Enter URL[/bold cyan] (e.g., https://example.com)")
        
        console.print(f"\n[bold yellow]🌐 Opening {url}...[/bold yellow]")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("[cyan]Loading page...", total=100)
            
            # شبیه‌سازی بارگذاری
            for i in range(100):
                await asyncio.sleep(0.01)
                progress.update(task, advance=1)
            
            await self.browser.open(url)
            screenshot = await self.browser.screenshot()
            self.screenshots.append(screenshot)
        
        console.print("[bold green]✅ Page loaded![/bold green]")
        console.print("[dim]📸 Screenshot saved[/dim]")
        input("\n⏎ Press Enter to continue...")
    
    async def analyze_page(self):
        """تحلیل صفحه با هوش مصنوعی"""
        console.print("\n[bold yellow]👁️ Analyzing page with AI vision...[/bold yellow]")
        
        with console.status("[bold cyan]Capturing and analyzing..."):
            screenshot = await self.browser.screenshot()
            analysis = self.vision.analyze(screenshot)
            self.results.append(analysis)
        
        # نمایش نتایج به‌صورت زیبا
        table = Table(title="📊 Page Analysis", style="cyan")
        table.add_column("Element Type", style="green")
        table.add_column("Count", style="yellow")
        table.add_column("Coordinates", style="blue")
        
        for element in analysis.get('elements', []):
            table.add_row(
                element.get('type', 'Unknown'),
                str(element.get('count', 0)),
                element.get('position', 'N/A')
            )
        
        console.print(table)
        
        # نمایش المان‌های شناسایی‌شده
        console.print("\n[bold green]✅ Analysis complete![/bold green]")
        console.print(f"[dim]Found {len(analysis.get('elements', []))} interactive elements[/dim]")
        input("\n⏎ Press Enter to continue...")
    
    async def click_element(self):
        """کلیک روی المان با بینایی"""
        console.print("\n[bold yellow]🖱️ Click on element...[/bold yellow]")
        
        description = Prompt.ask("[bold cyan]Describe what to click[/bold cyan] (e.g., 'Login button')")
        
        with console.status("[bold cyan]Locating and clicking..."):
            screenshot = await self.browser.screenshot()
            coordinates = self.vision.locate_element(screenshot, description)
            
            if coordinates:
                await self.browser.click(coordinates)
                console.print("[bold green]✅ Clicked successfully![/bold green]")
            else:
                console.print("[bold red]❌ Element not found![/bold red]")
        
        input("\n⏎ Press Enter to continue...")
    
    async def type_text(self):
        """تایپ متن در یک فیلد"""
        console.print("\n[bold yellow]⌨️ Type text...[/bold yellow]")
        
        field_desc = Prompt.ask("[bold cyan]Describe the field[/bold cyan] (e.g., 'Username field')")
        text = Prompt.ask("[bold cyan]Enter text to type[/bold cyan]")
        
        with console.status("[bold cyan]Locating field and typing..."):
            screenshot = await self.browser.screenshot()
            coordinates = self.vision.locate_element(screenshot, field_desc)
            
            if coordinates:
                await self.browser.type_text(coordinates, text)
                console.print("[bold green]✅ Text typed![/bold green]")
            else:
                console.print("[bold red]❌ Field not found![/bold red]")
        
        input("\n⏎ Press Enter to continue...")
    
    async def extract_data(self):
        """استخراج داده از صفحه"""
        console.print("\n[bold yellow]📋 Extract data...[/bold yellow]")
        
        what = Prompt.ask("[bold cyan]What to extract?[/bold cyan] (e.g., 'All prices', 'Email addresses')")
        
        with console.status("[bold cyan]Extracting..."):
            screenshot = await self.browser.screenshot()
            data = self.vision.extract(screenshot, what)
        
        console.print("[bold green]✅ Extraction complete![/bold green]")
        console.print(f"[dim]Data: {data}[/dim]")
        input("\n⏎ Press Enter to continue...")
    
    async def run_script(self):
        """اجرای اسکریپت خودکار"""
        console.print("\n[bold yellow]🎬 Running automation script...[/bold yellow]")
        
        script_code = Prompt.ask("[bold cyan]Enter script name[/bold cyan] (e.g., 'demo_login')")
        
        try:
            # بارگذاری و اجرای اسکریپت
            script = __import__(f"examples.{script_code}", fromlist=["run"])
            await script.run(self.browser, self.vision)
            console.print("[bold green]✅ Script executed successfully![/bold green]")
        except Exception as e:
            console.print(f"[bold red]❌ Error: {e}[/bold red]")
        
        input("\n⏎ Press Enter to continue...")
    
    async def demo_mode(self):
        """حالت دمو با افکت‌های سینمایی"""
        console.clear()
        console.print("[bold green]🎬 VisionBot Demo Mode[/bold green]\n")
        
        # افکت ماتریکس
        matrix_rain(console, duration=3)
        
        # تایپ هکری
        hacker_typing(console, "INITIALIZING VISION SYSTEM...")
        time.sleep(0.5)
        hacker_typing(console, "LOADING AI MODEL...")
        time.sleep(0.5)
        hacker_typing(console, "OPENING BROWSER...")
        time.sleep(0.5)
        hacker_typing(console, "ANALYZING PAGE ELEMENTS...")
        time.sleep(0.5)
        hacker_typing(console, "FOUND 15 INTERACTIVE ELEMENTS")
        time.sleep(0.5)
        hacker_typing(console, "CLICKING 'LOGIN' BUTTON...")
        time.sleep(0.5)
        hacker_typing(console, "TYPING CREDENTIALS...")
        time.sleep(0.5)
        hacker_typing(console, "✅ AUTOMATION COMPLETE!")
        
        glow_effect(console, "🔐 ACCESS GRANTED")
        
        console.print("\n[bold green]✅ Demo completed![/bold green]")
        console.print("[dim]Use the main menu to run real automations.[/dim]")
        input("\n⏎ Press Enter to continue...")
    
    async def generate_report(self):
        """تولید گزارش تصویری"""
        console.print("\n[bold yellow]📄 Generating report...[/bold yellow]")
        
        with console.status("[bold cyan]Creating visual report..."):
            reporter = HTMLReporter()
            filename = f"visionbot_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
            reporter.generate(self.results, self.screenshots, filename)
        
        console.print(f"[bold green]✅ Report saved: {filename}[/bold green]")
        console.print("[dim]Open the file in your browser to view the dashboard.[/dim]")
        input("\n⏎ Press Enter to continue...")
    
    async def run(self):
        """حلقه‌ی اصلی"""
        while True:
            console.clear()
            self.show_banner()
            choice = self.show_menu()
            
            if choice == "1":
                await self.open_website()
            elif choice == "2":
                await self.analyze_page()
            elif choice == "3":
                await self.click_element()
            elif choice == "4":
                await self.type_text()
            elif choice == "5":
                await self.extract_data()
            elif choice == "6":
                await self.run_script()
            elif choice == "7":
                await self.demo_mode()
            elif choice == "8":
                await self.generate_report()
            elif choice == "9":
                console.print("[bold red]👋 Goodbye! Stay visionary.[/bold red]")
                break
            else:
                console.print("[bold red]❌ Invalid choice![/bold red]")
                await asyncio.sleep(1)

def main():
    """نقطه‌ی ورود"""
    cli = VisionBotCLI()
    asyncio.run(cli.run())

if __name__ == "__main__":
    main()
