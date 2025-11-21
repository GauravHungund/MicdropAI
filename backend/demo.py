"""Quick demo of EchoDuo capabilities."""
from podcast_generator import PodcastGenerator
import sys


def run_demo():
    """Run a quick demo of EchoDuo."""
    print("=" * 70)
    print("🎙️  ECHODUO DEMO - Autonomous AI Podcast Generator")
    print("=" * 70)
    print()
    
    # Demo scenarios
    scenarios = [
        {
            'topic': 'AI taking over jobs',
            'context': 'Reports show 27% of repetitive roles were automated in the last year. McKinsey predicts 30% of work hours could be automated by 2030.',
            'description': 'Tech & Employment'
        },
        {
            'topic': 'mental health in the workplace',
            'context': 'WHO reports 25% increase in anxiety and depression since 2020. Companies investing heavily in wellness programs.',
            'description': 'Workplace Wellness'
        },
        {
            'topic': 'the future of remote work',
            'context': '74% of workers prefer hybrid models. Productivity up 13% but collaboration concerns persist.',
            'description': 'Future of Work'
        }
    ]
    
    print("Available demo scenarios:")
    for i, scenario in enumerate(scenarios, 1):
        print(f"  {i}. {scenario['description']}: {scenario['topic']}")
    
    print()
    choice = input("Select a scenario (1-3) or press Enter for all: ").strip()
    
    if choice == '':
        selected = scenarios
    else:
        try:
            selected = [scenarios[int(choice) - 1]]
        except (ValueError, IndexError):
            print("Invalid choice, running first scenario...")
            selected = [scenarios[0]]
    
    generator = PodcastGenerator()
    
    for scenario in selected:
        print("\n" + "=" * 70)
        print(f"📻 Generating: {scenario['description']}")
        print("=" * 70)
        print(f"Topic: {scenario['topic']}")
        print(f"Context: {scenario['context'][:80]}...")
        print()
        
        try:
            result = generator.generate(
                topic=scenario['topic'],
                real_world_context=scenario['context']
            )
            
            print("\n" + "🎧 " * 20)
            print(result['conversation'])
            print("🎧 " * 20)
            
            print(f"\n✨ Sponsor embedded: {result['sponsor']}")
            print("=" * 70)
            
            if len(selected) > 1:
                input("\nPress Enter for next scenario...")
        
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("\nMake sure you have:")
            print("  1. Created .env file with ANTHROPIC_API_KEY")
            print("  2. Valid Anthropic API key (get at console.anthropic.com)")
            print("  3. Installed dependencies: pip install -r requirements.txt")
            sys.exit(1)
    
    print("\n✅ Demo complete!")
    print("\nNext steps:")
    print("  • Run: python echoduo.py 'your topic here'")
    print("  • Check memory: python echoduo.py --show-memory")
    print("  • Read the README.md for more options")


if __name__ == '__main__':
    run_demo()

