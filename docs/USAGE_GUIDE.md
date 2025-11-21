# 📖 EchoDuo Usage Guide

Complete guide to using EchoDuo for podcast generation.

## Table of Contents

1. [Basic Usage](#basic-usage)
2. [Advanced Options](#advanced-options)
3. [API Usage](#api-usage)
4. [Web Interface](#web-interface)
5. [Batch Generation](#batch-generation)
6. [Memory Management](#memory-management)
7. [Best Practices](#best-practices)
8. [Troubleshooting](#troubleshooting)

## Basic Usage

### Generate a Simple Podcast

```bash
python echoduo.py "artificial intelligence and creativity"
```

Output:
```
🎙️  ECHODUO - AI Podcast Generator
════════════════════════════════════════════════════════════

🌍 Gathering real-world context about: artificial intelligence and creativity
🎯 Selected sponsor: Notion
📝 Context snippet: Recent developments in AI art generation...

🎙️  Generating conversation...
🧠 Self-improving conversation...

════════════════════════════════════════════════════════════
🎧 FINAL PODCAST
════════════════════════════════════════════════════════════

Alex: Have you seen these AI-generated art pieces winning competitions?

Maya: Yeah, and the controversy is fascinating...
[... conversation continues ...]

════════════════════════════════════════════════════════════
✨ Episode Info:
   Topic: artificial intelligence and creativity
   Sponsor: Notion
════════════════════════════════════════════════════════════
```

## Advanced Options

### Provide Custom Context

Instead of web scraping, provide your own context:

```bash
python echoduo.py "quantum computing" \
  --context "IBM's new quantum processor has 1000+ qubits. Google claims quantum advantage in specific tasks."
```

**Use case:** When you have specific data or want to control the information included.

### Force a Specific Sponsor

```bash
python echoduo.py "developer productivity" --sponsor Coder
```

**Available sponsors:**
- `Calm` - Mental health, meditation, wellness
- `Nike` - Fitness, sports, motivation
- `Notion` - Productivity, organization, knowledge management
- `Coder` - Developer tools, programming platforms
- `Forethought` - AI automation, customer service
- `Skyflow` - Data privacy, security, compliance

### Combine Options

```bash
python echoduo.py "startup funding strategies" \
  --context "2024 saw 35% drop in Series A funding. Angels focusing on profitability over growth." \
  --sponsor Notion
```

## API Usage

### Start the API Server

```bash
python api.py
```

Server starts on `http://localhost:5000`

### API Endpoints

#### Generate Podcast

```bash
curl -X POST http://localhost:5000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "sustainable fashion",
    "context": "Fast fashion industry produces 10% of global carbon emissions",
    "sponsor": "Nike"
  }'
```

Response:
```json
{
  "success": true,
  "data": {
    "conversation": "Alex: ...\nMaya: ...",
    "sponsor": "Nike",
    "topic": "sustainable fashion",
    "context_snippet": "Fast fashion industry..."
  }
}
```

#### Check Memory State

```bash
curl http://localhost:5000/memory
```

Response:
```json
{
  "success": true,
  "data": {
    "recent_sponsors": ["Nike", "Calm", "Notion"],
    "recent_phrases": ["I've been thinking", "That's interesting"],
    "tone_patterns": ["sustainable-fashion-Nike"]
  }
}
```

#### Clear Memory

```bash
curl -X POST http://localhost:5000/memory/clear
```

#### List Sponsors

```bash
curl http://localhost:5000/sponsors
```

#### Health Check

```bash
curl http://localhost:5000/health
```

### Python API Client Example

```python
import requests

# Generate podcast
response = requests.post('http://localhost:5000/generate', json={
    'topic': 'blockchain technology',
    'sponsor': 'Skyflow'
})

data = response.json()
if data['success']:
    print(data['data']['conversation'])
    print(f"Sponsor: {data['data']['sponsor']}")
```

## Web Interface

### Start the Web Interface

1. Start the API server:
   ```bash
   python api.py
   ```

2. Open `web_interface.html` in your browser

3. Fill in the form:
   - **Topic** (required): Main subject of the podcast
   - **Context** (optional): Specific data or recent news
   - **Sponsor** (optional): Force a specific sponsor or let AI choose

4. Click "Generate Podcast 🎧"

5. Wait 30-60 seconds for generation

6. View your podcast conversation with highlighted speakers

### Web Interface Features

- 🎨 Beautiful, modern UI
- ⚡ Real-time generation progress
- 📱 Responsive design (works on mobile)
- 🎯 Auto-selects best sponsor if not specified
- 💾 Shows metadata (topic, sponsor used)

## Batch Generation

### Create a Batch Input File

`my_topics.json`:
```json
[
  {
    "topic": "AI in healthcare",
    "context": "AI diagnostics now match radiologist accuracy in 7 out of 10 cases"
  },
  {
    "topic": "plant-based nutrition",
    "sponsor": "Nike"
  },
  {
    "topic": "cybersecurity threats 2024"
  }
]
```

### Run Batch Generation

```bash
python batch_generator.py my_topics.json
```

With options:
```bash
python batch_generator.py my_topics.json \
  --output-dir my_episodes \
  --delay 5
```

### Batch Output

Generated files:
```
my_episodes/
├── episode_20241121_143022_AI_in_healthcare.json
├── episode_20241121_143115_plant-based_nutrition.json
├── episode_20241121_143208_cybersecurity_threats_2024.json
└── batch_summary_20241121_143210.json
```

Each episode file contains:
```json
{
  "conversation": "Alex: ...\nMaya: ...",
  "sponsor": "Forethought",
  "topic": "AI in healthcare",
  "context_used": "AI diagnostics now match...",
  "generated_at": "2024-11-21T14:30:22.123456",
  "batch_index": 1
}
```

### Use Example Batch

```bash
python batch_generator.py example_batch.json
```

## Memory Management

### View Current Memory

```bash
python echoduo.py --show-memory
```

Output:
```
🧠 Current Memory State:
Recent Sponsors: ['Nike', 'Calm', 'Notion', 'Coder']
Recent Phrases: ['I've been thinking about', "That's interesting", ...]
Tone Patterns: ['AI-healthcare-Forethought', 'plant-based-Nike']
```

### Clear Memory

```bash
python echoduo.py --clear-memory
```

**When to clear memory:**
- Starting a new podcast series with different tone
- Testing sponsor distribution
- After major changes to generation prompts
- When you want to allow recent sponsors again

### Memory Behavior

**Automatic Management:**
- Last 5 sponsors are excluded from selection
- Last 20 phrases are avoided in generation
- Oldest items automatically removed when limit reached
- Memory persists across sessions (with Redis)

**Without Redis:**
- Memory resets when program exits
- Still tracks within a session
- Great for testing or temporary use

## Best Practices

### Topic Selection

**Good topics:**
- ✅ "the ethics of AI in criminal justice"
- ✅ "remote work and mental health"
- ✅ "sustainable investing strategies"
- ✅ "the future of electric vehicles"

**Topics to avoid:**
- ❌ Too broad: "technology"
- ❌ Too narrow: "Python 3.12 walrus operator"
- ❌ One word: "blockchain"
- ❌ Questions: "is AI good or bad?"

**Optimal length:** 4-8 words describing a specific angle

### Providing Context

**Good context:**
```
"Recent study shows 74% of developers experience burnout. 
Stack Overflow survey reveals work-life balance as #1 priority. 
Companies with 4-day weeks report 40% less turnover."
```

**What to include:**
- Recent statistics
- New research findings
- Current events
- Expert opinions
- Contrasting viewpoints

**What to avoid:**
- Opinions without data
- Outdated information
- Too much detail (keep under 500 chars)

### Sponsor Selection

**Let AI choose when:**
- Topic clearly maps to one sponsor (mental health → Calm)
- You want optimal relevance
- Creating diverse content

**Force sponsor when:**
- You have sponsorship obligations
- Testing integration quality
- Rotating through all sponsors
- Creating themed content

### Generation Frequency

**Recommended:**
- 2-5 episodes per session
- 5-10 second delay between batch generations
- Clear memory after every 20-30 episodes

**Why:**
- Prevents phrase/pattern burnout
- Maintains conversation freshness
- Respects API rate limits

## Advanced Techniques

### Custom Host Personalities

Edit `podcast_generator.py`:

```python
system_prompt = """You are a master podcast script writer.

Your hosts are:
- Alex: [customize personality here]
- Maya: [customize personality here]
...
"""
```

### Adjust Conversation Length

In `podcast_generator.py`, modify the prompt:

```python
prompt = f"""...
The conversation should:
- Be 20-25 exchanges long  # Change this number
...
"""
```

### Control Creativity

Edit `claude_client.py` or pass different temperature:

```python
result = self.claude.generate(
    prompt=prompt,
    temperature=0.9,  # Higher = more creative (0.0-1.0)
    max_tokens=4000   # Longer conversations
)
```

### Multiple Conversations from One Topic

```bash
for i in {1..5}; do
  python echoduo.py "cryptocurrency regulation" --sponsor Skyflow
  sleep 10
done
```

Each will be slightly different due to:
- Random sampling (temperature > 0)
- Memory updates between runs
- Self-improvement variations

## Integration Examples

### Slack Bot

```python
from slack_sdk import WebClient
from podcast_generator import PodcastGenerator

generator = PodcastGenerator()

@app.event("app_mention")
def handle_mention(event, say):
    topic = extract_topic(event['text'])
    result = generator.generate(topic=topic)
    say(f"🎙️ New episode on {topic}!\n\n{result['conversation']}")
```

### Discord Bot

```python
import discord
from podcast_generator import PodcastGenerator

generator = PodcastGenerator()

@bot.command()
async def podcast(ctx, *, topic):
    await ctx.send(f"Generating podcast on: {topic}...")
    result = generator.generate(topic=topic)
    await ctx.send(result['conversation'])
```

### Scheduled Daily Episodes

```bash
# crontab -e
0 9 * * * cd /path/to/SF_AWS_HACK && python echoduo.py "$(date +\%A) tech news"
```

## Troubleshooting

### "Could not connect to Redis"

**Solution:** This is just a warning. System uses in-memory fallback automatically.

To fix permanently:
```bash
# Install Redis
brew install redis  # macOS
sudo apt install redis-server  # Linux

# Start Redis
brew services start redis  # macOS
sudo systemctl start redis  # Linux
```

### "Anthropic API Error"

**Solutions:**
1. Check `.env` has correct `ANTHROPIC_API_KEY`
2. Verify API key is valid at [Anthropic Console](https://console.anthropic.com/)
3. Check you have sufficient API credits
4. Ensure API key has proper permissions

### "Rate limit exceeded"

**Solution:** Add delays between requests:
```bash
python echoduo.py "topic 1"
sleep 30
python echoduo.py "topic 2"
```

Or in batch mode:
```bash
python batch_generator.py topics.json --delay 30
```

### Conversations feel repetitive

**Solutions:**
1. Clear memory: `python echoduo.py --clear-memory`
2. Increase temperature in `claude_client.py`
3. Provide more diverse topics
4. Add more varied context

### Sponsor mentions too obvious

**Solution:** The self-improvement loop should catch this, but you can:
1. Run generation again (randomness will vary output)
2. Adjust prompt in `podcast_generator.py` to emphasize subtlety
3. Check `example_output.txt` for natural integration examples

## Tips for Best Results

1. **Be Specific:** "AI in medical diagnosis" > "AI in healthcare"
2. **Provide Data:** Real statistics make conversations more credible
3. **Vary Topics:** Don't generate 10 episodes about the same subject in a row
4. **Monitor Memory:** Check memory state every 10-15 episodes
5. **Test Sponsors:** Try different sponsor/topic combinations
6. **Customize Hosts:** Adjust personalities to match your audience
7. **Iterate:** Generate multiple versions and pick the best
8. **Use Context:** Real-world context makes episodes more timely and relevant

## Getting Help

- **Documentation:** Check `README.md` and `ARCHITECTURE.md`
- **Examples:** See `example_output.txt` for quality benchmarks
- **Testing:** Run `python test_echoduo.py` to verify setup
- **Demo:** Try `python demo.py` for interactive walkthrough

---

Happy podcasting! 🎙️✨

**Version:** 1.0.0  
**Last Updated:** November 2025

