"""
Lightpanda Cloud + Playwright integration via CDP (Chrome DevTools Protocol).
Uses Playwright's CDP.connect() to connect to Lightpanda Cloud WebSocket.
"""

import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from typing import Dict, Optional, Any
import os
from dotenv import load_dotenv


class LightpandaPlaywrightClient:
    """
    Client that connects Playwright to Lightpanda Cloud via CDP.
    """
    
    def __init__(self, api_token: str, region: str = "eu"):
        """
        Initialize Lightpanda Cloud client via Playwright CDP.
        
        Args:
            api_token: Your Lightpanda Cloud API token
            region: 'eu' for Europe or 'us' for United States
        """
        self.api_token = api_token
        
        # Build WebSocket CDP endpoint
        if region == "eu":
            self.cdp_url = f"wss://euwest.cloud.lightpanda.io/ws?token={api_token}"
        elif region == "us":
            self.cdp_url = f"wss://uswest.cloud.lightpanda.io/ws?token={api_token}"
        else:
            raise ValueError(f"Invalid region: {region}. Must be 'eu' or 'us'")
        
        self.region = region
        self.playwright = None
        self.browser = None
        self.context = None
    
    async def __aenter__(self):
        """Async context manager entry."""
        self.playwright = await async_playwright().start()
        
        # Connect to Lightpanda Cloud via CDP
        print(f"      → Connecting to Lightpanda Cloud ({self.region.upper()}) via CDP...")
        try:
            self.browser = await self.playwright.chromium.connect_over_cdp(
                self.cdp_url,
                timeout=30000
            )
            print(f"      ✅ Connected to Lightpanda Cloud!")
            
            # Get or create context
            contexts = self.browser.contexts
            if contexts:
                self.context = contexts[0]
            else:
                self.context = await self.browser.new_context(
                    user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
                )
            
            return self
            
        except Exception as e:
            print(f"      ❌ CDP connection failed: {e}")
            raise
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
    
    async def scrape_url(self, url: str, wait_time: float = 5.0) -> Dict[str, Any]:
        """
        Scrape a URL using Lightpanda Cloud browser via Playwright.
        
        Args:
            url: URL to scrape
            wait_time: Time to wait after page load (seconds) - increased for JS-heavy sites
            
        Returns:
            Dictionary with status and content
        """
        if not self.context:
            raise RuntimeError("Not connected. Use 'async with' context manager.")
        
        try:
            # Create a new page
            page = await self.context.new_page()
            
            # Navigate to URL
            print(f"      → Navigating to {url[:60]}...")
            try:
                # Wait for networkidle, then load state for maximum JS rendering
                await page.goto(url, wait_until='networkidle', timeout=45000)
                await page.wait_for_load_state('networkidle')  # Extra wait for JS
            except Exception as e:
                print(f"      ⚠️  Network idle timeout, but page may have loaded")
                await page.wait_for_load_state('domcontentloaded')
                await page.wait_for_load_state('load')  # Wait for full page load
            
            # Wait for JavaScript to render
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
                    "method": "lightpanda_cloud_via_playwright_cdp"
                }
            
            # Fallback: use body text
            if soup.body:
                text = soup.body.get_text(separator=' ', strip=True)
                text = ' '.join(text.split())
                
                if len(text) > 100:
                    return {
                        "status": "success",
                        "content": text,
                        "length": len(text),
                        "url": url,
                        "method": "lightpanda_cloud_via_playwright_cdp"
                    }
            
            return {
                "status": "error",
                "error": "No content found",
                "url": url
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "url": url
            }


def scrape_with_lightpanda_playwright(url: str, api_token: str, region: str = "eu") -> Dict[str, Any]:
    """
    Synchronous wrapper for scraping with Lightpanda Cloud via Playwright CDP.
    
    Args:
        url: URL to scrape
        api_token: Lightpanda Cloud API token
        region: 'eu' or 'us'
        
    Returns:
        Dictionary with status and content
    """
    async def _scrape():
        async with LightpandaPlaywrightClient(api_token, region) as client:
            return await client.scrape_url(url, wait_time=5.0)
    
    # Run async function
    try:
        return asyncio.run(_scrape())
    except Exception as e:
        return {
            "status": "failed",
            "error": str(e)
        }


if __name__ == "__main__":
    # Test the client
    load_dotenv()
    
    api_token = os.getenv("LIGHTPANDA_API_KEY")
    if not api_token:
        print("❌ LIGHTPANDA_API_KEY not found in .env")
        exit(1)
    
    test_urls = [
        "https://www.technologyreview.com/topic/artificial-intelligence/",
        "https://news.ycombinator.com/"
    ]
    
    print("🧪 Testing Lightpanda Cloud via Playwright CDP\n")
    
    for url in test_urls:
        print(f"\n{'='*70}")
        print(f"Testing: {url}")
        print('='*70)
        
        result = scrape_with_lightpanda_playwright(url, api_token, region="eu")
        
        if result["status"] == "success":
            print(f"\n✅ SUCCESS!")
            print(f"   Content length: {result['length']:,} characters")
            print(f"   Method: {result['method']}")
            print(f"   Preview: {result['content'][:300]}...")
        else:
            print(f"\n❌ FAILED: {result.get('error', 'Unknown error')}")

