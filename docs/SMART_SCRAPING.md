# 🧠 Smart Scraping Architecture

## Intelligent Two-Phase Web Research Pipeline

Instead of blindly scraping random websites, EchoDuo now uses an intelligent agent workflow:

```
┌─────────────────────────────────────────────────────────────┐
│                  SMART SCRAPING PIPELINE                     │
└─────────────────────────────────────────────────────────────┘

   USER TOPIC
       ↓
   ┌───────────────────────────────────────────┐
   │  PHASE 1: Claude Analysis Agent           │
   │  "Which websites have the BEST data?"     │
   └───────────────────────────────────────────┘
       ↓
   Target Selection:
   • Identifies 3 specific URLs
   • Explains WHY each is valuable
   • Considers: news, research, data sources
       ↓
   ┌───────────────────────────────────────────┐
   │  PHASE 2: Lightpanda Fetch Agent          │
   │  "Get the actual data from those sites"   │
   └───────────────────────────────────────────┘
       ↓
   Real Data Extraction:
   • Scrapes identified targets
   • Extracts article content
   • Handles JavaScript rendering
       ↓
   ┌───────────────────────────────────────────┐
   │  PHASE 3: Claude Synthesis Agent          │
   │  "Turn raw data into podcast context"     │
   └───────────────────────────────────────────┘
       ↓
   PODCAST CONTEXT
   • Statistics + Headlines + Insights
   • Ready for conversation generation
```

---

## Why This Is Better

### Old Way (Blind Scraping):
```python
# Just search and hope
search_results = google_search(topic)
content = scrape(search_results[0])  # Whatever comes first
```

**Problems:**
- ❌ Random source quality
- ❌ Might get irrelevant pages
- ❌ No understanding of WHAT data is needed
- ❌ Wastes API calls on bad sources

### New Way (Intelligent Agent Pipeline):
```python
# Claude thinks first
targets = claude.identify_best_sources(topic)
# → TechCrunch for tech news
# → Statista for statistics  
# → Research papers for data

# Then scrape intelligently
data = lightpanda.scrape(targets)

# Then synthesize
context = claude.synthesize(data, topic)
```

**Benefits:**
- ✅ High-quality, relevant sources
- ✅ Targeted data extraction
- ✅ Understands context needs
- ✅ Efficient API usage

---

## Example: AI Agents Topic

### Phase 1: Claude Identifies Targets

```json
[
  {
    "url": "https://techcrunch.com/ai-agents-2024",
    "source_name": "TechCrunch",
    "reason": "Breaking news on AI agent platforms and launches",
    "expected_content": "Recent company announcements, funding, product releases"
  },
  {
    "url": "https://arxiv.org/recent/cs.AI",
    "source_name": "ArXiv",
    "reason": "Latest research papers on autonomous agents",
    "expected_content": "Academic research, benchmarks, technical advances"
  },
  {
    "url": "https://www.statista.com/ai-adoption-2024",
    "source_name": "Statista",
    "reason": "Statistics on AI agent adoption rates",
    "expected_content": "Market data, adoption percentages, growth metrics"
  }
]
```

### Phase 2: Lightpanda Fetches

```
[Lightpanda] Scraping TechCrunch...
✅ Retrieved: "Anthropic launches Claude Agents platform... 
    340% growth in agent frameworks..."

[Lightpanda] Scraping ArXiv...
✅ Retrieved: "Autonomous agents achieve 92% task completion 
    in complex environments..."

[Lightpanda] Scraping Statista...
✅ Retrieved: "AI agent market size: $4.2B in 2024, 
    projected $28B by 2028..."
```

### Phase 3: Claude Synthesizes

**Output:**
> "AI agent frameworks saw 340% growth in 2024, with autonomous systems 
> now handling 28% of customer service interactions. Recent research 
> shows agents achieving 92% task completion in complex environments, 
> while the market is projected to grow from $4.2B to $28B by 2028."

**This becomes the context for the podcast conversation!**

---

## Implementation

### 1. Enable Smart Scraping

```python
from podcast_generator import PodcastGenerator

# Enable smart scraping (default)
generator = PodcastGenerator(use_smart_scraping=True)

# Or disable (use old method)
generator = PodcastGenerator(use_smart_scraping=False)
```

### 2. Direct Usage

```python
from smart_scraper import SmartScraper

scraper = SmartScraper()
result = scraper.get_intelligent_context("AI trends 2024")

print(result['context'])  # Synthesized context
print(result['sources'])  # Claude's target selection
print(result['scraped_data'])  # Lightpanda results
```

### 3. Test It

```bash
python test_smart_scraping.py
```

---

## Configuration

### Requirements

```python
# Required
ANTHROPIC_API_KEY=sk-ant-...  # For Claude analysis

# Optional but recommended
LIGHTPANDA_API_KEY=...  # For real scraping
```

### Fallback Behavior

**With Lightpanda:**
```
Phase 1: Claude → Phase 2: Lightpanda → Phase 3: Claude
```

**Without Lightpanda:**
```
Phase 1: Claude → Phase 2: Claude (synthesizes expected data) → Phase 3: Claude
```

Both work! But Lightpanda gives REAL data.

---

## Benefits for Autonomous Agents

This architecture demonstrates **agent orchestration**:

1. **Planning Agent** (Claude) - Decides what data is needed
2. **Execution Agent** (Lightpanda) - Fetches the data
3. **Synthesis Agent** (Claude) - Processes for downstream use

Each agent has a specific role and hands off to the next.

**This is how autonomous systems actually work.**

---

## Cost Considerations

### Smart Scraping:
- Claude calls: 2-3 per episode (~$0.02)
- Lightpanda calls: 3 per episode (~$0.15)
- **Total: ~$0.17 per episode**

### Old Scraping:
- Random web scraping: Free but unreliable
- Often requires multiple retries
- Lower quality data

**Worth the extra cost for reliable, targeted data!**

---

## Next Steps

1. ✅ **Test smart scraping**: `python test_smart_scraping.py`
2. ✅ **Add Lightpanda key**: For real data fetching
3. ✅ **Generate podcast**: Will automatically use smart scraping
4. ✅ **Monitor logs**: See each phase in action

---

## Future Enhancements

- [ ] Cache successful sources (Redis)
- [ ] Learn from failed scrapes
- [ ] Dynamic source quality scoring
- [ ] Parallel scraping for speed
- [ ] Source credibility checking

---

**This is autonomous AI research in action! 🚀**

