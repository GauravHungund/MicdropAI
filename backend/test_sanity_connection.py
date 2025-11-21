"""Test Sanity connection and verify episodes are accessible."""
import os
import requests
from dotenv import load_dotenv
from config import SANITY_PROJECT_ID, SANITY_DATASET, SANITY_API_TOKEN

load_dotenv()

print("╔══════════════════════════════════════════════════════════════════╗")
print("║ 🔍 TESTING SANITY CONNECTION & ACCESS                             ║")
print("╚══════════════════════════════════════════════════════════════════╝")
print()

if not SANITY_PROJECT_ID or not SANITY_API_TOKEN:
    print("❌ Sanity credentials not configured in .env")
    print("   Need: SANITY_PROJECT_ID, SANITY_API_TOKEN")
    exit(1)

print(f"Project ID: {SANITY_PROJECT_ID}")
print(f"Dataset: {SANITY_DATASET}")
print()

base_url = f"https://{SANITY_PROJECT_ID}.api.sanity.io/v2021-06-07"
headers = {
    "Authorization": f"Bearer {SANITY_API_TOKEN}"
}

# Test 1: Count episodes
print("=" * 70)
print("TEST 1: Counting Episodes")
print("=" * 70)
print()

query = 'count(*[_type == "episode"])'
url = f"{base_url}/data/query/{SANITY_DATASET}"
params = {"query": query}

try:
    response = requests.get(url, headers=headers, params=params, timeout=10)
    response.raise_for_status()
    result = response.json()
    count = result.get("result", 0)
    print(f"✅ Found {count} episode(s) in dataset '{SANITY_DATASET}'")
except Exception as e:
    print(f"❌ Error counting episodes: {e}")
    exit(1)

print()

# Test 2: List all episodes
print("=" * 70)
print("TEST 2: Listing All Episodes")
print("=" * 70)
print()

query = '*[_type == "episode"] | order(generatedAt desc) [0...10] {_id, topic, sponsor, generatedAt}'
params = {"query": query}

try:
    response = requests.get(url, headers=headers, params=params, timeout=10)
    response.raise_for_status()
    result = response.json()
    episodes = result.get("result", [])
    
    if episodes:
        print(f"📚 Found {len(episodes)} episode(s):")
        print()
        for i, ep in enumerate(episodes, 1):
            topic = ep.get('topic', 'Unknown')[:50]
            sponsor = ep.get('sponsor', 'None')
            doc_id = ep.get('_id', 'Unknown')[:30]
            print(f"  {i}. {topic}")
            print(f"     Sponsor: {sponsor} | ID: {doc_id}...")
            print()
    else:
        print("📭 No episodes found")
except Exception as e:
    print(f"❌ Error listing episodes: {e}")
    exit(1)

print()

# Test 3: Show GROQ queries for dashboard
print("=" * 70)
print("GROQ QUERIES FOR SANITY DASHBOARD")
print("=" * 70)
print()
print("Copy these queries and paste into Sanity Vision (API Explorer):")
print()
print("📍 URL: https://manage.sanity.io")
print("   → Select project: {SANITY_PROJECT_ID}")
print("   → API → Vision → Dataset: {SANITY_DATASET}")
print()
print("Query 1: Count episodes")
print("-" * 70)
print('count(*[_type == "episode"])')
print()
print("Query 2: List all episodes")
print("-" * 70)
print('*[_type == "episode"] | order(generatedAt desc) {_id, topic, sponsor, generatedAt}')
print()
print("Query 3: Full episode details")
print("-" * 70)
print('*[_type == "episode"] | order(generatedAt desc) {_id, topic, sponsor, conversation, contextUsed, sourceUrls, generatedAt}')
print()
print("Query 4: Single episode")
print("-" * 70)
print('*[_type == "episode"][0] {_id, topic, sponsor, conversation}')
print()

print("=" * 70)
print("✅ CONNECTION TEST COMPLETE")
print("=" * 70)
print()
print("If episodes are found, they're accessible via:")
print("  1. Sanity Dashboard Vision: https://manage.sanity.io")
print("  2. Sanity Studio: ./setup_sanity_studio.sh")
print("  3. Command line: python view_episodes.py")
print()

