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
                                     sponsor: str, memory_summary: Dict, 
                                     previous_script: Optional[str] = None) -> str:
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
7. Make the sponsor mention feel like a natural part of the discussion
8. IMPORTANT: When mentioning the sponsor name, wrap it with *sponsor* markers like this: *sponsor*SponsorName*sponsor*
   Example: "I've been using *sponsor*Notion*sponsor* for my project management and it's been great."
   This allows the frontend to highlight sponsor mentions."""

        recent_sponsors_text = ', '.join(memory_summary.get('recent_sponsors', [])) or 'None'
        recent_phrases = memory_summary.get('recent_phrases', [])
        recent_phrases_text = ', '.join(recent_phrases[:5]) or 'None'
        
        continuation_note = ""
        if previous_script:
            continuation_note = f"""

PREVIOUS CONVERSATION (continue naturally from this):
{previous_script}

IMPORTANT: This is a continuation. The conversation should flow naturally from the previous discussion. 
Reference the previous conversation naturally, but don't repeat it. Continue the discussion as if it's the same podcast episode."""
        
        prompt = f"""Create a natural podcast conversation on this topic:

TOPIC: {topic}

REAL-WORLD CONTEXT (incorporate this naturally):
{context}

SPONSOR TO EMBED: {sponsor}

RECENTLY USED SPONSORS (avoid these patterns): {recent_sponsors_text}

RECENT PHRASES TO AVOID: {recent_phrases_text}
{continuation_note}

The conversation should:
- Be 12-18 exchanges long
- Feel like a real podcast discussion
- Naturally incorporate the real-world context
- Subtly mention {sponsor} as part of the conversation (not as an advertisement)
- The sponsor mention should feel like a natural recommendation or personal experience
- Wrap sponsor name with *sponsor* markers: *sponsor*{sponsor}*sponsor*
- Avoid repetitive patterns from recent episodes
{'- Continue naturally from the previous conversation' if previous_script else ''}

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

IMPORTANT: Preserve all *sponsor* markers in the improved version.
If the sponsor name is wrapped with *sponsor* markers, keep them exactly as they are.

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

