"""View saved episodes from Sanity CMS."""
import os
from dotenv import load_dotenv
from sanity_client import SanityClient
from datetime import datetime

load_dotenv()

def format_date(date_str):
    """Format ISO date string to readable format."""
    try:
        if not date_str:
            return "Unknown"
        dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except:
        return date_str

def display_episodes(episodes, limit=None):
    """Display episodes in a formatted way."""
    if not episodes:
        print("📭 No episodes found in Sanity CMS.")
        print()
        print("Generate an episode first:")
        print("  python echoduo.py 'your topic'")
        return
    
    print(f"📚 Found {len(episodes)} episode(s) in Sanity CMS:")
    print("=" * 80)
    print()
    
    for i, ep in enumerate(episodes, 1):
        print(f"Episode #{i}")
        print("-" * 80)
        
        # Basic info
        print(f"  📝 Topic: {ep.get('topic', 'Unknown')}")
        print(f"  💰 Sponsor: {ep.get('sponsor', 'None')}")
        print(f"  🆔 Document ID: {ep.get('_id', 'Unknown')}")
        
        # Date
        created_at = ep.get('_createdAt') or ep.get('generatedAt')
        if created_at:
            print(f"  📅 Created: {format_date(created_at)}")
        
        # Conversation preview
        conversation = ep.get('conversation', '')
        if conversation:
            preview = conversation[:200].replace('\n', ' ')
            if len(conversation) > 200:
                preview += "..."
            print(f"  💬 Conversation Preview: {preview}")
        
        # Sources
        sources = ep.get('sourceUrls', [])
        if sources:
            print(f"  🔗 Sources: {len(sources)} URL(s)")
            for j, source in enumerate(sources[:3], 1):
                url = source.get('url', source) if isinstance(source, dict) else source
                print(f"     {j}. {url[:60]}...")
        
        # Context
        context = ep.get('contextUsed', '')
        if context:
            context_preview = context[:100].replace('\n', ' ')
            if len(context) > 100:
                context_preview += "..."
            print(f"  🌐 Context: {context_preview}")
        
        print()

def main():
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║ 📚 VIEW SAVED EPISODES - SANITY CMS                                ║")
    print("╚══════════════════════════════════════════════════════════════════╝")
    print()
    
    # Initialize client
    client = SanityClient(verbose=False)
    
    if not client.enabled:
        print("❌ Sanity CMS not enabled or not configured")
        print()
        print("Make sure you have in .env:")
        print("  SANITY_PROJECT_ID=your_project_id")
        print("  SANITY_API_TOKEN=your_token")
        print("  SANITY_DATASET=production")
        print("  SANITY_SAVE_EPISODES=true")
        return
    
    # Get episodes
    print("🔍 Querying Sanity CMS for episodes...")
    print()
    
    episodes = client.get_episodes(limit=20)
    
    if not episodes:
        print("📭 No episodes found.")
        print()
        print("Generate an episode first:")
        print("  python echoduo.py 'your topic'")
        return
    
    # Display episodes
    display_episodes(episodes)
    
    print("=" * 80)
    print()
    print("💡 Tips:")
    print("  • View full conversation: Use Sanity Studio (see below)")
    print("  • Search episodes: python view_episodes.py --search 'keyword'")
    print("  • View specific episode: python view_episodes.py --id <document_id>")
    print()
    print("🌐 To view in Sanity Studio web UI:")
    print("   1. Install Sanity CLI: npm install -g @sanity/cli")
    print("   2. Initialize: sanity init --project-id <PROJECT_ID> --dataset production")
    print("   3. Start Studio: sanity start")
    print("   4. Open browser: http://localhost:3333")

if __name__ == "__main__":
    import sys
    
    client = SanityClient(verbose=False)
    
    if not client.enabled:
        print("❌ Sanity CMS not enabled")
        sys.exit(1)
    
    # Handle command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--search" and len(sys.argv) > 2:
            # Search episodes
            query = sys.argv[2]
            print(f"🔍 Searching for: '{query}'")
            print()
            episodes = client.search_episodes(query, limit=10)
            display_episodes(episodes)
        elif sys.argv[1] == "--id" and len(sys.argv) > 2:
            # Get specific episode
            doc_id = sys.argv[2]
            print(f"🔍 Fetching episode: {doc_id}")
            print()
            episode = client.get_episode_by_id(doc_id)
            if episode:
                display_episodes([episode])
            else:
                print(f"❌ Episode not found: {doc_id}")
        elif sys.argv[1] == "--help":
            print("Usage:")
            print("  python view_episodes.py              # List all episodes")
            print("  python view_episodes.py --search <keyword>  # Search episodes")
            print("  python view_episodes.py --id <document_id>  # Get specific episode")
        else:
            print("Unknown option. Use --help for usage.")
    else:
        # Default: list all episodes
        main()

