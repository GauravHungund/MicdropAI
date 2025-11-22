# 🎙️ EchoDuo - Step-by-Step Project Flow

Complete flow of how the EchoDuo podcast generation system works from start to finish.

---

## 📋 High-Level Overview

**EchoDuo** is an autonomous AI podcast generator that creates natural conversations between two hosts (Alex & Maya) with intelligent sponsor integration, real-world context, and memory management.

---

## 🔄 Complete Flow (Step-by-Step)

### **PHASE 1: User Input** 👤

1. **User enters topic** in frontend UI
   - Location: `frontend/src/components/PromptInput.jsx`
   - User types: "AI and creativity"
   - Clicks "Generate Podcast" button

2. **Form submission**
   - `handleSubmit()` captures the topic
   - Validates input (not empty)
   - Calls `onGenerate(topic)` with the topic string

---

### **PHASE 2: Frontend API Call** 📡

3. **API service call**
   - Location: `frontend/src/services/api.js`
   - Function: `generatePodcast(topic)`
   - Sends POST request to: `http://localhost:5000/generate`
   - Request body:
     ```json
     {
       "topic": "AI and creativity"
     }
     ```

4. **Frontend shows loading state**
   - Sets `isGenerating = true`
   - Shows animated loading spinner
   - Hides input form

---

### **PHASE 3: Backend Receives Request** 🔧

5. **Flask API receives request**
   - Location: `backend/api.py`
   - Endpoint: `POST /generate`
   - Extracts `topic` from request body
   - Calls `generator.generate(topic)`

6. **PodcastGenerator initialization**
   - Location: `backend/podcast_generator.py`
   - Initializes:
     - `ClaudeClient` (Anthropic API)
     - `MemoryManager` (Redis)
     - `SmartScraper` (web scraping)

---

### **PHASE 4: Context Gathering** 🌐

7. **Smart scraping pipeline**
   - Location: `backend/smart_scraper.py`
   
   **Step 7a: Claude selects targets**
   - Claude analyzes topic: "AI and creativity"
   - Generates list of relevant websites to scrape
   - Returns URLs like:
     - `https://www.technologyreview.com/topic/artificial-intelligence/`
     - `https://techcrunch.com/tag/ai/`
   
   **Step 7b: Scraping targets**
   - Tries Lightpanda Cloud (if API key available)
   - Falls back to Playwright (local Chrome)
   - Falls back to HTTP (BeautifulSoup)
   - Extracts content from each URL
   
   **Step 7c: Synthesize context**
   - Claude synthesizes scraped data
   - Creates concise context summary (3-4 sentences)
   - Includes statistics, recent developments, insights

---

### **PHASE 5: Memory Check** 🗄️

8. **Redis memory query**
   - Location: `backend/memory_manager.py`
   - Queries Redis for:
     - Recent sponsors (last 5)
     - Recent phrases (last 20)
     - Tone patterns (last 10)
   - Returns memory summary to avoid repetition

---

### **PHASE 6: Sponsor Selection** 💰

9. **AI selects sponsor**
   - Location: `backend/podcast_generator.py`
   - Claude analyzes topic relevance
   - Available sponsors: Calm, Nike, Notion, Coder, Forethought, Skyflow
   - Excludes recently used sponsors (from memory)
   - Selects most relevant sponsor for topic
   - Example: "Notion" for productivity/AI topics

---

### **PHASE 7: Initial Conversation Generation** 🎬

10. **Alpha generation**
    - Location: `backend/podcast_generator.py`
    - System prompt defines Alex & Maya personalities
    - User prompt includes:
      - Topic
      - Real-world context (from scraping)
      - Selected sponsor
      - Memory constraints (avoid repetition)
    - Claude generates initial conversation (12-18 exchanges)
    - Format: Dialogue only (Alex: ... / Maya: ...)

---

### **PHASE 8: Self-Critique** 🔍

11. **AI critiques its own output**
    - Location: `backend/podcast_generator.py`
    - Claude analyzes the conversation for:
      - Naturalness and flow
      - Sponsor integration (organic vs forced)
      - Awkward transitions
      - Host personality consistency
    - Generates critique feedback

---

### **PHASE 9: Improvement** ✨

12. **Beta generation**
    - Location: `backend/podcast_generator.py`
    - Uses critique feedback
    - Generates improved version
    - Fixes identified issues
    - Returns polished final conversation

