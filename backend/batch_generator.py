"""Batch generator for creating multiple podcast episodes."""
import json
import time
from datetime import datetime
from podcast_generator import PodcastGenerator
import argparse


def load_topics_from_file(filepath):
    """Load topics from JSON file."""
    with open(filepath, 'r') as f:
        return json.load(f)


def save_episode(episode_data, output_dir='output'):
    """Save episode to file."""
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    topic_slug = episode_data['topic'][:30].replace(' ', '_').replace('/', '_')
    filename = f"{output_dir}/episode_{timestamp}_{topic_slug}.json"
    
    with open(filename, 'w') as f:
        json.dump(episode_data, f, indent=2)
    
    return filename


def generate_batch(topics, output_dir='output', delay=2):
    """
    Generate multiple podcast episodes in batch.
    
    Args:
        topics: List of topic dicts with 'topic', optional 'context', 'sponsor'
        output_dir: Directory to save output files
        delay: Delay between generations (seconds)
    
    Returns:
        List of results
    """
    generator = PodcastGenerator()
    results = []
    
    print(f"🎙️  Starting batch generation of {len(topics)} episodes")
    print("=" * 70)
    
    for i, topic_data in enumerate(topics, 1):
        print(f"\n[{i}/{len(topics)}] Processing: {topic_data['topic']}")
        print("-" * 70)
        
        try:
            # Generate episode
            result = generator.generate(
                topic=topic_data['topic'],
                real_world_context=topic_data.get('context'),
                force_sponsor=topic_data.get('sponsor')
            )
            
            # Add metadata
            result['generated_at'] = datetime.now().isoformat()
            result['batch_index'] = i
            
            # Save to file
            filepath = save_episode(result, output_dir)
            result['saved_to'] = filepath
            
            results.append({
                'success': True,
                'topic': topic_data['topic'],
                'sponsor': result['sponsor'],
                'filepath': filepath
            })
            
            print(f"✅ Generated successfully")
            print(f"   Sponsor: {result['sponsor']}")
            print(f"   Saved to: {filepath}")
            
            # Delay before next generation
            if i < len(topics):
                print(f"\n⏳ Waiting {delay}s before next generation...")
                time.sleep(delay)
        
        except Exception as e:
            print(f"❌ Error: {e}")
            results.append({
                'success': False,
                'topic': topic_data['topic'],
                'error': str(e)
            })
    
    print("\n" + "=" * 70)
    print("📊 Batch Generation Summary")
    print("=" * 70)
    
    successful = sum(1 for r in results if r['success'])
    failed = len(results) - successful
    
    print(f"Total: {len(results)}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    
    if successful > 0:
        print(f"\n✅ Episodes saved to: {output_dir}/")
    
    # Save summary
    summary_file = f"{output_dir}/batch_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(summary_file, 'w') as f:
        json.dump({
            'total': len(results),
            'successful': successful,
            'failed': failed,
            'results': results,
            'generated_at': datetime.now().isoformat()
        }, f, indent=2)
    
    print(f"📄 Summary saved to: {summary_file}")
    
    return results


def main():
    """CLI for batch generation."""
    parser = argparse.ArgumentParser(
        description='Batch generate podcast episodes'
    )
    parser.add_argument(
        'input_file',
        help='JSON file with topics (array of {topic, context?, sponsor?})'
    )
    parser.add_argument(
        '--output-dir',
        default='output',
        help='Output directory (default: output)'
    )
    parser.add_argument(
        '--delay',
        type=int,
        default=2,
        help='Delay between generations in seconds (default: 2)'
    )
    
    args = parser.parse_args()
    
    # Load topics
    try:
        topics = load_topics_from_file(args.input_file)
        if not isinstance(topics, list):
            print("❌ Error: Input file must contain an array of topics")
            return
    except Exception as e:
        print(f"❌ Error loading input file: {e}")
        return
    
    # Generate batch
    generate_batch(topics, args.output_dir, args.delay)


if __name__ == '__main__':
    main()


