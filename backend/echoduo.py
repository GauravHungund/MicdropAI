"""EchoDuo - Main entry point for the autonomous podcast generation system."""
import argparse
from podcast_generator import PodcastGenerator
from memory_manager import MemoryManager


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description='EchoDuo - Autonomous AI Podcast Generator'
    )
    parser.add_argument(
        'topic',
        type=str,
        help='The podcast topic to discuss'
    )
    parser.add_argument(
        '--context',
        type=str,
        default=None,
        help='Optional: Provide real-world context directly'
    )
    parser.add_argument(
        '--sponsor',
        type=str,
        default=None,
        help='Optional: Force a specific sponsor (Calm, Nike, Notion, Coder, Forethought, Skyflow)'
    )
    parser.add_argument(
        '--clear-memory',
        action='store_true',
        help='Clear all memory before generating'
    )
    parser.add_argument(
        '--show-memory',
        action='store_true',
        help='Show current memory state'
    )
    
    args = parser.parse_args()
    
    # Initialize generator
    generator = PodcastGenerator()
    
    # Handle memory operations
    if args.clear_memory:
        print("🗑️  Clearing memory...")
        generator.memory.clear_all()
        print("✅ Memory cleared")
        return
    
    if args.show_memory:
        print("🧠 Current Memory State:")
        memory = generator.memory.get_memory_summary()
        print(f"Recent Sponsors: {memory['recent_sponsors']}")
        print(f"Recent Phrases: {memory['recent_phrases'][:5]}")
        print(f"Tone Patterns: {memory['tone_patterns']}")
        return
    
    # Generate podcast
    print("=" * 60)
    print("🎙️  ECHODUO - AI Podcast Generator")
    print("=" * 60)
    print()
    
    result = generator.generate(
        topic=args.topic,
        real_world_context=args.context,
        force_sponsor=args.sponsor
    )
    
    print()
    print("=" * 60)
    print("🎧 FINAL PODCAST")
    print("=" * 60)
    print()
    print(result['conversation'])
    print()
    print("=" * 60)
    print(f"✨ Episode Info:")
    print(f"   Topic: {result['topic']}")
    print(f"   Sponsor: {result['sponsor']}")
    print("=" * 60)


if __name__ == '__main__':
    main()