---

### **PHASE 10: Memory Update** 💾

13. **Update Redis memory**
    - Location: `backend/memory_manager.py`
    - Adds sponsor to `recent_sponsors` list
    - Adds key phrases to `recent_phrases` list
    - Adds tone pattern (topic-sponsor combo)
    - Trims lists to max sizes (5 sponsors, 20 phrases)

---

### **PHASE 11: Sanity CMS Save** 📚

14. **Save to Sanity CMS**
    - Location: `backend/sanity_client.py`
    - Creates episode document with:
      - Topic
      - Full conversation
      - Sponsor
      - Context used
      - Sources
      - Timestamp
    - Saves to Sanity dataset: `production`
    - Returns document ID

---

### **PHASE 12: Response to Frontend** 📤

15. **Backend returns response**
    - Location: `backend/api.py`
    - Response format:
      ```json
      {
        "success": true,
        "data": {
          "conversation": "Alex: ...\nMaya: ...",
          "sponsor": "Notion",
          "topic": "AI and creativity",
          "context_snippet": "..."
        }
      }
      ```

---

### **PHASE 13: Frontend Display** 🎨

16. **Frontend receives and displays**
    - Location: `frontend/src/App.jsx`
    - Sets `podcastData = response.data`
    - Sets `isGenerating = false`
    - Sets `isPlaying = true`
    - Scrolls to player component

17. **PodcastPlayer renders**
    - Location: `frontend/src/components/PodcastPlayer.jsx`
    - Shows:
      - Waveform animation
      - Topic title
      - Sponsor badge
      - Full conversation transcript
      - Play button

---

## 🔄 Complete Flow Diagram

```
[User Input]
    ↓
[Frontend Form] → POST /generate { topic }
    ↓
[Backend API] → PodcastGenerator.generate()
    ↓
[Smart Scraper] → Claude selects URLs → Scrape → Synthesize context
    ↓
[Memory Manager] → Check Redis (sponsors, phrases)
    ↓
[Sponsor Selection] → Claude picks relevant sponsor
    ↓
[Alpha Generation] → Initial conversation
    ↓
[Self-Critique] → Analyze for improvements
    ↓
[Beta Generation] → Improved conversation
    ↓
[Memory Update] → Save to Redis
    ↓
[Sanity Save] → Save episode to CMS
    ↓
[API Response] → Return to frontend
    ↓
[Frontend Display] → Show transcript
```

---

## 🎯 Key Components

### **Frontend** (React + Vite)
- `PromptInput.jsx` - Topic input form
- `PodcastPlayer.jsx` - Transcript display
- `api.js` - Backend API client

### **Backend** (Python + Flask)
- `api.py` - REST API server
- `podcast_generator.py` - Core generation logic
- `claude_client.py` - Anthropic Claude API
- `smart_scraper.py` - Intelligent web scraping
- `memory_manager.py` - Redis memory management
- `sanity_client.py` - Sanity CMS integration

### **Infrastructure**
- **Redis** - Memory storage (sponsors, phrases, patterns)
- **Sanity CMS** - Episode storage and management
- **Lightpanda** - Web scraping (optional, with API key)
- **Playwright** - JavaScript rendering (fallback)

---

## ⏱️ Timing Breakdown

- **Frontend → Backend**: < 1 second
- **Context Gathering**: 10-30 seconds
  - Claude target selection: 3-5 seconds
  - Web scraping: 5-20 seconds
  - Context synthesis: 2-5 seconds
- **Memory Check**: < 1 second
- **Sponsor Selection**: 2-3 seconds
- **Alpha Generation**: 10-15 seconds
- **Self-Critique**: 5-8 seconds
- **Beta Generation**: 10-15 seconds
- **Memory Update**: < 1 second
- **Sanity Save**: 1-2 seconds
- **Total**: ~45-75 seconds

---

## 🎤 The Hosts

### **Alex** - The Curious Explorer
- Opens with: "I've been thinking about..."
- Asks: "What do you think that means for...?"
- Reflects: "That really resonates with me..."
- Voice: Warm, inviting, thoughtful

### **Maya** - The Analytical Mind
- Opens with: "From a technical standpoint..."
- Analyzes: "What the data shows is..."
- Grounds: "But here's the reality..."
- Voice: Clear, confident, matter-of-fact

---

## 💰 Sponsor Integration

