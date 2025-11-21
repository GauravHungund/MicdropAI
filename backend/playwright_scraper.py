"""
Playwright-based web scraper using Chrome for JavaScript rendering.
Solves the issue with JavaScript-heavy websites (SPAs).
"""

import asyncio
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout
from bs4 import BeautifulSoup
from typing import Dict, Optional, Any


class PlaywrightScraper:
    """
    Web scraper using Playwright + Chrome.
    Renders JavaScript just like a real browser.
    """
    
    def __init__(self, headless: bool = True, timeout: int = 30000):
        """
        Initialize Playwright scraper.
        
        Args:
            headless: Run browser in headless mode
            timeout: Page load timeout in milliseconds
        """
        self.headless = headless
        self.timeout = timeout
        self.browser = None
        self.context = None
    
    async def __aenter__(self):
        """Async context manager entry."""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=self.headless)
        self.context = await self.browser.new_context(
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if hasattr(self, 'playwright'):
            await self.playwright.stop()
    
    async def scrape_url(self, url: str, wait_time: float = 5.0, wait_for_selector: Optional[str] = None) -> Dict[str, Any]:
        """
        Scrape a URL with JavaScript rendering.
        
        Args:
            url: URL to scrape
            wait_time: Time to wait after page load (seconds) - increased for JS-heavy sites
            wait_for_selector: Optional CSS selector to wait for
            
        Returns:
            Dictionary with status and content
        """
        if not self.context:
            raise RuntimeError("Scraper not initialized. Use 'async with PlaywrightScraper() as scraper:'")
        
        try:
            # Create a new page
            page = await self.context.new_page()
            
            # Navigate to URL
            print(f"      → Navigating with Chrome...")
            try:
                # Wait for networkidle, then load state for maximum JS rendering
                await page.goto(url, wait_until='networkidle', timeout=self.timeout)
                await page.wait_for_load_state('networkidle')  # Extra wait for JS
            except PlaywrightTimeout:
                print(f"      ⚠️  Network idle timeout, but page may have loaded")
                await page.wait_for_load_state('domcontentloaded')
                await page.wait_for_load_state('load')  # Wait for full page load
            
            # Wait for specific selector if provided
            if wait_for_selector:
                try:
                    await page.wait_for_selector(wait_for_selector, timeout=5000)
                except PlaywrightTimeout:
                    print(f"      ⚠️  Selector not found, continuing anyway")
            
            # Additional wait for JavaScript to execute
            if wait_time > 0:
                print(f"      → Waiting {wait_time}s for JavaScript...")
                await asyncio.sleep(wait_time)
            
            # Get page content
            print(f"      → Extracting rendered content...")
            html_content = await page.content()
            
            # Close the page
            await page.close()
            
            # Parse with BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Remove unwanted elements
            for element in soup(['script', 'style', 'nav', 'footer', 'header', 'aside']):
                element.decompose()
            
            # Extract main content
            main_content = (
                soup.find('article') or 
                soup.find('main') or 
                soup.find('div', class_=['content', 'article', 'post']) or
                soup.body
            )
            
            if main_content:
                text = main_content.get_text(separator=' ', strip=True)
                text = ' '.join(text.split())
                
                return {
                    "status": "success",
                    "content": text,
                    "length": len(text),
                    "url": url,
                    "method": "playwright_chrome"
                }
            
            # Fallback: use body text
            if soup.body:
                text = soup.body.get_text(separator=' ', strip=True)
                text = ' '.join(text.split())
                
                if len(text) > 100:  # Minimum content threshold
                    return {
                        "status": "success",
                        "content": text,
                        "length": len(text),
                        "url": url,
                        "method": "playwright_chrome"
                    }
            
            return {
                "status": "error",
                "error": "No content found",
                "url": url
            }
            
        except PlaywrightTimeout:
            return {
                "status": "error",
                "error": f"Timeout after {self.timeout}ms",
                "url": url
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "url": url
            }


def scrape_with_playwright(url: str, wait_time: float = 5.0) -> Dict[str, Any]:
    """
    Synchronous wrapper for scraping with Playwright.
    
    Args:
        url: URL to scrape
        wait_time: Time to wait after page load (seconds) - increased for JS-heavy sites
        
    Returns:
        Dictionary with status and content
    """
    async def _scrape():
        async with PlaywrightScraper(headless=True) as scraper:
            return await scraper.scrape_url(url, wait_time=wait_time)
    
    # Run async function
    try:
        return asyncio.run(_scrape())
    except Exception as e:
        return {
            "status": "failed",
            "error": str(e)
        }


if __name__ == "__main__":
    # Test the scraper
    test_urls = [
        "https://www.technologyreview.com/topic/artificial-intelligence/",
        "https://news.ycombinator.com/",
        "https://www.nature.com/subjects/artificial-intelligence"
    ]
    
    print("🧪 Testing Playwright Chrome Scraper\n")
    
    for url in test_urls:
        print(f"\n{'='*70}")
        print(f"Testing: {url}")
        print('='*70)
        
        result = scrape_with_playwright(url, wait_time=5.0)
        
        if result["status"] == "success":
            print(f"\n✅ SUCCESS!")
            print(f"   Content length: {result['length']:,} characters")
            print(f"   Method: {result['method']}")
            print(f"   Preview: {result['content'][:300]}...")
        else:
            print(f"\n❌ FAILED: {result.get('error', 'Unknown error')}")

