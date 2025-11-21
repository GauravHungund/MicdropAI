"""Configuration management for EchoDuo podcast system."""
import os
from dotenv import load_dotenv

load_dotenv()

# Anthropic API Configuration
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')

# Lightpanda API Configuration
LIGHTPANDA_API_KEY = os.getenv('LIGHTPANDA_API_KEY')

# Redis Configuration
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
REDIS_DB = int(os.getenv('REDIS_DB', 0))
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', None)

# Model Configuration
MODEL_NAME = os.getenv('MODEL_NAME', 'claude-3-5-sonnet-20241022')
MAX_TOKENS = int(os.getenv('MAX_TOKENS', 4096))
DEFAULT_TEMPERATURE = float(os.getenv('DEFAULT_TEMPERATURE', 0.7))

# Podcast Configuration
AVAILABLE_SPONSORS = [
    "Calm",
    "Nike",
    "Notion",
    "Coder",
    "Forethought",
    "Skyflow"
]

# Memory Configuration
MAX_SPONSOR_HISTORY = 5
MAX_PHRASE_HISTORY = 20

# Redis Logging Configuration
REDIS_VERBOSE_LOGGING = os.getenv('REDIS_VERBOSE_LOGGING', 'true').lower() == 'true'

# Sanity CMS Configuration
SANITY_PROJECT_ID = os.getenv('SANITY_PROJECT_ID')
SANITY_DATASET = os.getenv('SANITY_DATASET', 'production')
SANITY_API_TOKEN = os.getenv('SANITY_API_TOKEN')
SANITY_SAVE_EPISODES = os.getenv('SANITY_SAVE_EPISODES', 'true').lower() == 'true'

