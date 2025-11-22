"""
Redis queue system for topic generation.
Manages sequential topic generation with status tracking and confirmations.
"""
import redis
import json
import time
import uuid
from typing import Dict, List, Optional
from config import (
    REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_PASSWORD, REDIS_VERBOSE_LOGGING
)


class TopicQueue:
    """
    Manages Redis queue for sequential topic generation.
    Handles status tracking, results storage, and confirmations.
    """
    
    def __init__(self):
        """Initialize Redis connection for topic queue."""
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
                print("🗄️  Redis: Connected for topic queue")
        except Exception as e:
            print(f"⚠️  Redis connection failed: {e}")
            self.redis_client = None
    
    def create_sequence(self, topics: List[str], sponsors: List[str] = None) -> str:
        """
        Create a new sequence for topic generation.
        
        Args:
            topics: List of topics to generate
            sponsors: Optional list of sponsors
            
        Returns:
            Sequence ID
        """
        if not self.redis_client:
            raise Exception("Redis not connected")
        
        sequence_id = f"seq-{uuid.uuid4().hex[:12]}"
        
        # Store sequence metadata
        sequence_key = f"topic:sequence:{sequence_id}"
        self.redis_client.hset(sequence_key, mapping={
            'total_topics': len(topics),
            'created_at': str(time.time()),
            'status': 'pending'
        })
        
        # Store topics and sponsors
        self.redis_client.set(f"{sequence_key}:topics", json.dumps(topics))
        if sponsors:
            self.redis_client.set(f"{sequence_key}:sponsors", json.dumps(sponsors))
        
        # Initialize status for all topics
        status_key = f"topic:status:{sequence_id}"
        for i in range(len(topics)):
            self.redis_client.hset(status_key, str(i), 'pending')
        
        # Set expiration (24 hours)
        self.redis_client.expire(sequence_key, 86400)
        self.redis_client.expire(status_key, 86400)
        self.redis_client.expire(f"{sequence_key}:topics", 86400)
        if sponsors:
            self.redis_client.expire(f"{sequence_key}:sponsors", 86400)
        
        if REDIS_VERBOSE_LOGGING:
            print(f"📋 Created sequence {sequence_id} with {len(topics)} topics")
        
        return sequence_id
    
    def get_sequence_info(self, sequence_id: str) -> Optional[Dict]:
        """Get sequence information."""
        if not self.redis_client:
            return None
        
        sequence_key = f"topic:sequence:{sequence_id}"
        if not self.redis_client.exists(sequence_key):
            return None
        
        info = self.redis_client.hgetall(sequence_key)
        topics_json = self.redis_client.get(f"{sequence_key}:topics")
        sponsors_json = self.redis_client.get(f"{sequence_key}:sponsors")
        
        try:
            topics = json.loads(topics_json) if topics_json else []
        except:
            topics = []
        
        try:
            sponsors = json.loads(sponsors_json) if sponsors_json else []
        except:
            sponsors = []
        
        return {
            'sequence_id': sequence_id,
            'total_topics': int(info.get('total_topics', 0)),
            'created_at': info.get('created_at'),
            'status': info.get('status', 'pending'),
            'topics': topics,
            'sponsors': sponsors
        }
    
    def set_topic_status(self, sequence_id: str, topic_index: int, status: str):
        """Set status for a topic."""
        if not self.redis_client:
            return
        
        status_key = f"topic:status:{sequence_id}"
        self.redis_client.hset(status_key, str(topic_index), status)
        self.redis_client.expire(status_key, 86400)
    
    def get_topic_status(self, sequence_id: str, topic_index: int) -> Optional[str]:
        """Get status for a topic."""
        if not self.redis_client:
            return None
        
        status_key = f"topic:status:{sequence_id}"
        return self.redis_client.hget(status_key, str(topic_index))
    
    def get_all_statuses(self, sequence_id: str) -> Dict[int, str]:
        """Get all topic statuses for a sequence."""
        if not self.redis_client:
            return {}
        
        status_key = f"topic:status:{sequence_id}"
        statuses = self.redis_client.hgetall(status_key)
        return {int(k): v for k, v in statuses.items()}
    
    def set_topic_result(self, sequence_id: str, topic_index: int, result: Dict):
        """Store result for a topic."""
        if not self.redis_client:
            return
        
        result_key = f"topic:result:{sequence_id}"
        self.redis_client.hset(result_key, str(topic_index), json.dumps(result))
        self.redis_client.expire(result_key, 86400)
    
    def get_topic_result(self, sequence_id: str, topic_index: int) -> Optional[Dict]:
        """Get result for a topic."""
        if not self.redis_client:
            return None
        
        result_key = f"topic:result:{sequence_id}"
        result_json = self.redis_client.hget(result_key, str(topic_index))
        if result_json:
            return json.loads(result_json)
        return None
    
    def get_all_results(self, sequence_id: str) -> Dict[int, Dict]:
        """Get all topic results for a sequence."""
        if not self.redis_client:
            return {}
        
        result_key = f"topic:result:{sequence_id}"
        results = self.redis_client.hgetall(result_key)
        return {int(k): json.loads(v) for k, v in results.items()}
    
    def confirm_topic(self, sequence_id: str, topic_index: int):
        """Mark a topic as confirmed by frontend."""
        if not self.redis_client:
            return
        
        confirmation_key = f"topic:confirmation:{sequence_id}"
        self.redis_client.hset(confirmation_key, str(topic_index), 'true')
        self.redis_client.expire(confirmation_key, 86400)
    
    def is_topic_confirmed(self, sequence_id: str, topic_index: int) -> bool:
        """Check if a topic is confirmed."""
        if not self.redis_client:
            return False
        
        confirmation_key = f"topic:confirmation:{sequence_id}"
        confirmed = self.redis_client.hget(confirmation_key, str(topic_index))
        return confirmed == 'true'
    
    def get_sequence_status(self, sequence_id: str) -> Dict:
        """
        Get complete status for a sequence.
        
        Returns:
            Dict with status, results, and completion status
        """
        if not self.redis_client:
            return {'error': 'Redis not connected'}
        
        sequence_info = self.get_sequence_info(sequence_id)
        if not sequence_info:
            return {'error': 'Sequence not found'}
        
        statuses = self.get_all_statuses(sequence_id)
        results = self.get_all_results(sequence_id)
        
        # Build results dict
        results_dict = {}
        for i in range(sequence_info['total_topics']):
            status = statuses.get(i, 'pending')
            if status in ['ready', 'sent']:
                topic_result = results.get(i)
                # Ensure we have data even if result is None
                if topic_result is None:
                    # Try to get it again (might be a race condition)
                    topic_result = self.get_topic_result(sequence_id, i)
                    # If still None, try one more time after a brief wait
                    if topic_result is None:
                        import time
                        time.sleep(0.1)
                        topic_result = self.get_topic_result(sequence_id, i)
                
                # Only include in results if we have actual data
                if topic_result:
                    results_dict[i] = {
                        'status': status,
                        'data': topic_result
                    }
                else:
                    # Status is ready but data not available yet
                    results_dict[i] = {
                        'status': status
                    }
            elif status == 'error':
                error_result = results.get(i, {})
                if isinstance(error_result, dict):
                    error_msg = error_result.get('error', 'Unknown error')
                else:
                    error_msg = str(error_result) if error_result else 'Unknown error'
                results_dict[i] = {
                    'status': 'error',
                    'error': error_msg
                }
            else:
                results_dict[i] = {
                    'status': status
                }
        
        # Check if all complete
        all_complete = all(
            statuses.get(i) in ['ready', 'sent', 'error']
            for i in range(sequence_info['total_topics'])
        )
        
        return {
            'sequence_id': sequence_id,
            'status': statuses,
            'results': results_dict,
            'complete': all_complete
        }
    
    def cleanup_sequence(self, sequence_id: str):
        """Clean up all keys for a sequence."""
        if not self.redis_client:
            return
        
        keys = [
            f"topic:sequence:{sequence_id}",
            f"topic:sequence:{sequence_id}:topics",
            f"topic:sequence:{sequence_id}:sponsors",
            f"topic:status:{sequence_id}",
            f"topic:result:{sequence_id}",
            f"topic:confirmation:{sequence_id}"
        ]
        
        for key in keys:
            self.redis_client.delete(key)
        
        if REDIS_VERBOSE_LOGGING:
            print(f"🧹 Cleaned up sequence {sequence_id}")

