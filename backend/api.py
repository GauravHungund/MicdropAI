"""Simple Flask API wrapper for EchoDuo."""
from flask import Flask, request, jsonify
from flask_cors import CORS
from podcast_generator import PodcastGenerator
from memory_manager import MemoryManager
import traceback

app = Flask(__name__)
CORS(app)

# Initialize generator
generator = PodcastGenerator()


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
        
        return jsonify({
            'success': True,
            'data': {
                'conversation': result['conversation'],
                'sponsor': result['sponsor'],
                'topic': result['topic'],
                'context_snippet': result['context_used']
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


if __name__ == '__main__':
    print("🎙️  Starting EchoDuo API Server...")
    print("📡 Endpoints:")
    print("   POST /generate - Generate podcast")
    print("   GET  /memory - View memory state")
    print("   POST /memory/clear - Clear memory")
    print("   GET  /sponsors - List available sponsors")
    print("   GET  /health - Health check")
    print()
    app.run(host='0.0.0.0', port=5000, debug=True)


