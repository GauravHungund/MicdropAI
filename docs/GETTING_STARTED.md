# 🚀 Getting Started with EchoDuo

A step-by-step guide to get EchoDuo up and running in under 5 minutes.

## ⚡ Quick Setup

### 1. Get Your Anthropic API Key

1. Visit [Anthropic Console](https://console.anthropic.com/)
2. Sign up or log in
3. Go to **API Keys** section
4. Click **Create Key**
5. Copy your key (starts with `sk-ant-`)

### 2. Install EchoDuo

```bash
cd /Users/gauravhungund/Documents/SF_AWS_HACK

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure API Key

```bash
# Copy example environment file
cp env.example .env

# Edit .env and add your key
nano .env  # or use your preferred editor
```

Add this line to `.env`:
```bash
ANTHROPIC_API_KEY=sk-ant-your-actual-api-key-here
```

**Important:** Replace `sk-ant-your-actual-api-key-here` with your actual API key!

### 4. Generate Your First Podcast

```bash
python echoduo.py "the future of artificial intelligence"
```

That's it! You should see:
```
🌍 Gathering real-world context...
🎯 Selected sponsor: Notion
🎙️  Generating conversation...
🧠 Self-improving conversation...

[Podcast conversation appears here]
```

## 📝 What Just Happened?

1. **Context Gathering**: EchoDuo scraped the web for recent info about AI
2. **Sponsor Selection**: AI chose the most relevant sponsor (likely Notion or Coder)
3. **Generation**: Created a natural conversation between Alex and Maya
4. **Self-Improvement**: Critiqued and improved its own output
5. **Output**: Delivered a polished podcast conversation

## 🎯 Try Different Topics

```bash
# Mental health topic
python echoduo.py "workplace burnout and mental health"

# Tech topic
python echoduo.py "the rise of quantum computing"

# Business topic
python echoduo.py "remote work productivity strategies"

# Fitness topic
python echoduo.py "marathon training in 2024"
```

## 🎨 Force a Specific Sponsor

```bash
python echoduo.py "meditation and mindfulness" --sponsor Calm
```

## 🔍 View Your Memory

See what sponsors and phrases were recently used:

```bash
python echoduo.py --show-memory
```

Output:
```
🧠 Current Memory State:
Recent Sponsors: ['Notion', 'Calm']
Recent Phrases: ['I've been thinking about', 'That's interesting']
Tone Patterns: ['AI-future-Notion', 'mental-health-Calm']
```

## 🧹 Clear Memory

Start fresh (allows recent sponsors again):

```bash
python echoduo.py --clear-memory
```

## 🌐 Use the Web Interface

1. Start the API server:
   ```bash
   python api.py
   ```

2. Open `web_interface.html` in your browser

3. Fill in the form and generate!

## 📦 Generate Multiple Episodes

Create a file called `my_topics.json`:
```json
[
  {"topic": "AI ethics in healthcare"},
  {"topic": "sustainable fashion trends"},
  {"topic": "cryptocurrency regulation"}
]
```

Then run:
```bash
python batch_generator.py my_topics.json
```

## 🧪 Run Tests

Verify everything is working:

```bash
python test_echoduo.py
```

## 💡 Pro Tips

### Tip 1: Better Topics
✅ **Good**: "AI ethics in criminal justice"  
❌ **Bad**: "AI" (too broad)

### Tip 2: Add Context
```bash
python echoduo.py "remote work trends" \
  --context "74% of workers prefer hybrid models, productivity up 13%"
```

### Tip 3: Let AI Choose Sponsors
Don't specify `--sponsor` and let the AI pick the most relevant one.

### Tip 4: Experiment with Topics
The system works best with:
- Current events
- Technology trends
- Health & wellness
- Business & productivity
- Sports & fitness

## 📊 Understanding Costs

Each podcast episode costs approximately:
- **Input tokens**: ~1,500 tokens @ $3/MTok = $0.0045
- **Output tokens**: ~2,000 tokens @ $15/MTok = $0.03
- **Total**: ~$0.035-0.10 per episode

10 episodes ≈ $0.50  
100 episodes ≈ $5.00

Check your usage at [Anthropic Console](https://console.anthropic.com/)

## 🔧 Customization

### Change Host Personalities

Edit `podcast_generator.py` and modify the system prompt:

```python
system_prompt = """You are a master podcast script writer.

Your hosts are:
- Alex: [Customize personality here]
- Maya: [Customize personality here]
```

### Adjust Conversation Length

In `podcast_generator.py`, find:
```python
"- Be 12-18 exchanges long"
```

Change to your preferred length (e.g., "20-25 exchanges long")

### Add New Sponsors

Edit `config.py`:
```python
AVAILABLE_SPONSORS = [
    "Calm",
    "Nike",
    "Notion",
    "Coder",
    "Forethought",
    "Skyflow",
    "YourNewSponsor"  # Add here
]
```

Then update sponsor descriptions in `podcast_generator.py`.

## 🐛 Troubleshooting

### "ANTHROPIC_API_KEY not found"
**Solution**: Make sure `.env` file exists and contains `ANTHROPIC_API_KEY=sk-ant-...`

### "Redis connection failed"
**Solution**: This is just a warning. System uses in-memory fallback automatically. No action needed!

### "Rate limit exceeded"
**Solution**: You're making requests too quickly. Add `--delay 5` to batch generation or wait a moment.

### Conversation seems repetitive
**Solution**: 
```bash
python echoduo.py --clear-memory
```

### Error: "No module named 'anthropic'"
**Solution**:
```bash
pip install -r requirements.txt --upgrade
```

## 📚 Learn More

- **Full Documentation**: See `README.md`
- **Complete Usage Guide**: See `USAGE_GUIDE.md`
- **System Architecture**: See `ARCHITECTURE.md`
- **Example Episodes**: See `example_output.txt`
- **Quick Commands**: See `QUICK_REFERENCE.md`

## 🎉 Next Steps

Now that you're set up:

1. ✅ Generate 3-5 different episodes to see variety
2. ✅ Try the web interface for easier interaction
3. ✅ Experiment with different sponsors
4. ✅ Read `USAGE_GUIDE.md` for advanced features
5. ✅ Check out the API for integrations

## 💬 Example Session

```bash
# Generate first episode
$ python echoduo.py "AI in education"
🎯 Selected sponsor: Notion
[Episode generated]

# Check what was used
$ python echoduo.py --show-memory
Recent Sponsors: ['Notion']

# Generate second episode (won't use Notion again)
$ python echoduo.py "productivity hacks for developers"
🎯 Selected sponsor: Coder
[Episode generated]

# Check memory again
$ python echoduo.py --show-memory
Recent Sponsors: ['Coder', 'Notion']
```

## 🎯 You're Ready!

You now have everything you need to generate amazing AI podcasts with natural sponsor integration.

**Have fun creating! 🎙️✨**

---

**Need help?** Check the troubleshooting section or read `README.md` for more details.

**Version**: 1.0.0 (Anthropic SDK)  
**Last Updated**: November 2025


