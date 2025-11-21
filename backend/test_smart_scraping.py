"""Test the intelligent Claude → Lightpanda scraping pipeline."""
from smart_scraper import SmartScraper
import json

print("=" * 70)
print("🧠 SMART SCRAPING TEST")
print("   Phase 1: Claude identifies best websites")
print("   Phase 2: Lightpanda fetches real data")
print("   Phase 3: Claude synthesizes context")
print("=" * 70)

# Initialize
scraper = SmartScraper()

# Test topics
topics = [
    "AI agents and autonomous systems 2024",
    "remote work productivity trends",
    "cybersecurity threats 2024"
]

print("\n📝 Select a topic:")
for i, topic in enumerate(topics, 1):
    print(f"  {i}. {topic}")

choice = input("\nEnter number (or press Enter for topic 1): ").strip()

if choice and choice.isdigit() and 1 <= int(choice) <= len(topics):
    selected_topic = topics[int(choice) - 1]
else:
    selected_topic = topics[0]

print(f"\n✅ Selected: {selected_topic}")

# Run intelligent scraping
result = scraper.get_intelligent_context(selected_topic, max_sources=3)

print("\n" + "=" * 70)
print("📊 RESULTS")
print("=" * 70)

print("\n🎯 FINAL CONTEXT:")
print("-" * 70)
print(result['context'])

print("\n\n📚 SOURCES IDENTIFIED BY CLAUDE:")
print("-" * 70)
for i, source in enumerate(result['sources'], 1):
    print(f"\n{i}. {source['source_name']}")
    print(f"   URL: {source['url']}")
    print(f"   Reason: {source['reason']}")

if result.get('scraped_data'):
    print("\n\n📥 DATA RETRIEVED BY LIGHTPANDA:")
    print("-" * 70)
    for item in result['scraped_data']:
        print(f"\n• {item['source']}")
        print(f"  Status: {item.get('status', 'unknown')}")
        if item.get('content'):
            print(f"  Preview: {item['content'][:150]}...")

print("\n\n" + "=" * 70)
print("✅ TEST COMPLETE")
print("=" * 70)
print(f"\nMethod used: {result['method']}")
print(f"Lightpanda active: {result['lightpanda_used']}")
print(f"Sources processed: {len(result['sources'])}")
print("\n💡 This context can now be used in podcast generation!")

