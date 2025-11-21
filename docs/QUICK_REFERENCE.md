# ⚡ EchoDuo Quick Reference

**One-page cheat sheet for EchoDuo commands and features**

## 🚀 Installation

```bash
pip install -r requirements.txt
cp env.example .env
# Edit .env with AWS credentials
./quickstart.sh  # Automated setup
```

## 📋 Basic Commands

### Generate Single Podcast
```bash
python echoduo.py "your topic here"
```

### With Options
```bash
python echoduo.py "topic" --context "stats and data" --sponsor Calm
```

### Memory Management
```bash
python echoduo.py --show-memory    # View state
python echoduo.py --clear-memory   # Reset
```

## 🎬 Demo & Testing

```bash
python demo.py              # Interactive demo
python test_echoduo.py      # Run tests
```

## 🌐 API Usage

### Start Server
```bash
python api.py
# Server runs on http://localhost:5000
```

### Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/generate` | Generate podcast |
| GET | `/memory` | View memory |
| POST | `/memory/clear` | Clear memory |
| GET | `/sponsors` | List sponsors |
| GET | `/health` | Health check |

### Example Request
```bash
curl -X POST http://localhost:5000/generate \
  -H "Content-Type: application/json" \
  -d '{"topic":"AI ethics","sponsor":"Notion"}'
```

## 📦 Batch Generation

```bash
# Create topics.json with array of topics
python batch_generator.py topics.json
python batch_generator.py topics.json --output-dir my_podcasts --delay 5
```

## 🎨 Web Interface

1. Start API: `python api.py`
2. Open `web_interface.html` in browser
3. Fill form and generate

## 🎯 Available Sponsors

| Sponsor | Best For |
|---------|----------|
| Calm | Mental health, wellness, meditation |
| Nike | Fitness, sports, motivation |
| Notion | Productivity, organization |
| Coder | Programming, development |
| Forethought | AI automation, support |
| Skyflow | Security, privacy, data |

## 🎤 The Hosts

- **Alex**: Curious, empathetic, asks questions
- **Maya**: Analytical, data-driven, insightful

## 📁 File Structure

```
SF_AWS_HACK/
├── echoduo.py              # Main CLI
├── api.py                  # REST API
├── podcast_generator.py    # Core logic
├── bedrock_client.py       # AWS integration
├── memory_manager.py       # Redis memory
├── lightpanda_scraper.py   # Web scraping
├── demo.py                 # Interactive demo
├── batch_generator.py      # Batch processing
├── test_echoduo.py         # Tests
├── web_interface.html      # Web UI
├── config.py              # Configuration
├── requirements.txt       # Dependencies
└── README.md             # Full docs
```

## 🔧 Configuration

Edit `.env`:
```bash
ANTHROPIC_API_KEY=sk-ant-your-api-key-here
REDIS_HOST=localhost
REDIS_PORT=6379
MODEL_NAME=claude-3-5-sonnet-20241022
MAX_TOKENS=4096
DEFAULT_TEMPERATURE=0.7
```

## 🐛 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| Redis error | It's optional, uses in-memory fallback |
| API key error | Check ANTHROPIC_API_KEY in .env |
| Rate limit | Add delays between requests |
| Repetitive output | Clear memory: `--clear-memory` |

## 💡 Pro Tips

### Better Topics
✅ "AI ethics in criminal justice"  
❌ "AI" (too broad)

### Provide Context
```bash
python echoduo.py "remote work" \
  --context "74% prefer hybrid, productivity up 13%"
```

### Let AI Choose Sponsor
Omit `--sponsor` for automatic selection based on relevance

### Force Specific Sponsor
```bash
--sponsor Calm
```

### Batch Processing
Create `topics.json`:
```json
[
  {"topic": "AI in healthcare", "sponsor": "Forethought"},
  {"topic": "meditation apps", "sponsor": "Calm"},
  {"topic": "developer tools"}
]
```

## 📊 Performance

- **Time**: 45-65 seconds per episode
- **Cost**: $0.05-0.10 per episode
- **Length**: 12-18 exchanges (customizable)

## 🔒 Security Best Practices

1. Never commit `.env` file
2. Rotate AWS keys regularly
3. Use Redis password in production
4. Validate all user inputs

## 📚 Documentation

| File | Purpose |
|------|---------|
| README.md | Overview & quickstart |
| SETUP.md | Detailed setup |
| USAGE_GUIDE.md | Complete examples |
| ARCHITECTURE.md | Technical details |
| PROJECT_SUMMARY.md | Project overview |
| CONTRIBUTING.md | How to contribute |
| example_output.txt | Sample episodes |

## 🎬 Example Workflow

```bash
# 1. First time setup
./quickstart.sh

# 2. Generate test episode
python echoduo.py "test topic"

# 3. Check memory
python echoduo.py --show-memory

# 4. Generate with options
python echoduo.py "AI trends" --sponsor Notion

# 5. Batch generate
python batch_generator.py example_batch.json

# 6. Start API for integrations
python api.py
```

## 🔗 Quick Links

- **Setup**: See `SETUP.md`
- **Examples**: See `USAGE_GUIDE.md`
- **Architecture**: See `ARCHITECTURE.md`
- **API Docs**: See `api.py` docstrings

## 📞 Getting Help

1. Check relevant `.md` documentation
2. Run tests: `python test_echoduo.py`
3. Try demo: `python demo.py`
4. Check example output: `example_output.txt`

## ⚡ Common Use Cases

### Content Marketing
```bash
python echoduo.py "sustainable fashion" --sponsor Nike
```

### Educational Content
```bash
python echoduo.py "quantum computing basics"
```

### A/B Testing
```bash
for sponsor in Calm Nike Notion; do
  python echoduo.py "workplace wellness" --sponsor $sponsor
done
```

### Scheduled Generation
```bash
# Add to crontab
0 9 * * * cd /path/to/SF_AWS_HACK && python echoduo.py "daily tech news"
```

## 🎯 Quick Quality Check

Good episode has:
- ✅ Natural conversation flow
- ✅ Sponsor mentioned subtly
- ✅ Real-world context integrated
- ✅ Distinct host voices
- ✅ No obvious advertising

## 🚦 Status Indicators

```bash
🎙️  = Main process
🌍 = Fetching context
🎯 = Sponsor selected
💭 = Generating
🧠 = Self-improving
✅ = Complete
❌ = Error
⚠️  = Warning
```

---

**🎙️ Ready to generate?** → `python echoduo.py "your amazing topic"`

**Version 1.0.0** | [Full Docs](README.md) | [Setup](SETUP.md) | [Usage](USAGE_GUIDE.md)