IMPORTANT: Preserve all *sponsor* markers. If sponsor was marked as *sponsor*SponsorName*sponsor*, keep it exactly like that.

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
    
    def extract_tags_from_topic(self, topic: str) -> List[str]:
        """
        Extract relevant tags from a topic using Claude.
        
        Args:
            topic: Podcast topic
            
        Returns:
            List of tags (e.g., ["ai", "technology", "machine-learning"])
        """
        prompt = f"""Given this podcast topic: "{topic}"

Extract 3-5 relevant tags that would help categorize and find similar episodes.
Tags should be:
- Single words or short phrases (1-2 words max)
- Lowercase
- Relevant to the topic
- Common categories (e.g., "ai", "technology", "business", "health", "education")

Return ONLY a comma-separated list of tags, nothing else.
Example: ai,technology,machine-learning,innovation"""

        try:
            tags_str = self.claude.generate(prompt, temperature=0.3, max_tokens=100).strip()
            # Parse tags
            tags = [tag.strip().lower() for tag in tags_str.split(',') if tag.strip()]
            # Limit to 5 tags and remove duplicates
            unique_tags = list(dict.fromkeys(tags))[:5]
            return unique_tags
        except Exception as e:
            print(f"⚠️  Failed to extract tags: {e}")
            # Fallback: simple keyword extraction
            words = topic.lower().split()
            # Filter out common words
            stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'about', 'is', 'are', 'was', 'were'}
            tags = [w for w in words if w not in stop_words and len(w) > 3][:5]
            return tags
    
    def generate(self, topic: str, real_world_context: Optional[str] = None,
                 force_sponsor: Optional[str] = None, previous_script: Optional[str] = None,
                 sequence_id: Optional[str] = None, sequence_index: Optional[int] = None) -> Dict[str, str]:
        """
        Main generation pipeline.
        
        Args:
            topic: Podcast topic
            real_world_context: Optional pre-fetched context, otherwise will scrape
            force_sponsor: Optional sponsor to force (useful for testing)
            previous_script: Optional previous conversation script for continuation
            sequence_id: Optional sequence ID for grouping related episodes
            sequence_index: Optional index in the sequence (0-based)
        
        Returns:
            Dict with conversation and metadata
        """
        # Extract tags from topic
        tags = self.extract_tags_from_topic(topic)
        print(f"🏷️  Extracted tags: {tags}")
        
        # Check for existing context in Sanity
        existing_context = None
        existing_scraped_data = []
        if self.sanity:
            # Search for episodes with similar tags
            similar_episodes = self.sanity.get_episodes_by_tags(tags, limit=3)
            if similar_episodes:
                print(f"📚 Found {len(similar_episodes)} similar episodes with matching tags")
                # Get scraped data from similar episodes
                existing_scraped_data = self.sanity.get_scraped_data_by_tags(tags, limit=5)
                if existing_scraped_data:
                    print(f"📊 Found {len(existing_scraped_data)} pieces of scraped content from similar episodes")
                    # Combine existing scraped content
                    existing_context_parts = []
                    for item in existing_scraped_data[:3]:  # Use top 3
                        content_snippet = item.get('content', '')[:500]
                        if content_snippet:
                            existing_context_parts.append(f"From {item.get('source', 'previous episode')}: {content_snippet}")
                    if existing_context_parts:
                        existing_context = "\n\n".join(existing_context_parts)
                        print(f"📚 Using existing context from similar episodes")
            
            # Also check by topic (existing logic)
            topic_context = self.sanity.get_context_for_topic(topic)
            if topic_context:
                if existing_context:
                    existing_context = f"{existing_context}\n\nTopic-specific context: {topic_context}"
                else:
                    existing_context = topic_context
                print(f"📚 Found existing context for topic: {topic}")
            
            # Also search for previous scripts in the same sequence
            if sequence_id:
                previous_episodes = self.sanity.get_episodes_by_sequence(sequence_id)
                if previous_episodes:
                    # Get the most recent previous script
                    latest_episode = sorted(previous_episodes, key=lambda x: x.get('sequenceIndex', 0))[-1]
                    if latest_episode.get('conversation'):
                        previous_script = latest_episode['conversation']
                        print(f"📜 Found previous script from sequence {sequence_id}")
        
        # Get real-world context
        smart_result = None
        scraped_data_for_sanity = []
        if not real_world_context:
            if self.use_smart_scraping and hasattr(self, 'smart_scraper'):
                print(f"🧠 Using intelligent scraping for: {topic}")
                smart_result = self.smart_scraper.get_intelligent_context(topic)
                new_context = smart_result['context']
                scraped_data_for_sanity = smart_result.get('scraped_data', [])
                
                # Combine existing and new context
                if existing_context:
                    # Add existing scraped data to new scraping
                    if existing_scraped_data:
                        scraped_data_for_sanity.extend(existing_scraped_data[:3])  # Include top 3 from similar episodes
                    real_world_context = f"{existing_context}\n\nRecent updates: {new_context}"
                    print(f"🔄 Combined existing context with new scraping data")
                else:
                    real_world_context = new_context
                
                print(f"\n📊 Scraped from {len(smart_result.get('sources', []))} intelligent targets")
            else:
                print(f"🌍 Gathering real-world context about: {topic}")
                new_context = self.scraper.get_context(topic)
                
                # Combine existing and new context
                if existing_context:
                    real_world_context = f"{existing_context}\n\nRecent updates: {new_context}"
                else:
                    real_world_context = new_context
        
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
        if previous_script:
            print(f"📜 Using previous script for continuation")
        initial_conversation = self.generate_initial_conversation(
            topic, real_world_context, sponsor, memory_summary, previous_script
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
        
        # Prepare result with scraped data for Sanity
        result = {
            'conversation': improved_conversation,
            'sponsor': sponsor,
            'topic': topic,
            'context_used': real_world_context,  # Full context, not truncated
            'previous_script': previous_script if previous_script else None,
            'is_continuation': previous_script is not None,
            'sequence_id': sequence_id,
            'sequence_index': sequence_index,
            'tags': tags
        }
        
        # Add sources and scraped data if available from smart scraping
        if smart_result:
            result['sources'] = [
                {'url': s.get('url', ''), 'source_name': s.get('source_name', '')}
                for s in smart_result.get('sources', [])
            ]
            result['scraped_data'] = scraped_data_for_sanity  # List of scraped content
        
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

