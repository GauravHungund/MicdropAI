"""Test suite for EchoDuo system."""
from podcast_generator import PodcastGenerator
from memory_manager import MemoryManager
from lightpanda_scraper import LightpandaScraper


def test_sponsor_selection():
    """Test sponsor selection logic."""
    generator = PodcastGenerator()
    
    # Test with no exclusions
    sponsor = generator.select_sponsor("AI taking over jobs", [])
    print(f"✅ Sponsor selected for AI topic: {sponsor}")
    assert sponsor in ["Calm", "Nike", "Notion", "Coder", "Forethought", "Skyflow"]
    
    # Test with exclusions
    excluded = ["Calm", "Nike"]
    sponsor = generator.select_sponsor("AI automation", excluded)
    print(f"✅ Sponsor selected (excluding {excluded}): {sponsor}")
    assert sponsor not in excluded


def test_memory_manager():
    """Test memory management."""
    memory = MemoryManager()
    
    # Clear first
    memory.clear_all()
    
    # Test sponsor storage
    memory.add_sponsor("Calm")
    memory.add_sponsor("Nike")
    recent = memory.get_recent_sponsors()
    print(f"✅ Recent sponsors stored: {recent}")
    assert "Calm" in recent and "Nike" in recent
    
    # Test phrase storage
    memory.add_phrase("I've been thinking")
    memory.add_phrase("That's interesting")
    phrases = memory.get_recent_phrases()
    print(f"✅ Recent phrases stored: {phrases[:2]}")
    assert len(phrases) > 0
    
    # Clean up
    memory.clear_all()


def test_scraper():
    """Test web scraping functionality."""
    scraper = LightpandaScraper()
    
    # Test fallback context
    context = scraper._generate_fallback_context("AI taking over jobs")
    print(f"✅ Fallback context generated: {context[:100]}...")
    assert len(context) > 50


def test_conversation_format():
    """Test that generated conversation has correct format."""
    generator = PodcastGenerator()
    
    # Use a simple topic with forced sponsor
    result = generator.generate(
        topic="mental health in the workplace",
        real_world_context="Recent studies show 25% increase in workplace stress",
        force_sponsor="Calm"
    )
    
    conversation = result['conversation']
    lines = conversation.strip().split('\n')
    
    # Check format
    has_alex = any('Alex:' in line for line in lines)
    has_maya = any('Maya:' in line for line in lines)
    
    print(f"✅ Conversation generated with {len(lines)} lines")
    print(f"✅ Has Alex: {has_alex}, Has Maya: {has_maya}")
    print(f"✅ Sponsor used: {result['sponsor']}")
    
    assert has_alex and has_maya
    assert result['sponsor'] == "Calm"
    
    # Print first few lines
    print("\n📝 Sample output:")
    for line in lines[:6]:
        print(line)


if __name__ == '__main__':
    print("🧪 Running EchoDuo Test Suite\n")
    print("=" * 60)
    
    print("\n1️⃣  Testing Sponsor Selection...")
    test_sponsor_selection()
    
    print("\n2️⃣  Testing Memory Manager...")
    test_memory_manager()
    
    print("\n3️⃣  Testing Scraper...")
    test_scraper()
    
    print("\n4️⃣  Testing Full Conversation Generation...")
    print("⚠️  This will make Anthropic API calls (costs ~$0.05)")
    response = input("Continue? (y/n): ")
    if response.lower() == 'y':
        test_conversation_format()
    
    print("\n" + "=" * 60)
    print("✅ All tests completed!")

