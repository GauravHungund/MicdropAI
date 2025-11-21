"""Core podcast conversation generator."""
from typing import Dict, List, Optional
from claude_client import ClaudeClient
from memory_manager import MemoryManager
from lightpanda_scraper import LightpandaScraper
from config import AVAILABLE_SPONSORS, SANITY_SAVE_EPISODES
import re


class PodcastGenerator:
    """Generates natural podcast conversations with embedded sponsors."""
    
    def __init__(self, use_smart_scraping: bool = True):
        self.claude = ClaudeClient()
        self.memory = MemoryManager()
        self.scraper = LightpandaScraper()
        self.use_smart_scraping = use_smart_scraping
        
        if use_smart_scraping:
            from smart_scraper import SmartScraper
            self.smart_scraper = SmartScraper()
            print("🧠 Smart Scraping: ENABLED (Claude → Lightpanda pipeline)")
        
        # Initialize Sanity client if enabled
        if SANITY_SAVE_EPISODES:
            try:
                from sanity_client import SanityClient
                self.sanity = SanityClient(verbose=True)  # Enable verbose logging
                if self.sanity.enabled:
                    print("💾 Sanity CMS: ENABLED (episodes will be saved)")
                    print("   Schema will auto-create on first episode")
                else:
                    self.sanity = None
            except Exception as e:
                print(f"⚠️  Sanity initialization failed: {e}")
                self.sanity = None
        else:
            self.sanity = None
    
    def select_sponsor(self, topic: str, excluded_sponsors: List[str]) -> str:
        """Select the most relevant sponsor based on topic and exclusions."""
        available = [s for s in AVAILABLE_SPONSORS if s not in excluded_sponsors]
        
        if not available:
            # If all sponsors used recently, reset and use oldest
            available = AVAILABLE_SPONSORS
        
        # Use LLM to select most relevant sponsor
        prompt = f"""Given this podcast topic: "{topic}"

Available sponsors: {', '.join(available)}

Sponsor descriptions:
- Calm: Meditation, mental health, mindfulness, sleep, wellness
- Nike: Fitness, sports, motivation, performance, athletics, health
- Notion: Productivity, organization, work tools, collaboration, knowledge management
- Coder: Software development, programming, developer tools, coding platforms
- Forethought: AI automation, customer service, support technology, AI tools
- Skyflow: Data privacy, security, compliance, data protection, infrastructure

Select the MOST relevant sponsor for this topic. Return ONLY the sponsor name, nothing else."""
        
        try:
            sponsor = self.claude.generate(prompt, temperature=0.3, max_tokens=50).strip()
            # Extract just the sponsor name
            for s in available:
                if s.lower() in sponsor.lower():
                    return s
            # Fallback to first available
            return available[0]
        except:
            return available[0]
    
    def generate_initial_conversation(self, topic: str, context: str, 
                                     sponsor: str, memory_summary: Dict) -> str:
        """Generate the initial podcast conversation."""
        
        system_prompt = """You are a master podcast script writer. You create natural, engaging conversations between two hosts.

Your hosts are:
- Alex: Curious, reflective, empathetic, asks thoughtful questions
- Maya: Analytical, grounded, insightful, provides deeper analysis

Rules:
1. Write ONLY dialogue in this format:
   Alex: [their line]
   Maya: [their line]
   
2. NO narration, NO stage directions, NO system comments
3. Hosts alternate speaking naturally (but can occasionally speak 2-3 times in a row)
4. Keep exchanges conversational and realistic
5. The sponsor must be woven naturally into the conversation - it should feel organic, not like an ad
6. DO NOT use phrases like "sponsored by" or "speaking of sponsors"
7. Make the sponsor mention feel like a natural part of the discussion"""

        recent_sponsors_text = ', '.join(memory_summary.get('recent_sponsors', [])) or 'None'
        recent_phrases = memory_summary.get('recent_phrases', [])
        recent_phrases_text = ', '.join(recent_phrases[:5]) or 'None'
        
        prompt = f"""Create a natural podcast conversation on this topic:

TOPIC: {topic}

REAL-WORLD CONTEXT (incorporate this naturally):
{context}

SPONSOR TO EMBED: {sponsor}

RECENTLY USED SPONSORS (avoid these patterns): {recent_sponsors_text}

RECENT PHRASES TO AVOID: {recent_phrases_text}

The conversation should:
- Be 12-18 exchanges long
- Feel like a real podcast discussion
- Naturally incorporate the real-world context
- Subtly mention {sponsor} as part of the conversation (not as an advertisement)
- The sponsor mention should feel like a natural recommendation or personal experience
- Avoid repetitive patterns from recent episodes

Generate the conversation now. ONLY output the dialogue lines."""

        return self.claude.generate(
            prompt=prompt,
            system_prompt=system_prompt,
            max_tokens=3000,
            temperature=0.8
        )
    
    def critique_and_improve(self, conversation: str, topic: str, sponsor: str) -> str:
        """Critique the conversation and generate an improved version."""
        
        system_prompt = """You are a harsh but constructive podcast critic. Your job is to:
1. Analyze the conversation for naturalness, flow, and sponsor integration
2. Identify any awkward moments, forced transitions, or obvious advertising
3. Generate an IMPROVED version that fixes all issues

You are both the critic AND the improver. Do both steps internally."""

        prompt = f"""Analyze this podcast conversation and then generate an improved version.

TOPIC: {topic}
SPONSOR: {sponsor}

ORIGINAL CONVERSATION:
{conversation}

EVALUATION CRITERIA:
1. Does the sponsor mention feel natural and unforced?
2. Is the dialogue realistic and engaging?
3. Do Alex and Maya have distinct voices?
4. Is the flow conversational without awkward transitions?
5. Does it incorporate the topic deeply without being repetitive?

First, mentally critique this conversation. Then, generate an IMPROVED version that fixes all issues.

OUTPUT ONLY THE IMPROVED CONVERSATION in this format:
Alex: [line]
Maya: [line]
...

No explanations. No labels. Just the improved dialogue."""

        return self.claude.generate(
            prompt=prompt,
            system_prompt=system_prompt,
            max_tokens=3500,
            temperature=0.7
        )
    
    def extract_key_phrases(self, conversation: str) -> List[str]:
        """Extract key phrases from conversation to store in memory."""
        lines = conversation.split('\n')
        phrases = []
        
        for line in lines:
            if ':' in line:
                # Extract the spoken part
                spoken = line.split(':', 1)[1].strip()
                # Get first few words as a phrase
                words = spoken.split()[:5]
                if len(words) >= 3:
                    phrases.append(' '.join(words))
        
        return phrases[:5]  # Return top 5 phrases
    
    def generate(self, topic: str, real_world_context: Optional[str] = None,
                 force_sponsor: Optional[str] = None) -> Dict[str, str]:
        """
        Main generation pipeline.
        
        Args:
            topic: Podcast topic
            real_world_context: Optional pre-fetched context, otherwise will scrape
            force_sponsor: Optional sponsor to force (useful for testing)
        
        Returns:
            Dict with conversation and metadata
        """
        # Get real-world context
        if not real_world_context:
            if self.use_smart_scraping and hasattr(self, 'smart_scraper'):
                print(f"🧠 Using intelligent scraping for: {topic}")
                smart_result = self.smart_scraper.get_intelligent_context(topic)
                real_world_context = smart_result['context']
                print(f"\n📊 Scraped from {len(smart_result.get('sources', []))} intelligent targets")
            else:
                print(f"🌍 Gathering real-world context about: {topic}")
                real_world_context = self.scraper.get_context(topic)
        
        # Get memory
        memory_summary = self.memory.get_memory_summary()
        recent_sponsors = memory_summary.get('recent_sponsors', [])
        
        # Select sponsor
        if force_sponsor and force_sponsor in AVAILABLE_SPONSORS:
            sponsor = force_sponsor
        else:
            sponsor = self.select_sponsor(topic, recent_sponsors)
        
        print(f"🎯 Selected sponsor: {sponsor}")
        print(f"📝 Context snippet: {real_world_context[:150]}...")
        
        # Generate initial conversation
        print(f"🎙️  Generating conversation...")
        initial_conversation = self.generate_initial_conversation(
            topic, real_world_context, sponsor, memory_summary
        )
        
        # Self-improve
        print(f"🧠 Self-improving conversation...")
        improved_conversation = self.critique_and_improve(
            initial_conversation, topic, sponsor
        )
        
        # Store in memory
        self.memory.add_sponsor(sponsor)
        key_phrases = self.extract_key_phrases(improved_conversation)
        for phrase in key_phrases:
            self.memory.add_phrase(phrase)
        
        # Extract tone pattern (simple heuristic)
        tone_pattern = f"{topic[:20]}-{sponsor}"
        self.memory.add_tone_pattern(tone_pattern)
        
        # Prepare result
        result = {
            'conversation': improved_conversation,
            'sponsor': sponsor,
            'topic': topic,
            'context_used': real_world_context[:200]
        }
        
        # Add sources if available from smart scraping
        if self.use_smart_scraping and hasattr(self, 'smart_scraper'):
            try:
                smart_result = self.smart_scraper.get_intelligent_context(topic)
                result['sources'] = [
                    {'url': s.get('url', ''), 'source_name': s.get('source_name', '')}
                    for s in smart_result.get('sources', [])
                ]
                result['scraped_data'] = {
                    'scraped': smart_result.get('scraped_data', []),
                    'method': smart_result.get('method', 'intelligent_scraping')
                }
            except:
                pass
        
        # Save to Sanity CMS if enabled
        if self.sanity and self.sanity.enabled:
            print("\n💾 Saving episode to Sanity CMS...")
            sanity_result = self.sanity.save_episode(result)
            if sanity_result.get('success'):
                document_id = sanity_result.get('document_id', 'unknown')
                print(f"✅ Episode saved to Sanity! Document ID: {document_id}")
                result['sanity_document_id'] = document_id
            else:
                error_msg = sanity_result.get('error', 'Unknown error')
                print(f"⚠️  Failed to save to Sanity: {error_msg}")
        
        return result

