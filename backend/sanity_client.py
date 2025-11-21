"""Sanity CMS client for storing and retrieving podcast episodes."""
import requests
import os
from typing import Dict, List, Optional
from datetime import datetime
from config import SANITY_PROJECT_ID, SANITY_DATASET, SANITY_API_TOKEN, SANITY_SAVE_EPISODES


class SanityClient:
    """Client for interacting with Sanity CMS."""
    
    def __init__(self, verbose: bool = False):
        """
        Initialize Sanity client.
        
        Args:
            verbose: Enable verbose logging
        """
        self.verbose = verbose
        
        if not SANITY_PROJECT_ID or not SANITY_API_TOKEN:
            self.enabled = False
            if self.verbose:
                print("⚠️  Sanity: Not configured (missing PROJECT_ID or API_TOKEN)")
            return
            
        self.project_id = SANITY_PROJECT_ID
        self.dataset = SANITY_DATASET
        self.api_token = SANITY_API_TOKEN
        self.base_url = f"https://{self.project_id}.api.sanity.io/v2021-06-07"
        self.enabled = SANITY_SAVE_EPISODES
        
        # Test connection
        if self.enabled:
            try:
                self._test_connection()
                if self.verbose:
                    print(f"✅ Sanity: Connected to project {self.project_id}")
            except Exception as e:
                if self.verbose:
                    print(f"⚠️  Sanity connection test failed: {e}")
                    print("   Episodes may still save - Sanity will auto-create schema")
                # Don't disable - let it try anyway for auto-creation
    
    def _test_connection(self):
        """Test Sanity connection."""
        query = '*[_type == "episode"] | order(_createdAt desc) [0...1]'
        url = f"{self.base_url}/data/query/{self.dataset}"
        headers = {
            "Authorization": f"Bearer {self.api_token}"
        }
        params = {"query": query}
        
        response = requests.get(url, headers=headers, params=params, timeout=5)
        response.raise_for_status()
        
    def save_episode(self, episode_data: Dict) -> Dict:
        """
        Save a podcast episode to Sanity.
        This will auto-create the schema if it doesn't exist.
        
        Args:
            episode_data: Dictionary with episode information
                - topic: str
                - conversation: str
                - sponsor: str
                - context_used: str (optional)
                - sources: list (optional)
                - scraped_data: dict (optional)
        
        Returns:
            Dict with Sanity document ID and status
        """
        if not self.enabled:
            return {
                "success": False,
                "error": "Sanity not enabled or not configured"
            }
        
        # Prepare episode document
        # Note: Sanity will auto-create schema from first document if schema doesn't exist
        episode_doc = {
            "_type": "episode",
            "topic": episode_data.get('topic', ''),
            "conversation": episode_data.get('conversation', ''),
            "sponsor": episode_data.get('sponsor', ''),
            "contextUsed": episode_data.get('context_used', '')[:500] if episode_data.get('context_used') else '',
            "generatedAt": datetime.now().isoformat(),
            "hostAlex": "Curious, reflective, empathetic",
            "hostMaya": "Analytical, grounded, insightful"
        }
        
        # Add sources if available
        sources = episode_data.get('sources', [])
        if isinstance(sources, list):
            episode_doc["sourceUrls"] = [
                s.get('url', s) if isinstance(s, dict) else s 
                for s in sources[:10]  # Limit to 10 sources
            ]
        
        # Add scraped data summary if available
        scraped_data = episode_data.get('scraped_data', {})
        if scraped_data:
            episode_doc["scrapedSourcesCount"] = len(scraped_data.get('scraped', []))
            episode_doc["scrapingMethod"] = scraped_data.get('method', 'unknown')
        
        # Generate a deterministic document ID
        # Sanity format: lowercase alphanumeric, 32 chars
        import hashlib
        topic_hash = hashlib.md5(episode_doc.get('topic', '').encode()).hexdigest()
        timestamp = episode_doc.get('generatedAt', '').replace('-', '').replace(':', '').replace('.', '')[:14]
        doc_id = f"episode-{topic_hash[:16]}-{timestamp[:8]}"
        
        # Add the _id to the document so we know it after creation
        episode_doc["_id"] = doc_id
        
        mutation = {
            "mutations": [{
                "create": episode_doc
            }]
        }
        
        url = f"{self.base_url}/data/mutate/{self.dataset}"
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(url, json=mutation, headers=headers, timeout=10)
            response.raise_for_status()
            result = response.json()
            
            # Sanity mutation API returns: {"transactionId": "...", "results": [...]}
            # Document ID is not in response, but we generated it client-side
            transaction_id = result.get("transactionId", "unknown")
            
            # Verify document was created by querying it immediately
            verify_query = f'*[_id == "{doc_id}"]'
            query_url = f"{self.base_url}/data/query/{self.dataset}"
            params = {"query": verify_query}
            
            try:
                verify_response = requests.get(query_url, headers=headers, params=params, timeout=5)
                if verify_response.status_code == 200:
                    verify_result = verify_response.json()
                    if verify_result.get("result") and len(verify_result.get("result", [])) > 0:
                        # Document confirmed to exist
                        document_id = doc_id
                    else:
                        # Try querying by topic and timestamp as fallback
                        fallback_query = f'*[_type == "episode" && topic == "{episode_doc["topic"]}" && generatedAt == "{episode_doc["generatedAt"]}"] | order(_createdAt desc) [0]'
                        fallback_params = {"query": fallback_query}
                        fallback_response = requests.get(query_url, headers=headers, params=fallback_params, timeout=5)
                        if fallback_response.status_code == 200:
                            fallback_result = fallback_response.json()
                            if fallback_result.get("result") and fallback_result.get("result"):
                                document_id = fallback_result["result"][0].get("_id", doc_id)
                            else:
                                document_id = doc_id  # Use our generated ID anyway
                        else:
                            document_id = doc_id  # Use our generated ID anyway
                else:
                    document_id = doc_id  # Use our generated ID anyway
            except:
                document_id = doc_id  # Use our generated ID anyway
            
            if self.verbose:
                print(f"💾 Sanity: Episode saved successfully")
                print(f"   Document ID: {document_id}")
                print(f"   Transaction ID: {transaction_id}")
            
            return {
                "success": True,
                "document_id": document_id,
                "transaction_id": transaction_id,
                "status": "saved",
                "note": "Schema auto-created from document if this is first episode"
            }
        except requests.exceptions.HTTPError as e:
            error_msg = f"HTTP {e.response.status_code}"
            try:
                error_detail = e.response.json().get("message", str(e))
                error_msg = error_detail
            except:
                error_msg = str(e)
            
            if self.verbose:
                print(f"❌ Sanity save failed: {error_msg}")
            
            return {
                "success": False,
                "error": error_msg
            }
        except requests.exceptions.RequestException as e:
            if self.verbose:
                print(f"❌ Sanity connection error: {str(e)}")
            return {
                "success": False,
                "error": f"Request error: {str(e)}"
            }
        except Exception as e:
            if self.verbose:
                print(f"❌ Sanity unexpected error: {str(e)}")
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}"
            }
    
    def get_episodes(self, limit: int = 10, topic: Optional[str] = None) -> List[Dict]:
        """
        Query recent episodes from Sanity.
        
        Args:
            limit: Number of episodes to retrieve
            topic: Optional topic filter
            
        Returns:
            List of episode documents
        """
        if not self.enabled:
            return []
        
        if topic:
            query = f'*[_type == "episode" && topic match "{topic}*"] | order(generatedAt desc) [0...{limit}]'
        else:
            query = f'*[_type == "episode"] | order(generatedAt desc) [0...{limit}]'
        
        url = f"{self.base_url}/data/query/{self.dataset}"
        headers = {
            "Authorization": f"Bearer {self.api_token}"
        }
        params = {"query": query}
        
        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            result = response.json()
            return result.get("result", [])
        except Exception as e:
            print(f"❌ Error querying Sanity: {e}")
            return []
    
    def get_episode_by_id(self, doc_id: str) -> Optional[Dict]:
        """Get a specific episode by document ID."""
        if not self.enabled:
            return None
            
        query = f'*[_id == "{doc_id}"]'
        url = f"{self.base_url}/data/query/{self.dataset}"
        headers = {
            "Authorization": f"Bearer {self.api_token}"
        }
        params = {"query": query}
        
        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            result = response.json()
            return result.get("result", [None])[0]
        except Exception as e:
            print(f"❌ Error fetching episode from Sanity: {e}")
            return None
    
    def search_episodes(self, query_text: str, limit: int = 10) -> List[Dict]:
        """
        Search episodes by topic or conversation content.
        
        Args:
            query_text: Search text
            limit: Number of results
            
        Returns:
            List of matching episodes
        """
        if not self.enabled:
            return []
        
        query = f'*[_type == "episode" && (topic match "{query_text}*" || conversation match "{query_text}*")] | order(generatedAt desc) [0...{limit}]'
        
        url = f"{self.base_url}/data/query/{self.dataset}"
        headers = {
            "Authorization": f"Bearer {self.api_token}"
        }
        params = {"query": query}
        
        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            result = response.json()
            return result.get("result", [])
        except Exception as e:
            print(f"❌ Error searching Sanity: {e}")
            return []


def test_sanity_connection():
    """Test function to verify Sanity connection."""
    client = SanityClient()
    
    if not client.enabled:
        print("⚠️  Sanity not enabled or not configured")
        print("   Set SANITY_PROJECT_ID and SANITY_API_TOKEN in .env")
        return False
    
    print("✅ Sanity client initialized")
    print(f"   Project ID: {client.project_id}")
    print(f"   Dataset: {client.dataset}")
    
    # Test query
    print("\n🔍 Testing query...")
    episodes = client.get_episodes(limit=1)
    if episodes:
        print(f"✅ Successfully queried {len(episodes)} episode(s)")
    else:
        print("ℹ️  No episodes found (database may be empty)")
    
    return True


if __name__ == "__main__":
    test_sanity_connection()

