"""
Redis queue system for ElevenLabs API calls.
Alternates between Alex and Maya dialogues, processing them in parallel when possible.
"""
import redis
import json
import requests
import time
import os
from typing import Dict, List, Optional
from config import (
    REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_PASSWORD, REDIS_VERBOSE_LOGGING,
    ELEVENLABS_API_KEY, ELEVENLABS_VOICE_ID_ALEX, ELEVENLABS_VOICE_ID_MAYA, 
    ELEVENLABS_API_URL, ELEVENLABS_MODEL_ID
)


class ElevenLabsQueue:
    """
    Manages Redis queue for ElevenLabs text-to-speech generation.
    Alternates between Alex and Maya, processing in parallel when possible.
    """
    
    def __init__(self):
        """Initialize Redis connection and ElevenLabs queue."""
        self.redis_client = None
        try:
            self.redis_client = redis.Redis(
                host=REDIS_HOST,
                port=REDIS_PORT,
                db=REDIS_DB,
                password=REDIS_PASSWORD,
                decode_responses=True
            )
            self.redis_client.ping()
            if REDIS_VERBOSE_LOGGING:
                print("🗄️  Redis: Connected for ElevenLabs queue")
        except Exception as e:
            print(f"⚠️  Redis connection failed: {e}")
            self.redis_client = None
        
        self.api_key = ELEVENLABS_API_KEY
        self.voice_alex = ELEVENLABS_VOICE_ID_ALEX
        self.voice_maya = ELEVENLABS_VOICE_ID_MAYA
        
        if not self.api_key:
            print("⚠️  ElevenLabs API key not configured")
            print("   Set ELEVENLABS_API_KEY in .env file")
        else:
            if REDIS_VERBOSE_LOGGING:
                print(f"🎤 ElevenLabs: API key configured")
                print(f"   Alex voice: {self.voice_alex}")
                print(f"   Maya voice: {self.voice_maya}")
    
    def parse_conversation(self, conversation: str) -> List[Dict]:
        """
        Parse conversation into Alex and Maya dialogue segments.
        
        Args:
            conversation: Full conversation text with "Alex:" and "Maya:" lines
            
        Returns:
            List of dialogue dicts with 'speaker', 'text', 'index'
        """
        dialogues = []
        lines = conversation.split('\n')
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
            
            if line.startswith('Alex:'):
                text = line.replace('Alex:', '').strip()
                # Remove sponsor markers for audio generation
                text = text.replace('*sponsor*', '')
                dialogues.append({
                    'speaker': 'alex',
                    'text': text,
                    'index': len(dialogues)
                })
            elif line.startswith('Maya:'):
                text = line.replace('Maya:', '').strip()
                # Remove sponsor markers for audio generation
                text = text.replace('*sponsor*', '')
                dialogues.append({
                    'speaker': 'maya',
                    'text': text,
                    'index': len(dialogues)
                })
        
        return dialogues
    
    def queue_dialogues(self, conversation: str, episode_id: str) -> Dict:
        """
        Queue all dialogues from a conversation for ElevenLabs processing.
        
        Args:
            conversation: Full conversation text
            episode_id: Unique identifier for this episode
            
        Returns:
            Dict with queue status and dialogue count
        """
        if not self.redis_client:
            return {
                'success': False,
                'error': 'Redis not connected'
            }
        
        if not self.api_key:
            error_msg = 'ElevenLabs API key not configured. Set ELEVENLABS_API_KEY in .env file'
            print(f"❌ {error_msg}")
            return {
                'success': False,
                'error': error_msg
            }
        
        # Parse conversation into dialogues
        dialogues = self.parse_conversation(conversation)
        
        if not dialogues:
            return {
                'success': False,
                'error': 'No dialogues found in conversation'
            }
        
        # Queue each dialogue
        queued = []
        for dialogue in dialogues:
            queue_item = {
                'episode_id': episode_id,
                'speaker': dialogue['speaker'],
                'text': dialogue['text'],
                'index': dialogue['index'],
                'status': 'queued',
                'created_at': time.time()
            }
            
            # Use Redis list as queue (FIFO)
            queue_key = f"elevenlabs:queue:{episode_id}"
            self.redis_client.lpush(queue_key, json.dumps(queue_item))
            queued.append(queue_item)
            
            if REDIS_VERBOSE_LOGGING:
                print(f"📤 Queued {dialogue['speaker']} dialogue {dialogue['index']}: {dialogue['text'][:50]}...")
        
        # Store episode metadata
        episode_key = f"elevenlabs:episode:{episode_id}"
        self.redis_client.hset(episode_key, mapping={
            'total_dialogues': len(dialogues),
            'processed': '0',
            'status': 'queued',
            'created_at': str(time.time())
        })
        
        return {
            'success': True,
            'episode_id': episode_id,
            'total_dialogues': len(dialogues),
            'queued': len(queued)
        }
    
    def process_queue(self, episode_id: str, max_parallel: int = 2) -> Dict:
        """
        Process queued dialogues for an episode sequentially.
        Processes dialogues in order, alternating between Alex and Maya voices.
        
        Args:
            episode_id: Episode identifier
            max_parallel: Not used (kept for compatibility)
            
        Returns:
            Dict with processing status and audio files
        """
        if not self.redis_client or not self.api_key:
            return {
                'success': False,
                'error': 'Redis or ElevenLabs not configured'
            }
        
        queue_key = f"elevenlabs:queue:{episode_id}"
        episode_key = f"elevenlabs:episode:{episode_id}"
        
        # Get all queued items (they're stored in order)
        queue_items = []
        # Read all items without removing them first
        all_items = self.redis_client.lrange(queue_key, 0, -1)
        for item_json in all_items:
            queue_items.append(json.loads(item_json))
        
        # Now remove them from queue
        self.redis_client.delete(queue_key)
        
        if not queue_items:
            return {
                'success': False,
                'error': 'No items in queue'
            }
        
        # Sort by index to maintain order
        queue_items.sort(key=lambda x: x['index'])
        
        processed = []
        failed = []
        
        # Process dialogues sequentially
        for item in queue_items:
            speaker = item['speaker']
            text = item['text']
            
            # Determine voice based on speaker
            voice_id = self.voice_alex if speaker == 'alex' else self.voice_maya
            
            if REDIS_VERBOSE_LOGGING:
                print(f"🎤 Processing {speaker} dialogue {item['index']}...")
            
            result = self._call_elevenlabs(text, voice_id, item['index'], episode_id)
            
            if result['success']:
                processed.append(result)
            else:
                failed.append(result)
            
            # Update episode status
            self.redis_client.hset(episode_key, 'processed', str(len(processed)))
        
        # Mark as completed
        self.redis_client.hset(episode_key, 'status', 'completed')
        
        return {
            'success': True,
            'processed': len(processed),
            'failed': len(failed),
            'total': len(queue_items),
            'audio_files': [p.get('audio_file') for p in processed if p.get('audio_file')]
        }
    
    def _call_elevenlabs(self, text: str, voice_id: str, index: int, episode_id: str) -> Dict:
        """
        Call ElevenLabs API for text-to-speech.
        
        Args:
            text: Text to convert to speech
            voice_id: ElevenLabs voice ID
            index: Dialogue index
            episode_id: Episode identifier
            
        Returns:
            Dict with success status and audio URL/path
        """
        if not self.api_key:
            return {
                'success': False,
                'error': 'API key not configured'
            }
        
        url = f"{ELEVENLABS_API_URL}/{voice_id}"
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": self.api_key
        }
        
        data = {
            "text": text,
            "model_id": ELEVENLABS_MODEL_ID,  # Uses config value (default: eleven_turbo_v2)
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5
            }
        }
        
        try:
            if REDIS_VERBOSE_LOGGING:
                print(f"🎤 Calling ElevenLabs for dialogue {index} (voice: {voice_id[:8]}...)")
            
            response = requests.post(url, json=data, headers=headers, timeout=30)
            
            if response.status_code == 200:
                # Save audio to file - use absolute path
                audio_dir = os.path.join(os.path.dirname(__file__), '..', 'audio')
                os.makedirs(audio_dir, exist_ok=True)
                audio_filename = f"{episode_id}_dialogue_{index}.mp3"
                audio_path = os.path.join(audio_dir, audio_filename)
                
                with open(audio_path, 'wb') as f:
                    f.write(response.content)
                
                if REDIS_VERBOSE_LOGGING:
                    print(f"✅ Generated audio: {audio_filename}")
                
                return {
                    'success': True,
                    'audio_file': audio_filename,  # Just filename for URL
                    'index': index,
                    'episode_id': episode_id
                }
            else:
                error_msg = f"HTTP {response.status_code}: {response.text[:100]}"
                if REDIS_VERBOSE_LOGGING:
                    print(f"❌ ElevenLabs API error: {error_msg}")
                return {
                    'success': False,
                    'error': error_msg,
                    'index': index
                }
        
        except Exception as e:
            if REDIS_VERBOSE_LOGGING:
                print(f"❌ ElevenLabs request failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'index': index
            }
    
    def get_queue_status(self, episode_id: str) -> Dict:
        """Get current queue status for an episode."""
        if not self.redis_client:
            return {'error': 'Redis not connected'}
        
        episode_key = f"elevenlabs:episode:{episode_id}"
        queue_key = f"elevenlabs:queue:{episode_id}"
        
        episode_data = self.redis_client.hgetall(episode_key)
        queue_length = self.redis_client.llen(queue_key)
        
        return {
            'episode_id': episode_id,
            'status': episode_data.get('status', 'unknown'),
            'processed': int(episode_data.get('processed', 0)),
            'total': int(episode_data.get('total_dialogues', 0)),
            'queued': queue_length
        }


if __name__ == "__main__":
    # Test the queue system
    queue = ElevenLabsQueue()
    
    test_conversation = """Alex: I've been thinking about AI and creativity lately.
Maya: That's a fascinating topic. What specifically interests you?
Alex: Well, I've been using *sponsor*Notion*sponsor* for my project management and it's been great.
Maya: From a technical standpoint, AI systems have seen significant growth."""
    
    result = queue.queue_dialogues(test_conversation, "test-episode-001")
    print(f"Queue result: {result}")

