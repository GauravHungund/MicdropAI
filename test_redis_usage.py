#!/usr/bin/env python3
"""Quick test to see EchoDuo Redis usage."""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from memory_manager import MemoryManager

print("╔══════════════════════════════════════════════════════════════════╗")
print("║ 🧪 TESTING ECHODUO REDIS USAGE                                    ║")
print("╚══════════════════════════════════════════════════════════════════╝")
print()

# Initialize memory manager
memory = MemoryManager()

print("1. Adding test sponsor to Redis...")
memory.add_sponsor("Calm")
print("   ✅ Added sponsor: Calm")

print("\n2. Adding test phrases to Redis...")
memory.add_phrase("This is a test phrase")
memory.add_phrase("Another test phrase")
print("   ✅ Added 2 phrases")

print("\n3. Getting memory summary...")
summary = memory.get_memory_summary()
print(summary)

print("\n4. Checking if sponsor is blocked...")
blocked = memory.is_sponsor_blocked("Calm")
print(f"   Sponsor 'Calm' is blocked: {blocked}")

print("\n✅ Test complete! Check Redis now:")
print("   redis-cli KEYS 'echoduo:*'")
print("   redis-cli LRANGE echoduo:sponsors 0 -1")
print("   redis-cli LRANGE echoduo:phrases 0 -1")

