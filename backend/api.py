"""Simple Flask API wrapper for EchoDuo."""
from flask import Flask, request, jsonify, send_from_directory, Response, stream_with_context
from flask_cors import CORS
from podcast_generator import PodcastGenerator
from memory_manager import MemoryManager
import traceback
import os
import threading
import queue
import uuid
import json
import time

app = Flask(__name__)
CORS(app)

# Ensure audio directory exists
AUDIO_DIR = os.path.join(os.path.dirname(__file__), '..', 'audio')
os.makedirs(AUDIO_DIR, exist_ok=True)

# Initialize generator
generator = PodcastGenerator()

# Initialize Redis-based topic queue
try:
    from topic_queue import TopicQueue
    topic_queue = TopicQueue()
    print("✅ Topic queue: Redis-based queue initialized")
except Exception as e:
    print(f"⚠️  Topic queue initialization failed: {e}")
    topic_queue = None


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'service': 'EchoDuo API',
        'version': '1.0.0'
    })


@app.route('/generate', methods=['POST'])
def generate_podcast():
    """
    Generate a podcast episode.
    
    Request body:
    {
        "topic": "string (required)",
        "context": "string (optional)",
        "sponsor": "string (optional)"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'topic' not in data:
            return jsonify({
                'error': 'Missing required field: topic'
            }), 400
        
        topic = data['topic']
        context = data.get('context')
        sponsor = data.get('sponsor')
        
        # Validate sponsor if provided
        if sponsor:
            from config import AVAILABLE_SPONSORS
            if sponsor not in AVAILABLE_SPONSORS:
                return jsonify({
                    'error': f'Invalid sponsor. Must be one of: {", ".join(AVAILABLE_SPONSORS)}'
                }), 400
        
        # Generate podcast
        result = generator.generate(
            topic=topic,
            real_world_context=context,
            force_sponsor=sponsor
        )
        
        # Queue and process dialogues for ElevenLabs if configured
        audio_files = []
        elevenlabs_queued = False
        elevenlabs_error = None
        episode_id = None
        
        try:
            from elevenlabs_queue import ElevenLabsQueue
            from config import ELEVENLABS_API_KEY
            import uuid
            import os
            
            if ELEVENLABS_API_KEY:
                queue_manager = ElevenLabsQueue()
                episode_id = f"episode-{uuid.uuid4().hex[:12]}"
                
                # Queue dialogues
                queue_result = queue_manager.queue_dialogues(
                    result['conversation'],
                    episode_id
                )
                
                if queue_result.get('success'):
                    elevenlabs_queued = True
                    total_dialogues = queue_result.get('total_dialogues', 0)
                    print(f"🎤 Queued {total_dialogues} dialogues for ElevenLabs")
                    
                    # Process queue to generate audio files
                    print(f"🎵 Processing audio generation...")
                    process_result = queue_manager.process_queue(episode_id)
                    
                    if process_result.get('success'):
                        processed_count = process_result.get('processed', 0)
                        print(f"✅ Generated {processed_count} audio files")
                        
                        # Get audio files from process result
                        generated_files = process_result.get('audio_files', [])
                        for audio_file in generated_files:
                            # audio_file is just the filename, add /audio/ prefix
                            if audio_file:
                                audio_files.append(f"/audio/{audio_file}")
                        
                        # Fallback: check files directly if not in result
                        if not audio_files:
                            for i in range(total_dialogues):
                                audio_filename = f"{episode_id}_dialogue_{i}.mp3"
                                audio_path = os.path.join(AUDIO_DIR, audio_filename)
                                if os.path.exists(audio_path):
                                    audio_files.append(f"/audio/{audio_filename}")
                    else:
                        elevenlabs_error = process_result.get('error', 'Processing failed')
                        print(f"⚠️  Audio processing failed: {elevenlabs_error}")
                else:
                    elevenlabs_error = queue_result.get('error', 'Unknown error')
                    print(f"⚠️  ElevenLabs queue failed: {elevenlabs_error}")
            else:
                print("ℹ️  ElevenLabs API key not configured, skipping audio generation")
        except Exception as e:
            elevenlabs_error = str(e)
            print(f"⚠️  ElevenLabs queue failed: {e}")
            import traceback
            traceback.print_exc()
        
        return jsonify({
            'success': True,
            'data': {
                'conversation': result['conversation'],
                'sponsor': result['sponsor'],
                'topic': result['topic'],
                'context_snippet': result['context_used'],
                'elevenlabs_queued': elevenlabs_queued,
                'audio_files': audio_files,
                'episode_id': episode_id
            }
        })
    
    except Exception as e:
        traceback.print_exc()
        return jsonify({
            'error': str(e),
            'type': type(e).__name__
        }), 500


@app.route('/memory', methods=['GET'])
def get_memory():
    """Get current memory state."""
    try:
        memory = generator.memory.get_memory_summary()
        return jsonify({
            'success': True,
            'data': memory
        })
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500


@app.route('/memory/clear', methods=['POST'])
def clear_memory():
    """Clear all memory."""
    try:
        generator.memory.clear_all()
        return jsonify({
            'success': True,
            'message': 'Memory cleared successfully'
        })
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500


@app.route('/sponsors', methods=['GET'])
def get_sponsors():
    """Get list of available sponsors."""
    from config import AVAILABLE_SPONSORS
    return jsonify({
        'success': True,
        'sponsors': AVAILABLE_SPONSORS
    })


@app.route('/audio/<path:filename>', methods=['GET'])
def serve_audio(filename):
    """Serve audio files."""
    try:
        return send_from_directory(AUDIO_DIR, filename)
    except Exception as e:
        return jsonify({'error': str(e)}), 404


def generate_topic_worker(sequence_id, topic_index, topic, sponsors, previous_script=None, wait_for_confirmation=False):
    """Worker function to generate a single topic."""
    try:
        # Wait for confirmation if needed (for topic 3+)
        if wait_for_confirmation and topic_index > 1:
            prev_index = topic_index - 1
            print(f"⏳ [Sequence {sequence_id}] Waiting for topic {prev_index + 1} confirmation...")
            max_wait = 300  # 5 minutes max wait
            waited = 0
            while waited < max_wait:
                if topic_queue and topic_queue.is_topic_confirmed(sequence_id, prev_index):
                    print(f"✅ [Sequence {sequence_id}] Topic {prev_index + 1} confirmed, proceeding...")
                    break
                time.sleep(1)
                waited += 1
            if waited >= max_wait:
                print(f"⚠️  [Sequence {sequence_id}] Timeout waiting for confirmation, proceeding anyway...")
        
        print(f"🎙️  [Sequence {sequence_id}] Starting topic {topic_index + 1}: {topic}")
        if topic_queue:
            topic_queue.set_topic_status(sequence_id, topic_index, 'generating')
        
        # Select sponsor if available
        sponsor = None
        if sponsors and topic_index < len(sponsors):
            sponsor = sponsors[topic_index]
            print(f"🎯 [Sequence {sequence_id}] Using sponsor from list: {sponsor}")
        elif sponsors and len(sponsors) > 0:
            sponsor = sponsors[0]  # Reuse first sponsor if not enough sponsors
            print(f"🎯 [Sequence {sequence_id}] Reusing first sponsor: {sponsor}")
        else:
            print(f"🎯 [Sequence {sequence_id}] No sponsor provided, will be auto-selected")
        
        # Generate podcast with previous script as context for continuation
        result = generator.generate(
            topic=topic,
            real_world_context=None,  # Will be scraped
            force_sponsor=sponsor,
            previous_script=previous_script,
            sequence_id=sequence_id,
            sequence_index=topic_index
        )
        
        # Process audio files
        audio_files = []
        episode_id = None
        
        try:
            from elevenlabs_queue import ElevenLabsQueue
            from config import ELEVENLABS_API_KEY
            
            if ELEVENLABS_API_KEY:
                queue_manager = ElevenLabsQueue()
                episode_id = f"episode-{sequence_id}-{topic_index}"
                
                queue_result = queue_manager.queue_dialogues(
                    result['conversation'],
                    episode_id
                )
                
                if queue_result.get('success'):
                    process_result = queue_manager.process_queue(episode_id)
                    
                    if process_result.get('success'):
                        generated_files = process_result.get('audio_files', [])
                        for audio_file in generated_files:
                            if audio_file:
                                audio_files.append(f"/audio/{audio_file}")
                        
                        if not audio_files:
                            for i in range(queue_result.get('total_dialogues', 0)):
                                audio_filename = f"{episode_id}_dialogue_{i}.mp3"
                                audio_path = os.path.join(AUDIO_DIR, audio_filename)
                                if os.path.exists(audio_path):
                                    audio_files.append(f"/audio/{audio_filename}")
        except Exception as e:
            print(f"⚠️  Audio generation failed for topic {topic_index + 1}: {e}")
        
        # Store result
        topic_data = {
            'conversation': result['conversation'],
            'sponsor': result['sponsor'],
            'topic': result['topic'],
            'context_snippet': result['context_used'],
            'elevenlabs_queued': len(audio_files) > 0,
            'audio_files': audio_files,
            'episode_id': episode_id
        }
        
        if topic_queue:
            # Store result first, then set status to ensure data is available
            topic_queue.set_topic_result(sequence_id, topic_index, topic_data)
            # Small delay to ensure Redis write completes
            time.sleep(0.1)
            topic_queue.set_topic_status(sequence_id, topic_index, 'ready')
            print(f"✅ [Sequence {sequence_id}] Topic {topic_index + 1} ready - Sponsor: {result['sponsor']}")
        else:
            print(f"✅ [Sequence {sequence_id}] Topic {topic_index + 1} ready (no queue) - Sponsor: {result['sponsor']}")
        
    except Exception as e:
        print(f"❌ [Sequence {sequence_id}] Topic {topic_index + 1} failed: {e}")
        traceback.print_exc()
        if topic_queue:
            topic_queue.set_topic_status(sequence_id, topic_index, 'error')
            topic_queue.set_topic_result(sequence_id, topic_index, {'error': str(e)})
        topic_status[sequence_id][topic_index] = 'error'
        topic_results[sequence_id][topic_index] = {'error': str(e)}


@app.route('/generate-sequence', methods=['POST'])
def generate_sequence():
    """
    Generate multiple podcast episodes sequentially.
    
    Request body:
    {
        "topics": ["topic1", "topic2", ...],
        "sponsors": ["sponsor1", "sponsor2", ...] (optional)
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'topics' not in data:
            return jsonify({
                'error': 'Missing required field: topics'
            }), 400
        
        topics = data['topics']
        sponsors = data.get('sponsors', [])
        
        if not isinstance(topics, list) or len(topics) == 0:
            return jsonify({
                'error': 'topics must be a non-empty array'
            }), 400
        
        if not topic_queue:
            return jsonify({
                'error': 'Topic queue not available (Redis not connected)'
            }), 500
        
        # Create sequence in Redis
        sequence_id = topic_queue.create_sequence(topics, sponsors)
        
        # Start generating first topic immediately
        print(f"🚀 Starting sequence {sequence_id} with {len(topics)} topics")
        # Retrieve sponsors from Redis to ensure consistency
        seq_info = topic_queue.get_sequence_info(sequence_id) if topic_queue else None
        redis_sponsors = seq_info.get('sponsors', []) if seq_info else (sponsors or [])
        if redis_sponsors:
            print(f"📋 Using sponsors from Redis: {redis_sponsors}")
        else:
            print(f"📋 No sponsors in Redis, using provided: {sponsors}")
            redis_sponsors = sponsors or []
        thread = threading.Thread(
            target=generate_topic_worker,
            args=(sequence_id, 0, topics[0], redis_sponsors, None, False)
        )
        thread.daemon = True
        thread.start()
        
        # Start topic 2 immediately after topic 1 (don't wait)
        if len(topics) > 1:
            def start_topic_2():
                # Wait for topic 1 to be ready
                max_wait = 300
                waited = 0
                while waited < max_wait:
                    if topic_queue and topic_queue.get_topic_status(sequence_id, 0) == 'ready':
                        # Get topic 1 script for continuation
                        result = topic_queue.get_topic_result(sequence_id, 0)
                        prev_script = result.get('conversation', '') if result else ''
                        # Get sponsors from Redis
                        seq_info = topic_queue.get_sequence_info(sequence_id)
                        redis_sponsors = seq_info.get('sponsors', []) if seq_info else sponsors
                        thread2 = threading.Thread(
                            target=generate_topic_worker,
                            args=(sequence_id, 1, topics[1], redis_sponsors, prev_script, False)
                        )
                        thread2.daemon = True
                        thread2.start()
                        break
                    time.sleep(0.5)
                    waited += 0.5
            
            thread_t2 = threading.Thread(target=start_topic_2)
            thread_t2.daemon = True
            thread_t2.start()
        
        # Start topics 3+ after confirmation
        if len(topics) > 2:
            def start_remaining_topics():
                for i in range(2, len(topics)):
                    # Wait for previous topic confirmation
                    prev_index = i - 1
                    max_wait = 300
                    waited = 0
                    while waited < max_wait:
                        if topic_queue and topic_queue.is_topic_confirmed(sequence_id, prev_index):
                            # Get previous script
                            result = topic_queue.get_topic_result(sequence_id, prev_index)
                            prev_script = result.get('conversation', '') if result else ''
                            # Get sponsors from Redis
                            seq_info = topic_queue.get_sequence_info(sequence_id)
                            redis_sponsors = seq_info.get('sponsors', []) if seq_info else sponsors
                            thread_n = threading.Thread(
                                target=generate_topic_worker,
                                args=(sequence_id, i, topics[i], redis_sponsors, prev_script, True)
                            )
                            thread_n.daemon = True
                            thread_n.start()
                            break
                        time.sleep(0.5)
                        waited += 0.5
            
            thread_remaining = threading.Thread(target=start_remaining_topics)
            thread_remaining.daemon = True
            thread_remaining.start()
        
        return jsonify({
            'success': True,
            'sequence_id': sequence_id,
            'total_topics': len(topics)
        })
    
    except Exception as e:
        traceback.print_exc()
        return jsonify({
            'error': str(e),
            'type': type(e).__name__
        }), 500


@app.route('/generate-sequence-stream', methods=['GET'])
def generate_sequence_stream():
    """
    Stream results for a sequence using Server-Sent Events.
    Query params: sequence_id, topics (JSON), sponsors (JSON)
    """
    try:
        sequence_id = request.args.get('sequence_id')
        topics_json = request.args.get('topics', '[]')
        sponsors_json = request.args.get('sponsors', '[]')
        
        try:
            topics = json.loads(topics_json)
            sponsors = json.loads(sponsors_json) if sponsors_json else []
        except:
            return jsonify({'error': 'Invalid JSON in query params'}), 400
        
        if not sequence_id:
            # Create new sequence
            sequence_id = f"seq-{uuid.uuid4().hex[:12]}"
            topic_status[sequence_id] = {i: 'pending' for i in range(len(topics))}
            topic_results[sequence_id] = {}
            topic_confirmations[sequence_id] = {}
            
            # Start first topic
            thread = threading.Thread(
                target=generate_topic_worker,
                args=(sequence_id, 0, topics[0], sponsors, None)
            )
            thread.daemon = True
            thread.start()
        
        def generate():
            previous_script = None
            next_topic_index = 1
            
            while True:
                # Check current topic status
                for topic_index in range(len(topics)):
                    status = topic_status.get(sequence_id, {}).get(topic_index, 'pending')
                    
                    if status == 'ready' and topic_index < next_topic_index:
                        # Topic is ready, send it
                        result = topic_results[sequence_id][topic_index]
                        topic_status[sequence_id][topic_index] = 'sent'
                        
                        yield f"data: {json.dumps({'type': 'topic_complete', 'data': result, 'index': topic_index})}\n\n"
                        
                        # Start next topic if not the last one
                        if topic_index == 0 and next_topic_index < len(topics):
                            # Start topic 2 immediately after topic 1 is ready
                            thread = threading.Thread(
                                target=generate_topic_worker,
                                args=(sequence_id, next_topic_index, topics[next_topic_index], sponsors, previous_script)
                            )
                            thread.daemon = True
                            thread.start()
                            next_topic_index += 1
                        elif topic_index > 0 and next_topic_index < len(topics):
                            # For topic 3+, wait for confirmation
                            if topic_confirmations.get(sequence_id, {}).get(topic_index - 1, False):
                                previous_script = topic_results[sequence_id][topic_index - 1].get('conversation', '')
                                thread = threading.Thread(
                                    target=generate_topic_worker,
                                    args=(sequence_id, next_topic_index, topics[next_topic_index], sponsors, previous_script)
                                )
                                thread.daemon = True
                                thread.start()
                                next_topic_index += 1
                    
                    elif status == 'error':
                        yield f"data: {json.dumps({'type': 'error', 'error': topic_results[sequence_id].get(topic_index, {}).get('error', 'Unknown error'), 'index': topic_index})}\n\n"
                
                # Check if all done
                all_done = all(
                    topic_status.get(sequence_id, {}).get(i) in ['ready', 'sent', 'error']
                    for i in range(len(topics))
                )
                
                if all_done:
                    yield f"data: {json.dumps({'type': 'sequence_complete'})}\n\n"
                    break
                
                time.sleep(0.5)  # Poll every 500ms
        
        return Response(stream_with_context(generate()), mimetype='text/event-stream')
    
    except Exception as e:
        traceback.print_exc()
        return jsonify({
            'error': str(e),
            'type': type(e).__name__
        }), 500


@app.route('/confirm-topic', methods=['POST'])
def confirm_topic():
    """
    Confirm that a topic was received by the frontend.
    This allows the backend to proceed with the next topic.
    """
    try:
        data = request.get_json()
        sequence_id = data.get('sequence_id')
        topic_index = data.get('topic_index')
        
        if not topic_queue:
            return jsonify({'error': 'Topic queue not available'}), 500
        
        if sequence_id and topic_index is not None:
            topic_queue.confirm_topic(sequence_id, topic_index)
            print(f"✅ [Sequence {sequence_id}] Topic {topic_index + 1} confirmed")
        
        return jsonify({'success': True})
    
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500


@app.route('/sequence-status/<sequence_id>', methods=['GET'])
def get_sequence_status(sequence_id):
    """
    Get status of a sequence generation.
    """
    try:
        if not topic_queue:
            return jsonify({'error': 'Topic queue not available'}), 500
        
        status = topic_queue.get_sequence_status(sequence_id)
        
        if 'error' in status:
            return jsonify(status), 404
        
        return jsonify(status)
    
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500


if __name__ == '__main__':
    print("🎙️  Starting EchoDuo API Server...")
    print("📡 Endpoints:")
    print("   POST /generate - Generate podcast")
    print("   GET  /memory - View memory state")
    print("   POST /memory/clear - Clear memory")
    print("   GET  /sponsors - List available sponsors")
    print("   GET  /health - Health check")
    print()
    app.run(host='0.0.0.0', port=5001, debug=True)


