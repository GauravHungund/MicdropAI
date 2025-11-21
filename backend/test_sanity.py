"""Test Sanity CMS integration."""
import os
from dotenv import load_dotenv
from sanity_client import SanityClient, test_sanity_connection

load_dotenv()

print("╔══════════════════════════════════════════════════════════════════╗")
print("║ 🧪 TESTING SANITY CMS INTEGRATION                                ║")
print("╚══════════════════════════════════════════════════════════════════╝")
print()

# Test connection
print("=" * 70)
print("STEP 1: Testing Sanity Connection")
print("=" * 70)
print()

if not test_sanity_connection():
    print("\n❌ Sanity connection failed!")
    print("\nMake sure you have:")
    print("  1. Created a Sanity project")
    print("  2. Set SANITY_PROJECT_ID in .env")
    print("  3. Set SANITY_API_TOKEN in .env")
    print("  4. Created the episode schema in Sanity Studio")
    exit(1)

print()
print("=" * 70)
print("STEP 2: Testing Episode Save")
print("=" * 70)
print()

# Create test episode
client = SanityClient()

if not client.enabled:
    print("⚠️  Sanity client not enabled")
    exit(1)

test_episode = {
    'topic': 'Test Episode: Sanity Integration',
    'conversation': 'Alex: This is a test episode.\nMaya: Yes, testing Sanity CMS integration.',
    'sponsor': 'Calm',
    'context_used': 'Test context for Sanity integration',
    'sources': [
        {'url': 'https://example.com/test', 'source_name': 'Test Source'}
    ],
    'scraped_data': {
        'scraped': [],
        'method': 'test'
    }
}

print("💾 Saving test episode...")
result = client.save_episode(test_episode)

if result.get('success'):
    doc_id = result.get('document_id')
    print(f"✅ Test episode saved! Document ID: {doc_id}")
    print()
    
    print("=" * 70)
    print("STEP 3: Querying Episodes")
    print("=" * 70)
    print()
    
    # Query episodes
    print("🔍 Querying recent episodes...")
    episodes = client.get_episodes(limit=5)
    
    if episodes:
        print(f"\n✅ Found {len(episodes)} episode(s):")
        for i, ep in enumerate(episodes, 1):
            print(f"\n   {i}. {ep.get('topic', 'Unknown')}")
            print(f"      Sponsor: {ep.get('sponsor', 'Unknown')}")
            print(f"      Date: {ep.get('generatedAt', 'Unknown')}")
    else:
        print("ℹ️  No episodes found (may need to generate some first)")
    
    print()
    print("=" * 70)
    print("✅ SANITY CMS INTEGRATION WORKING!")
    print("=" * 70)
    print()
    print("Your episodes will now be automatically saved to Sanity.")
    print("View them in Sanity Studio: sanity start")
    
else:
    print(f"\n❌ Failed to save test episode: {result.get('error')}")
    print("\nTroubleshooting:")
    print("  1. Check SANITY_PROJECT_ID is correct")
    print("  2. Check SANITY_API_TOKEN is valid")
    print("  3. Ensure dataset exists and is accessible")
    print("  4. Make sure episode schema is created in Sanity Studio")

