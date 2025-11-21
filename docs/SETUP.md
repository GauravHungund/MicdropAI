# 🚀 EchoDuo Setup Guide

Quick setup guide to get EchoDuo running in minutes.

## Prerequisites

- Python 3.8 or higher
- Anthropic API Key ([Sign up here](https://console.anthropic.com/))
- (Optional) Redis server

## Step-by-Step Setup

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Get Anthropic API Key

1. Go to [Anthropic Console](https://console.anthropic.com/)
2. Sign up or log in
3. Navigate to **API Keys** section
4. Click **Create Key**
5. Copy your API key

### 3. Configure Environment

Create a `.env` file in the project root:

```bash
cp env.example .env
```

Edit `.env` and add your Anthropic API key:

```bash
ANTHROPIC_API_KEY=sk-ant-your-api-key-here
MODEL_NAME=claude-3-5-sonnet-20241022
MAX_TOKENS=4096
DEFAULT_TEMPERATURE=0.7
```

### 4. (Optional) Setup Redis

#### macOS

```bash
brew install redis
brew services start redis
```

#### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install redis-server
sudo systemctl start redis-server
```

#### Windows

Download from: https://redis.io/download

**Note:** Redis is optional. EchoDuo will automatically fall back to in-memory storage if Redis is not available.

### 5. Verify Installation

Run the test suite:

```bash
python test_echoduo.py
```

Run the demo:

```bash
python demo.py
```

## Quick Test

Generate your first podcast episode:

```bash
python echoduo.py "the future of artificial intelligence"
```

## Troubleshooting

### Error: "ANTHROPIC_API_KEY not found"

**Solution:**
- Check that `.env` file exists in the project root
- Verify API key is correctly set: `ANTHROPIC_API_KEY=sk-ant-...`
- Make sure there are no quotes around the key
- Get a new key from [Anthropic Console](https://console.anthropic.com/) if needed

### Error: "Redis connection failed"

**Solution:**
- Install and start Redis server
- Or just ignore - system will use in-memory fallback
- Check Redis connection with: `redis-cli ping`

### Error: "ModuleNotFoundError"

**Solution:**
```bash
pip install -r requirements.txt --upgrade
```

## API Costs

Approximate costs per podcast episode using Anthropic API:
- Claude 3.5 Sonnet input: ~1,500 tokens @ $3/MTok = $0.0045
- Claude 3.5 Sonnet output: ~2,000 tokens @ $15/MTok = $0.030
- **Total: ~$0.035-0.10 per episode**

Check current pricing at [Anthropic Pricing](https://www.anthropic.com/pricing#anthropic-api)

## Next Steps

1. ✅ Read the [README.md](README.md) for full documentation
2. ✅ Try different topics and sponsors
3. ✅ Customize host personalities in `podcast_generator.py`
4. ✅ Integrate with your own applications

## Need Help?

Common commands:

```bash
# Generate podcast
python echoduo.py "your topic"

# Force specific sponsor
python echoduo.py "your topic" --sponsor Calm

# View memory state
python echoduo.py --show-memory

# Clear memory
python echoduo.py --clear-memory

# Run tests
python test_echoduo.py

# Run demo
python demo.py
```

Happy podcasting! 🎙️✨

