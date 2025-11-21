"""Anthropic Claude API client for podcast generation."""
import anthropic
from typing import Optional
from config import ANTHROPIC_API_KEY, MODEL_NAME, MAX_TOKENS, DEFAULT_TEMPERATURE


class ClaudeClient:
    """Client for interacting with Anthropic's Claude API."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Claude client.
        
        Args:
            api_key: Optional API key. Uses ANTHROPIC_API_KEY from env if not provided.
        """
        self.api_key = api_key or ANTHROPIC_API_KEY
        if not self.api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY not found. Please set it in your .env file or pass it directly."
            )
        
        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.model_name = MODEL_NAME
    
    def generate(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None,
        max_tokens: int = MAX_TOKENS,
        temperature: float = DEFAULT_TEMPERATURE
    ) -> str:
        """
        Generate text using Claude.
        
        Args:
            prompt: The user prompt
            system_prompt: Optional system prompt to set context
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature (0.0-1.0)
        
        Returns:
            Generated text response
        """
        try:
            message_params = {
                "model": self.model_name,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }
            
            if system_prompt:
                message_params["system"] = system_prompt
            
            response = self.client.messages.create(**message_params)
            
            # Extract text from response
            return response.content[0].text
            
        except anthropic.APIError as e:
            print(f"Anthropic API Error: {e}")
            raise
        except Exception as e:
            print(f"Error calling Claude: {e}")
            raise
    
    def generate_streaming(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = MAX_TOKENS,
        temperature: float = DEFAULT_TEMPERATURE
    ):
        """
        Generate text using Claude with streaming.
        
        Args:
            prompt: The user prompt
            system_prompt: Optional system prompt
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
        
        Yields:
            Text chunks as they arrive
        """
        try:
            message_params = {
                "model": self.model_name,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }
            
            if system_prompt:
                message_params["system"] = system_prompt
            
            with self.client.messages.stream(**message_params) as stream:
                for text in stream.text_stream:
                    yield text
                    
        except anthropic.APIError as e:
            print(f"Anthropic API Error: {e}")
            raise
        except Exception as e:
            print(f"Error in streaming: {e}")
            raise


