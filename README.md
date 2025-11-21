# 🎙️ EchoDuo - Autonomous AI Podcast Generator

An intelligent, self-improving two-host AI podcast system that generates natural conversations while seamlessly embedding relevant sponsors.

## 🌟 Features

- **Natural Dialogue Generation**: Creates realistic conversations between two distinct AI hosts (Alex & Maya)
- **Intelligent Sponsor Integration**: Weaves sponsors naturally into conversations without sounding like ads
- **Real-World Context**: Uses web scraping (Lightpanda-style) to incorporate current, relevant information
- **Memory Management**: Redis-based memory system prevents repetition of sponsors, phrases, and patterns
- **Self-Improvement**: Automatically critiques and improves its own output before final delivery
- **Claude API Integration**: Powered by Claude 3.5 Sonnet via Anthropic API

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│                    EchoDuo System                    │
├─────────────────────────────────────────────────────┤
│                                                      │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────┐ │
│  │  Lightpanda  │  │    Redis     │  │  Bedrock  │ │
│  │   Scraper    │  │    Memory    │  │  (Claude) │ │
│  └──────┬───────┘  └──────┬───────┘  └─────┬─────┘ │
│         │                 │                 │       │
│         └────────┬────────┴─────────────────┘       │
│                  │                                   │
│         ┌────────▼───────────┐                      │
│         │ Podcast Generator  │                      │
│         │  - Topic Analysis  │                      │
│         │  - Sponsor Select  │                      │
│         │  - Conversation    │                      │
│         │  - Self-Critique   │                      │
│         └────────────────────┘                      │
│                                                      │
└─────────────────────────────────────────────────────┘
```

## 📋 Requirements

- Python 3.8+
- Anthropic API Key ([Get one here](https://console.anthropic.com/))
- Redis (optional - has in-memory fallback)

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
cd SF_AWS_HACK

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Copy the example environment file and configure your credentials:

```bash
cp .env.example .env
```

Edit `.env`:

```bash
# Anthropic API Configuration
ANTHROPIC_API_KEY=your_api_key_here

# Redis Configuration (optional)
REDIS_HOST=localhost
REDIS_PORT=6379

# Model Configuration
MODEL_NAME=claude-3-5-sonnet-20241022
MAX_TOKENS=4096
DEFAULT_TEMPERATURE=0.7
```

### 3. Run EchoDuo

```bash
python echoduo.py "AI taking over jobs"
```

## 💡 Usage Examples

### Basic Usage

```bash
python echoduo.py "climate change and technology"
```

### With Custom Context

```bash
python echoduo.py "remote work trends" --context "Recent study shows 74% of workers prefer hybrid models..."
```

### Force a Specific Sponsor

```bash
python echoduo.py "mental health in tech" --sponsor Calm
```

### Memory Management

```bash
# View current memory
python echoduo.py --show-memory

# Clear memory (reset sponsor/phrase history)
python echoduo.py --clear-memory
```

## 🎭 The Hosts

**Alex** - Curious, reflective, empathetic
- Asks thoughtful questions
- Draws connections between ideas
- Brings emotional intelligence

**Maya** - Analytical, grounded, insightful
- Provides data-driven analysis
- Offers practical perspectives
- Grounds conversations in reality

## 🎯 Available Sponsors

- **Calm** - Meditation, mental health, mindfulness, wellness
- **Nike** - Fitness, sports, motivation, performance
- **Notion** - Productivity, organization, collaboration tools
- **Coder** - Developer tools, programming platforms
- **Forethought** - AI automation, customer service
- **Skyflow** - Data privacy, security, compliance

## 🧠 How It Works

1. **Context Gathering**: Scrapes real-world information about the topic
2. **Memory Check**: Reviews recent sponsors and phrases to avoid repetition
3. **Sponsor Selection**: AI chooses the most relevant sponsor for the topic
4. **Initial Generation**: Creates first draft of conversation
5. **Self-Critique**: Analyzes the conversation for naturalness and flow
6. **Improvement**: Generates final improved version
7. **Memory Update**: Stores sponsor and key phrases for future avoidance

## 🔧 Project Structure

```
SF_AWS_HACK/
├── echoduo.py              # Main entry point
├── podcast_generator.py    # Core generation logic
├── bedrock_client.py       # AWS Bedrock/Claude interface
├── memory_manager.py       # Redis memory management
├── lightpanda_scraper.py   # Web scraping for context
├── config.py              # Configuration management
├── requirements.txt       # Python dependencies
├── .env.example          # Environment template
└── README.md            # This file
```

## 🎨 Example Output

```
Alex: So I've been thinking about this whole AI automation thing. The numbers are actually pretty staggering.

Maya: Right, I saw that recent report - 27% of repetitive roles automated in just the last year. That's not some distant future prediction, that's happening now.

Alex: And here's what gets me - everyone focuses on the jobs being lost, but what about the new ones emerging? Like AI supervision roles, or human-AI collaboration specialists?

Maya: Exactly. It's not just displacement, it's transformation. Though I'll admit, when I'm organizing all this information, trying to keep track of different perspectives, data points, studies...

Alex: You use Notion for that, right?

Maya: Yeah, it's been a game-changer. I can link related ideas, embed data, create different views. It's like having a second brain that actually helps me think through these complex topics instead of just storing information.

Alex: That's interesting because it's kind of meta - using a productivity tool to analyze how AI tools are changing work.
...
```

## 🔒 Privacy & Security

- No conversation content is stored permanently
- Only metadata (sponsor names, key phrases) kept in Redis
- All web scraping respects robots.txt and rate limits
- AWS credentials never exposed in code

## 🐛 Troubleshooting

### Redis Connection Issues
If Redis is not available, the system automatically falls back to in-memory storage. You'll see:
```
⚠️  Redis not available, using in-memory fallback
```

### AWS Bedrock Access
Ensure your AWS account has Bedrock access enabled and Claude 3.5 Sonnet model access granted.

### Web Scraping Fails
The system includes fallback context for common topics if web scraping fails.

## 🚧 Future Enhancements

- [ ] Multiple voice profiles beyond Alex & Maya
- [ ] Audio generation integration
- [ ] Multi-episode story arcs
- [ ] Sentiment analysis for sponsor fit
- [ ] A/B testing different conversation styles
- [ ] Integration with podcast hosting platforms

## 📄 License

MIT License - Feel free to use this for your hackathon projects!

## 🤝 Contributing

This is a hackathon project, but contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Share your generated podcasts

## 🎉 Credits

Built for the SF AWS Hackathon 2025

Powered by:
- AWS Bedrock (Claude 3.5 Sonnet)
- Redis
- Python ecosystem

---

Made with ❤️ and ☕ by the EchoDuo team

