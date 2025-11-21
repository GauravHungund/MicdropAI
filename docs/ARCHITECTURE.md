# 🏗️ EchoDuo Architecture

Detailed architectural documentation for the EchoDuo AI podcast generation system.

## System Overview

EchoDuo is a sophisticated multi-component system that generates natural podcast conversations with intelligently embedded sponsors. The architecture emphasizes autonomy, self-improvement, and contextual awareness.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Interface Layer                     │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐ │
│  │   CLI Tool  │  │  Flask API  │  │  Web Interface (HTML)   │ │
│  │ (echoduo.py)│  │  (api.py)   │  │  (web_interface.html)  │ │
│  └──────┬──────┘  └──────┬──────┘  └───────────┬─────────────┘ │
└─────────┼─────────────────┼──────────────────────┼───────────────┘
          │                 │                      │
          └─────────────────┴──────────────────────┘
                            │
┌───────────────────────────▼───────────────────────────────────┐
│                   Core Generation Engine                      │
│                   (podcast_generator.py)                      │
│                                                               │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │  1. Context Gathering       (Lightpanda Scraper)        │ │
│  │  2. Memory Check            (Redis Memory Manager)      │ │
│  │  3. Sponsor Selection       (LLM-based ranking)         │ │
│  │  4. Initial Generation      (AWS Bedrock - Claude)      │ │
│  │  5. Self-Critique           (LLM as critic)             │ │
│  │  6. Improvement Loop        (Iterative refinement)      │ │
│  │  7. Memory Update           (Store patterns)            │ │
│  └─────────────────────────────────────────────────────────┘ │
└───────────────────────────────────────────────────────────────┘
           │                │                  │
           ▼                ▼                  ▼
┌──────────────────┐  ┌──────────────┐  ┌────────────────┐
│   Lightpanda     │  │    Redis     │  │  Claude API    │
│    Scraper       │  │   Memory     │  │  (Anthropic)   │
│ - Web scraping   │  │ - Sponsors   │  │ - Generation   │
│ - Context fetch  │  │ - Phrases    │  │ - Critique     │
│ - Fallbacks      │  │ - Patterns   │  │ - Improvement  │
└──────────────────┘  └──────────────┘  └────────────────┘
```

## Component Details

### 1. Podcast Generator (`podcast_generator.py`)

**Purpose:** Core orchestrator for the entire generation pipeline.

**Key Methods:**
- `generate()` - Main entry point, orchestrates entire flow
- `select_sponsor()` - Uses LLM to choose most relevant sponsor
- `generate_initial_conversation()` - Creates first draft
- `critique_and_improve()` - Self-improvement loop
- `extract_key_phrases()` - Memory extraction

**Flow:**
1. Receive topic + optional context
2. Fetch real-world context (if not provided)
3. Load memory (recent sponsors/phrases)
4. Select appropriate sponsor
5. Generate initial conversation
6. Critique and improve
7. Update memory
8. Return final result

### 2. Claude Client (`claude_client.py`)

**Purpose:** Interface with Anthropic's Claude API.

**Architecture:**
```
┌─────────────────────────────────────┐
│       Claude Client                 │
├─────────────────────────────────────┤
│  generate()                         │
│  ├─ Standard generation             │
│  ├─ Temperature control             │
│  └─ Token management                │
│                                     │
│  generate_streaming()               │
│  ├─ Stream text chunks              │
│  ├─ Real-time output                │
│  └─ Lower latency                   │
└─────────────────────────────────────┘
```

**Key Features:**
- Simple API key authentication
- Error handling with Anthropic SDK
- Support for streaming responses
- Configurable temperature and max tokens

### 3. Memory Manager (`memory_manager.py`)

**Purpose:** Persistent memory using Redis with in-memory fallback.

**Data Structures:**

```redis
recent_sponsors: LIST
├─ [0] "Calm"
├─ [1] "Nike"
└─ [2] "Notion"

recent_phrases: LIST
├─ [0] "I've been thinking about"
├─ [1] "That's really interesting"
└─ [2] "Let me tell you"

