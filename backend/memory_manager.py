"""Redis-based memory management for tracking sponsors and conversation patterns."""
import redis
import json
from typing import List, Dict, Optional
from config import REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_PASSWORD, MAX_SPONSOR_HISTORY, MAX_PHRASE_HISTORY, REDIS_VERBOSE_LOGGING


class MemoryManager:
    """Manages conversation memory using Redis."""
    
    def __init__(self, verbose: bool = None):
        """
        Initialize Redis connection.
        
        Args:
            verbose: Enable verbose logging. If None, uses REDIS_VERBOSE_LOGGING from config.
        """
        self.verbose = verbose if verbose is not None else REDIS_VERBOSE_LOGGING
        
        try:
            self.redis_client = redis.Redis(
                host=REDIS_HOST,
                port=REDIS_PORT,
                db=REDIS_DB,
                password=REDIS_PASSWORD if REDIS_PASSWORD else None,
                decode_responses=True
            )
            # Test connection
            self.redis_client.ping()
            self.connected = True
            if self.verbose:
                print("🗄️  Redis: Connected successfully")
        except (redis.ConnectionError, redis.TimeoutError):
            print("⚠️  Redis not available, using in-memory fallback")
            self.connected = False
            self.fallback_memory = {
                'sponsors': [],
                'phrases': [],
                'tone_patterns': []
            }
    
    def add_sponsor(self, sponsor: str) -> None:
        """Add a sponsor to recent history."""
        if self.connected:
            # Get before state
            before = self.redis_client.lrange('recent_sponsors', 0, -1)
            
            # Add new sponsor
            self.redis_client.lpush('recent_sponsors', sponsor)
            self.redis_client.ltrim('recent_sponsors', 0, MAX_SPONSOR_HISTORY - 1)
            
            # Get after state
            after = self.redis_client.lrange('recent_sponsors', 0, -1)
            
            if self.verbose:
                removed = before[-1] if len(before) >= MAX_SPONSOR_HISTORY else None
                print(f"🗄️  Redis: Added sponsor '{sponsor}'")
                print(f"   Before: {before if before else '[]'}")
                print(f"   After:  {after}")
                if removed and removed != sponsor:
                    print(f"   Removed: '{removed}' (oldest)")
        else:
            before = self.fallback_memory['sponsors'].copy()
            self.fallback_memory['sponsors'].insert(0, sponsor)
            self.fallback_memory['sponsors'] = self.fallback_memory['sponsors'][:MAX_SPONSOR_HISTORY]
            if self.verbose:
                print(f"🗄️  Memory: Added sponsor '{sponsor}' (fallback mode)")
                print(f"   Before: {before}")
                print(f"   After:  {self.fallback_memory['sponsors']}")
    
    def get_recent_sponsors(self) -> List[str]:
        """Get list of recently used sponsors."""
        if self.connected:
            sponsors = self.redis_client.lrange('recent_sponsors', 0, -1)
            if self.verbose:
                print(f"🗄️  Redis: Query recent sponsors → {sponsors if sponsors else '[]'}")
            return sponsors
        else:
            return self.fallback_memory['sponsors']
    
    def add_phrase(self, phrase: str) -> None:
        """Add a phrase to recent history to avoid repetition."""
        if self.connected:
            before_count = self.redis_client.llen('recent_phrases')
            self.redis_client.lpush('recent_phrases', phrase)
            self.redis_client.ltrim('recent_phrases', 0, MAX_PHRASE_HISTORY - 1)
            after_count = self.redis_client.llen('recent_phrases')
            
            if self.verbose:
                print(f"🗄️  Redis: Added phrase '{phrase[:50]}{'...' if len(phrase) > 50 else ''}'")
                print(f"   Phrases count: {before_count} → {after_count}")
        else:
            before_count = len(self.fallback_memory['phrases'])
            self.fallback_memory['phrases'].insert(0, phrase)
            self.fallback_memory['phrases'] = self.fallback_memory['phrases'][:MAX_PHRASE_HISTORY]
            after_count = len(self.fallback_memory['phrases'])
            if self.verbose:
                print(f"🗄️  Memory: Added phrase '{phrase[:50]}{'...' if len(phrase) > 50 else ''}' (fallback)")
                print(f"   Phrases count: {before_count} → {after_count}")
    
    def get_recent_phrases(self) -> List[str]:
        """Get list of recently used phrases."""
        if self.connected:
            return self.redis_client.lrange('recent_phrases', 0, -1)
        else:
            return self.fallback_memory['phrases']
    
    def add_tone_pattern(self, pattern: str) -> None:
        """Add a tone pattern to avoid repetitive conversation styles."""
        if self.connected:
            before_count = self.redis_client.llen('tone_patterns')
            self.redis_client.lpush('tone_patterns', pattern)
            self.redis_client.ltrim('tone_patterns', 0, 9)  # Keep last 10
            after_count = self.redis_client.llen('tone_patterns')
            
            if self.verbose:
                print(f"🗄️  Redis: Added tone pattern '{pattern[:50]}{'...' if len(pattern) > 50 else ''}'")
                print(f"   Patterns count: {before_count} → {after_count}")
        else:
            before_count = len(self.fallback_memory.get('tone_patterns', []))
            self.fallback_memory['tone_patterns'].insert(0, pattern)
            self.fallback_memory['tone_patterns'] = self.fallback_memory['tone_patterns'][:10]
            after_count = len(self.fallback_memory['tone_patterns'])
            if self.verbose:
                print(f"🗄️  Memory: Added tone pattern '{pattern[:50]}{'...' if len(pattern) > 50 else ''}' (fallback)")
                print(f"   Patterns count: {before_count} → {after_count}")
    
    def get_recent_tone_patterns(self) -> List[str]:
        """Get recent tone patterns."""
        if self.connected:
            return self.redis_client.lrange('tone_patterns', 0, -1)
        else:
            return self.fallback_memory.get('tone_patterns', [])
    
    def clear_all(self) -> None:
        """Clear all memory (useful for testing)."""
        if self.connected:
            if self.verbose:
                print("🗄️  Redis: Clearing all memory...")
            self.redis_client.delete('recent_sponsors', 'recent_phrases', 'tone_patterns')
            if self.verbose:
                print("🗄️  Redis: All memory cleared")
        else:
            if self.verbose:
                print("🗄️  Memory: Clearing all memory (fallback mode)...")
            self.fallback_memory = {
                'sponsors': [],
                'phrases': [],
                'tone_patterns': []
            }
            if self.verbose:
                print("🗄️  Memory: All memory cleared")
    
    def get_memory_summary(self) -> Dict:
        """Get a summary of current memory state."""
        return {
            'recent_sponsors': self.get_recent_sponsors(),
            'recent_phrases': self.get_recent_phrases(),
            'tone_patterns': self.get_recent_tone_patterns()
        }