Sponsors are embedded naturally:
- **Alex**: Personal experience ("I've been using Notion...")
- **Maya**: Practical tool ("From a productivity standpoint, Notion...")
- **No advertising language**: Never says "sponsored by"
- **Organic mentions**: Feels like genuine recommendation

---

## 🗄️ Memory System

**Redis tracks:**
- **Recent Sponsors** (5): Prevents sponsor repetition
- **Recent Phrases** (20): Avoids repetitive language
- **Tone Patterns** (10): Varies conversation styles

**Example:**
- If "Calm" used recently → Won't use again
- If phrase "That's really interesting" used → Avoids it
- If pattern "AI-creativity-Calm" exists → Tries different approach

---

## 📊 Data Flow

```
Input: "AI and creativity"
  ↓
Context: "AI systems have seen 340% growth..."
  ↓
Sponsor: "Notion" (selected by AI)
  ↓
Memory: Exclude ["Calm", "Coder"] (recent)
  ↓
Conversation: Alex & Maya discuss topic naturally
  ↓
Output: Full transcript with sponsor embedded
  ↓
Storage: Saved to Redis + Sanity CMS
```

---

## 🚀 Quick Start Flow

1. **Start Backend:**
   ```bash
   source venv/bin/activate
   cd backend
   python api.py
   ```

2. **Start Frontend:**
   ```bash
   cd frontend
   npm run dev
   ```

3. **Use Application:**
   - Open: http://localhost:5173
   - Enter topic
   - Click "Generate Podcast"
   - Wait ~60 seconds
   - See transcript!

---

## 🔍 Debugging Flow

**Check each phase:**

1. **Frontend logs** (Browser console):
   - `🎙️  Starting podcast generation...`
   - `📡 Calling backend API...`
   - `✅ Podcast generated successfully!`

2. **Backend logs** (Terminal):
   - `🧠 INTELLIGENT SCRAPING PIPELINE`
   - `🗄️  Redis: Added sponsor...`
   - `💾 Sanity: Episode saved...`

3. **Redis** (Terminal):
   ```bash
   redis-cli MONITOR  # Watch all operations
   redis-cli LRANGE recent_sponsors 0 -1
   ```

4. **Sanity** (Dashboard):
   - https://manage.sanity.io
   - Vision → Query: `*[_type == "episode"]`

---

## 📝 Example Complete Flow

**Input:** "AI and creativity"

**Step 1:** User types in frontend → Form submits

**Step 2:** Frontend sends: `POST /generate { "topic": "AI and creativity" }`

**Step 3:** Backend receives, starts generation

**Step 4:** Smart scraper:
   - Claude suggests: techcrunch.com/tag/ai, technologyreview.com/topic/ai
   - Playwright scrapes these URLs
   - Extracts content
   - Claude synthesizes: "AI systems have seen 340% growth..."

**Step 5:** Memory check:
   - Recent sponsors: ["Calm", "Coder"]
   - Available: ["Nike", "Notion", "Forethought", "Skyflow"]

**Step 6:** Sponsor selection:
   - Claude picks "Notion" (most relevant for AI/productivity)

**Step 7:** Generate conversation:
   - Alex: "I've been thinking about AI's impact on creativity..."
   - Maya: "From a data perspective, what's happening is fascinating..."
   - (12-18 exchanges with Notion mentioned naturally)

**Step 8:** Self-critique:
   - "Sponsor mention feels natural ✓"
   - "Flow is good ✓"
   - "Could improve transition at exchange 7"

**Step 9:** Improved version generated

**Step 10:** Save to Redis:
   - Add "Notion" to recent_sponsors
   - Add phrases to recent_phrases

**Step 11:** Save to Sanity:
   - Document ID: `episode-xxxxx-xxxxx`

**Step 12:** Return to frontend:
   - Shows full transcript
   - Displays topic, sponsor, conversation

**Result:** Complete podcast episode ready!

---

## 🎯 Key Features

✅ **Natural Conversations** - Realistic dialogue between two distinct hosts
✅ **Intelligent Sponsors** - AI-selected, naturally embedded
✅ **Real-World Context** - Web scraping for current information
✅ **Memory Management** - Prevents repetition via Redis
✅ **Self-Improvement** - AI critiques and improves its own output
✅ **CMS Integration** - Auto-saves to Sanity
✅ **Beautiful UI** - Modern React frontend with animations

---

**Last Updated:** Based on current implementation