tone_patterns: LIST
├─ [0] "AI-automation-Coder"
└─ [1] "mental-health-Calm"
```

**Operations:**
- `add_sponsor()` - LPUSH with LTRIM to maintain size
- `get_recent_sponsors()` - LRANGE to retrieve
- Automatic fallback to dict if Redis unavailable

### 4. Lightpanda Scraper (`lightpanda_scraper.py`)

**Purpose:** Real-world context gathering from web.

**Strategy:**
```
Topic → Search Strategy → URL Fetch → Content Extract → Clean → Return
```

**Features:**
- Multi-source scraping
- Intelligent fallbacks for common topics
- BeautifulSoup parsing
- Rate limiting and politeness
- Content truncation (1000 chars per source)

**Fallback System:**
```python
{
    "AI taking over jobs": "Recent reports show...",
    "mental health": "WHO reports...",
    "remote work": "Studies show...",
    # ... more fallbacks
}
```

## Prompt Engineering Architecture

### Sponsor Selection Prompt

```
Context: Topic + Available Sponsors + Descriptions
Task: Match topic to sponsor semantically
Output: Single sponsor name
Temperature: 0.3 (deterministic)
Max Tokens: 50
```

### Initial Conversation Generation Prompt

```
System Prompt:
├─ Host personalities defined
├─ Format rules (Alex:/Maya:)
├─ No narration rule
└─ Sponsor integration guidelines

User Prompt:
├─ Topic
├─ Real-world context
├─ Chosen sponsor
├─ Recent memory (avoid patterns)
└─ Length guidelines (12-18 exchanges)

Temperature: 0.8 (creative)
Max Tokens: 3000
```

### Critique and Improvement Prompt

```
Role: Harsh critic + improver
Input: Original conversation + evaluation criteria
Process:
├─ Mental critique (internal)
├─ Identify issues
└─ Generate improved version

Output: Only improved conversation
Temperature: 0.7 (balanced)
Max Tokens: 3500
```

## Self-Improvement Loop

```
┌─────────────────────────────────────────────────┐
│              Self-Improvement Cycle              │
├─────────────────────────────────────────────────┤
│                                                  │
│  1. Generate Alpha Version                      │
│     ├─ Topic + Context + Sponsor                │
│     └─ Output: initial_conversation             │
│                                                  │
│  2. Analyze                                     │
│     ├─ Naturalness check                        │
│     ├─ Sponsor integration quality              │
│     ├─ Flow and transitions                     │
│     ├─ Host voice distinctiveness               │
│     └─ Engagement level                         │
│                                                  │
│  3. Generate Beta Version                       │
│     ├─ Fix identified issues                    │
│     ├─ Enhance natural flow                     │
│     └─ Output: improved_conversation            │
│                                                  │
│  4. Return Final                                │
│                                                  │
└─────────────────────────────────────────────────┘
```

## Memory System Architecture

### Memory Lifecycle

```
Episode 1:
├─ Generate conversation
├─ Select sponsor: "Calm"
├─ Store in Redis: recent_sponsors[0] = "Calm"
└─ Extract phrases: ["I've been thinking", "That's interesting"]

Episode 2:
├─ Load memory: recent_sponsors = ["Calm"]
├─ Exclude "Calm" from selection
├─ Select different sponsor: "Nike"
├─ Avoid phrases: ["I've been thinking", "That's interesting"]
└─ Generate with new patterns

Episode 6:
├─ Sponsor list full (5 entries)
├─ LTRIM removes oldest
└─ "Calm" now available again
```

### Memory Priority

1. **Sponsors**: Last 5 used → Prevent immediate repetition
2. **Phrases**: Last 20 used → Avoid formulaic language
3. **Tone Patterns**: Last 10 used → Vary conversation style

## API Architecture

### REST Endpoints

```
POST /generate
├─ Body: { topic, context?, sponsor? }
├─ Process: Full generation pipeline
└─ Response: { conversation, sponsor, topic, context }

GET /memory
├─ Process: Retrieve current state
└─ Response: { recent_sponsors[], recent_phrases[], tone_patterns[] }

