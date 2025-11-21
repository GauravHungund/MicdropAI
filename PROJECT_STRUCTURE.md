# 📁 EchoDuo Project Structure

```
SF_AWS_HACK/
├── backend/                    # Python backend code
│   ├── *.py                   # All Python modules
│   ├── requirements.txt       # Python dependencies
│   ├── env.example           # Environment template
│   ├── sanity_schema/        # Sanity schema files
│   └── README.md             # Backend documentation
│
├── studio-hello-world/        # Sanity Studio (frontend)
│   ├── schemaTypes/          # Sanity schemas
│   ├── sanity.config.ts      # Sanity configuration
│   └── package.json          # Node dependencies
│
├── docs/                      # Documentation files
│   ├── ARCHITECTURE.md
│   ├── SANITY_SETUP.md
│   ├── SMART_SCRAPING.md
│   └── ...
│
├── venv/                      # Python virtual environment
├── .env                       # Environment variables (SECRET - not in git)
├── README.md                  # Main project readme
└── INFORMATION.md             # Project overview
```

## Quick Start

### Setup

1. **Create virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # macOS/Linux
   ```

2. **Install backend dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Configure environment:**
   - Copy `backend/env.example` to `.env` in project root
   - Add your API keys

4. **Setup Sanity Studio:**
   ```bash
   cd studio-hello-world
   npm install
   sanity start
   ```

### Running

**From project root:**

```bash
# Activate venv first
source venv/bin/activate

# Generate podcast episode
python backend/echoduo.py "AI and creativity"

# View saved episodes
python backend/view_episodes.py

# Run API server
python backend/api.py
```

## Important Notes

- **`.env` file** stays in project root (never commit to git)
- **`venv/`** stays in project root
- **`studio-hello-world/`** stays in project root (separate from backend)
- All Python code is in `backend/`
- All documentation is in `docs/`

## Paths

When running scripts:
- **From project root:** `python backend/script.py`
- **From backend folder:** `python script.py` (when venv is activated)

