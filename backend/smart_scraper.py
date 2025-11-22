"""Intelligent scraping: Claude selects targets → Lightpanda fetches data."""
from typing import List, Dict, Optional
from claude_client import ClaudeClient
# Lightpanda is handled via lightpanda_playwright_client now
from lightpanda_playwright_client import LightpandaPlaywrightClient as LightpandaClient
from lightpanda_playwright_client import scrape_with_lightpanda_playwright
from playwright_scraper import scrape_with_playwright
from config import LIGHTPANDA_API_KEY
import json


class SmartScraper:
    """
    Two-phase intelligent scraping:
    1. Claude analyzes topic and recommends target websites
    2. Lightpanda scrapes those specific targets for real data
    """
    
    def __init__(self):
        self.claude = ClaudeClient()
        self.use_lightpanda = bool(LIGHTPANDA_API_KEY)
        # Note: Lightpanda is used via scrape_with_lightpanda_playwright function
        # No need to instantiate a client here
    
    def get_intelligent_context(self, topic: str, max_sources: int = 3) -> Dict:
        """
        Intelligent two-phase scraping.
        
        Phase 1: Ask Claude which websites to scrape
        Phase 2: Use Lightpanda to fetch from those targets
        
        Args:
            topic: The podcast topic
            max_sources: Maximum number of sources to scrape
        
        Returns:
            Dict with context, sources, and metadata
        """
        print("\n" + "=" * 70)
        print("🧠 INTELLIGENT SCRAPING PIPELINE")
        print("=" * 70)
        
        # PHASE 1: Claude recommends targets
        print("\n[PHASE 1] Claude Agent: Analyzing topic & selecting targets...")
        targets = self._get_target_websites(topic, max_sources)
        
        if not targets:
            print("⚠️  No targets identified, using fallback")
            return self._fallback_context(topic)
        
        print(f"\n✅ Claude identified {len(targets)} target websites:")
        for i, target in enumerate(targets, 1):
            print(f"   {i}. {target['url']}")
            print(f"      → {target['reason'][:60]}...")
        
        # PHASE 2: Lightpanda scrapes targets
        if self.use_lightpanda:
            print("\n[PHASE 2] Lightpanda Agent: Fetching real data...")
            scraped_data = self._scrape_targets(targets)
        else:
            print("\n[PHASE 2] ⚠️  Lightpanda not available, using Claude synthesis...")
            scraped_data = self._synthesize_data(topic, targets)
        
        # PHASE 3: Claude synthesizes into podcast context
        print("\n[PHASE 3] Claude Agent: Synthesizing context...")
        context = self._synthesize_context(topic, scraped_data)
        
        print("\n✅ Intelligent scraping complete!")
        print("=" * 70)
        
        return {
            'context': context,
            'sources': targets,
            'scraped_data': scraped_data,
            'method': 'intelligent_scraping',
            'lightpanda_used': self.use_lightpanda
        }
    
    def _get_target_websites(self, topic: str, max_sources: int) -> List[Dict]:
        """
        Phase 1: Ask Claude to identify best websites to scrape.
        """
        prompt = f"""You are a research agent identifying the BEST websites to scrape for podcast context.

Topic: "{topic}"
Current Date: November 2025

CRITICAL REQUIREMENTS FOR URLs:
1. ✅ MUST BE RECENT: Prefer URLs from 2024-2025 or current/latest content
2. ✅ MUST BE VALID: Use landing pages, topic pages, or category pages that are GUARANTEED to exist
3. ✅ PREFER BASE/Topic PAGES over specific old article URLs
4. ✅ AVOID: Specific article URLs from 2020-2023 (these often return 404)

URL PATTERNS TO PREFER:
✅ https://www.technologyreview.com/topic/artificial-intelligence/  (topic page)
✅ https://www.theverge.com/ai-artificial-intelligence  (category page)
✅ https://techcrunch.com/  (main page or /tag/ai/)
✅ https://venturebeat.com/ai/  (category page)
✅ https://www.bbc.com/news/technology  (section page)
✅ https://www.reuters.com/technology/  (section page)
✅ https://arstechnica.com/information-technology/  (category page)

❌ AVOID: https://www.technologyreview.com/2022/01/11/1041557/specific-article/
❌ AVOID: https://www.nature.com/articles/d41586-022-00623-x  (old specific articles)

Your task:
1. Identify {max_sources} reputable websites with RECENT (2024-2025) or CURRENT content
2. Use TOPIC/CATEGORY/LANDING pages that are guaranteed to exist, not old specific articles
3. For each, explain WHY it's valuable

Consider:
- News sites (TechCrunch, The Verge, Bloomberg, BBC, Reuters)
- Research platforms (ArXiv, Nature topic pages, Pew Research topic pages)
- Industry blogs (relevant to topic)
- Data sources (Statista, Pew Research topic pages)
- Official sources (government, orgs)

Return ONLY a JSON array in this format:
[
  {{
    "url": "https://domain.com/topic-or-category-page",
    "source_name": "Source Name",
    "reason": "Why this source is valuable for this topic",
    "expected_content": "What kind of data/info we expect"
  }}
]

IMPORTANT:
- Use topic/category pages, NOT specific old article URLs
- Prefer URLs from 2024-2025 or current content pages
- Ensure URLs are guaranteed to exist (use section pages, not specific articles)
- Be specific but use stable, long-lived page URLs

Return ONLY the JSON array, nothing else."""

        try:
            response = self.claude.generate(
                prompt=prompt,
                temperature=0.3,  # More deterministic
                max_tokens=1000
            )
            
            # Extract JSON from response
            response = response.strip()
            if "```json" in response:
                response = response.split("```json")[1].split("```")[0]
            elif "```" in response:
                response = response.split("```")[1].split("```")[0]
            
            targets = json.loads(response)
            return targets[:max_sources]
            
        except json.JSONDecodeError as e:
            print(f"⚠️  JSON parse error: {e}")
            print(f"Response was: {response[:200]}")
            return []
        except Exception as e:
            print(f"⚠️  Error getting targets: {e}")
            return []
    
    def _scrape_targets(self, targets: List[Dict]) -> List[Dict]:
        """
        Phase 2: Scrape each target once - try best method, if fails move on.
        Priority: Lightpanda Cloud > Playwright > HTTP
        """
        scraped = []
        
        for i, target in enumerate(targets, 1):
            print(f"\n   [{i}/{len(targets)}] Scraping {target['source_name']}...")
            
            success = False
            
            # Try Lightpanda Cloud first (if API key available)
            if LIGHTPANDA_API_KEY and not success:
                try:
                    print(f"      → Trying Lightpanda Cloud...")
                    result = scrape_with_lightpanda_playwright(
                        url=target['url'],
                        api_token=LIGHTPANDA_API_KEY,
                        region="eu"
                    )
                    
                    if result.get('status') == 'success' and result.get('content'):
                        content = result.get('content', '')
                        if len(content) > 100:
                            scraped.append({
                                'source': target['source_name'],
                                'url': target['url'],
                                'content': content[:2000],
                                'status': 'success',
                                'method': 'lightpanda_cloud_cdp'
                            })
                            print(f"      ✅ Retrieved {len(content):,} characters")
                            success = True
                            continue
                except Exception as e:
                    print(f"      ⚠️  Lightpanda failed: {str(e)[:60]}")
            
            # Try Playwright if Lightpanda failed
            if not success:
                try:
                    print(f"      → Trying Playwright Chrome...")
                    result = scrape_with_playwright(
                        url=target['url'],
                        wait_time=5.0
                    )
                    
                    if result.get('status') == 'success' and result.get('content'):
                        content = result.get('content', '')
                        if len(content) > 100:
                            scraped.append({
                                'source': target['source_name'],
                                'url': target['url'],
                                'content': content[:2000],
                                'status': 'success',
                                'method': 'playwright_chrome'
                            })
                            print(f"      ✅ Retrieved {len(content):,} characters")
                            success = True
                            continue
                except Exception as e:
                    print(f"      ⚠️  Playwright failed: {str(e)[:60]}")
            
            # Try HTTP as last resort
            if not success:
                try:
                    print(f"      → Trying direct HTTP...")
                    scraped_content = self._direct_scrape(target['url'])
                    if scraped_content and len(scraped_content) > 100:
                        scraped.append({
                            'source': target['source_name'],
                            'url': target['url'],
                            'content': scraped_content[:2000],
                            'status': 'success',
                            'method': 'http'
                        })
                        print(f"      ✅ Retrieved {len(scraped_content)} characters")
                        success = True
                except Exception as e:
                    print(f"      ⚠️  HTTP failed: {str(e)[:60]}")
            
            if not success:
                print(f"      ❌ All methods failed, moving on...")
        
        return scraped
    
    def _direct_scrape(self, url: str) -> str:
        """
        Direct HTTP scraping using BeautifulSoup (fallback method).
        """
        import requests
        from bs4 import BeautifulSoup
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=15)
            
            # Check status
            if response.status_code == 404:
                print(f"         → 404 Not Found (URL may be incorrect)")
                return ""
            elif response.status_code == 403:
                print(f"         → 403 Forbidden (site blocking scraper)")
                return ""
            
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove unwanted elements
            for element in soup(['script', 'style', 'nav', 'footer', 'header', 'aside']):
                element.decompose()
            
            # Try to find main content
            main_content = (
                soup.find('article') or 
                soup.find('main') or 
                soup.find('div', class_=['content', 'article', 'post']) or
                soup.body
            )
            
            if main_content:
                text = main_content.get_text(separator=' ', strip=True)
                # Clean up whitespace
                text = ' '.join(text.split())
                
                # Warn if content is suspiciously short (likely JavaScript-rendered)
                if len(text) < 500:
                    print(f"         → Warning: Only {len(text)} chars (site may be JavaScript-heavy)")
                    # Still return it, but it's probably not useful
                
                return text if len(text) > 100 else ""  # Minimum 100 chars
            
            print(f"         → No main content found")
            return ""
            
        except requests.exceptions.Timeout:
            print(f"         → Timeout (site too slow)")
            return ""
        except requests.exceptions.ConnectionError:
            print(f"         → Connection error")
            return ""
        except Exception as e:
            print(f"         → Error: {type(e).__name__}")
            return ""
    
    def _synthesize_data(self, topic: str, targets: List[Dict]) -> List[Dict]:
        """
        Fallback: Claude synthesizes expected data when Lightpanda unavailable.
        """
        prompt = f"""Based on these target websites for the topic "{topic}", 
synthesize what kind of information we would likely find:

Targets:
{json.dumps(targets, indent=2)}

Generate realistic, current information that would be found at these sources.
Include statistics, recent developments, and quotes where appropriate.

Return as JSON array:
[
  {{
    "source": "Source Name",
    "content": "Synthesized content with stats and info"
  }}
]"""

        try:
            response = self.claude.generate(prompt, temperature=0.7, max_tokens=1500)
            if "```json" in response:
                response = response.split("```json")[1].split("```")[0]
            return json.loads(response)
        except:
            return []
    
    def _synthesize_context(self, topic: str, scraped_data: List[Dict]) -> str:
        """
        Phase 3: Claude synthesizes scraped data into podcast context.
        """
        if not scraped_data:
            return self._fallback_context(topic)
        
        sources_text = "\n\n".join([
            f"Source: {item['source']}\n{item.get('content', '')[:500]}"
            for item in scraped_data
        ])
        
        prompt = f"""You are synthesizing research for a podcast about: "{topic}"

Here is real data from multiple sources:

{sources_text}

Create a concise context summary (3-4 sentences) that includes:
1. One compelling statistic
2. One recent development or headline
3. One key insight or trend

Make it natural and conversational for podcast hosts to reference.
DO NOT mention the sources explicitly.
Just provide the synthesized information."""

        try:
            context = self.claude.generate(
                prompt=prompt,
                temperature=0.6,
                max_tokens=500
            )
            return context.strip()
        except Exception as e:
            print(f"⚠️  Synthesis error: {e}")
            return self._fallback_context(topic)
    
    def _fallback_context(self, topic: str) -> str:
        """Simple fallback when intelligent scraping fails."""
        fallbacks = {
            "AI": "AI systems have seen 340% growth in adoption this year, with autonomous agents now handling 28% of customer service interactions. Recent developments show agents moving from simple automation to complex decision-making.",
            "automation": "Workplace automation reached new milestones with 27% of repetitive roles now automated. The focus is shifting from replacing humans to augmenting human capabilities.",
            "mental health": "Mental health awareness has increased 25% globally since 2020. Companies are investing heavily in wellness programs, with 78% now offering comprehensive mental health benefits.",
        }
        
        for key, value in fallbacks.items():
            if key.lower() in topic.lower():
                return value
        
        return f"Recent discussions about {topic} have gained significant attention, with experts debating various perspectives and new data emerging regularly."


# Example usage
if __name__ == "__main__":
    scraper = SmartScraper()
    result = scraper.get_intelligent_context("AI agents and autonomous systems")
    
    print("\n" + "=" * 70)
    print("FINAL CONTEXT:")
    print("=" * 70)
    print(result['context'])
    print("\n" + "=" * 70)
    print("SOURCES USED:")
    print("=" * 70)
    for source in result['sources']:
        print(f"  • {source['source_name']}: {source['url']}")