POST /memory/clear
├─ Process: Clear all Redis keys
└─ Response: { success: true }

GET /sponsors
├─ Process: Return available sponsors
└─ Response: { sponsors: [...] }

GET /health
└─ Response: { status: "healthy" }
```

## Data Flow Diagram

```
User Input (Topic)
    │
    ▼
┌────────────────────┐
│ Lightpanda Scraper │ ──→ Real-world Context
└────────────────────┘
    │
    ▼
┌────────────────────┐
│  Memory Manager    │ ──→ Recent Sponsors/Phrases
└────────────────────┘
    │
    ▼
┌────────────────────┐
│ Sponsor Selector   │ ──→ Chosen Sponsor
└────────────────────┘
    │
    ▼
┌────────────────────┐
│ Initial Generator  │ ──→ Alpha Conversation
└────────────────────┘
    │
    ▼
┌────────────────────┐
│   Critic System    │ ──→ Analysis
└────────────────────┘
    │
    ▼
┌────────────────────┐
│  Improver System   │ ──→ Beta Conversation
└────────────────────┘
    │
    ▼
┌────────────────────┐
│  Memory Update     │ ──→ Store Patterns
└────────────────────┘
    │
    ▼
Final Output (Conversation)
```

## Error Handling Strategy

### Graceful Degradation

```
AWS Bedrock Failure
├─ Retry with exponential backoff
├─ Log error details
└─ Raise exception (no silent failure)

Redis Connection Failure
├─ Automatic fallback to in-memory dict
├─ Warning message to user
└─ Continue operation normally

Web Scraping Failure
├─ Try multiple sources
├─ Use fallback context library
└─ Synthetic context generation

Invalid Sponsor Selection
├─ Validate against AVAILABLE_SPONSORS
├─ Fallback to first available
└─ Log warning
```

## Performance Characteristics

### Latency

- Lightpanda scraping: 3-5 seconds
- Memory operations: <10ms (Redis) or <1ms (in-memory)
- Sponsor selection: 1-2 seconds (API call)
- Initial generation: 15-25 seconds (API call)
- Critique + improvement: 20-30 seconds (API call)
- **Total: ~45-65 seconds per episode**

### Cost (per episode via Anthropic API)

- Claude 3.5 Sonnet input: ~1,500 tokens @ $3/MTok = $0.0045
- Claude 3.5 Sonnet output: ~2,000 tokens @ $15/MTok = $0.030
- **Total: ~$0.035-0.10 per episode**

### Scalability

- **Horizontal:** Multiple API instances behind load balancer
- **Vertical:** Increase Anthropic API rate limits (contact support)
- **Caching:** Redis can handle 100K+ episodes metadata
- **Async:** Could parallelize scraping + memory ops

## Security Considerations

1. **API Keys**: Stored in `.env`, never committed
2. **Redis**: Optional password authentication
3. **API**: CORS enabled, add rate limiting for production
4. **Input Validation**: Sanitize topics to prevent injection
5. **Content Safety**: Anthropic API has built-in safety filters

## Future Architecture Extensions

### Potential Enhancements

```
┌─────────────────────────────────────┐
│     Audio Generation Layer          │
│  (AWS Polly / ElevenLabs)          │
└─────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────┐
│   Multi-Episode Story Arc Engine    │
│  (Track themes across episodes)     │
└─────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────┐
│    A/B Testing & Analytics          │
│  (Track engagement metrics)         │
└─────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────┐
│   Automated Publishing Pipeline     │
│  (RSS, Spotify, Apple Podcasts)    │
└─────────────────────────────────────┘
```

## Configuration Management

```python
# config.py structure
├─ Anthropic API Configuration (api_key)
├─ Redis Configuration (host, port, auth)
├─ Model Configuration (model_name, max_tokens, temperature)
├─ Podcast Configuration (sponsors list)
└─ Memory Configuration (history sizes)
```

All config exposed via environment variables for 12-factor app compliance.

---

**Last Updated:** November 2025  
**Version:** 1.0.0  
**Maintainer:** EchoDuo Team

