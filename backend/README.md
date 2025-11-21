# EchoDuo Backend

This is the backend server for the EchoDuo podcast generation system.

## Structure

- **Core Modules:**
  - `podcast_generator.py` - Main podcast generation logic
  - `claude_client.py` - Anthropic Claude API client
  - `sanity_client.py` - Sanity CMS integration
  - `memory_manager.py` - Redis memory management
  - `config.py` - Configuration management

- **Scraping:**
  - `smart_scraper.py` - Intelligent web scraping with Claude
  - `lightpanda_scraper.py` - Lightpanda integration
  - `lightpanda_playwright_client.py` - Playwright-based scraping
  - `playwright_scraper.py` - Playwright scraping utilities

- **Entry Points:**
  - `echoduo.py` - CLI interface
  - `api.py` - REST API server
  - `demo.py` - Interactive demo
  - `batch_generator.py` - Batch episode generation

- **Utilities:**
  - `view_episodes.py` - View saved episodes from Sanity
  - `test_*.py` - Test scripts

## Setup

1. Create virtual environment (from project root):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On macOS/Linux
   ```

2. Install dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. Configure environment:
   - Copy `env.example` to `.env` in the project root
   - Add your API keys (Anthropic, Lightpanda, Redis, Sanity)

## Usage

From the project root:

```bash
# Activate virtual environment
source venv/bin/activate

# Run CLI
python backend/echoduo.py "your topic"

# Run API server
python backend/api.py

# View episodes
python backend/view_episodes.py
```

## Note

The `.env` file should remain in the project root directory (not in backend/).

