import os
import anthropic
from typing import Iterator, Optional


class AnthropicLLMClient:
    def __init__(self, api_key: str = None, model: str = "claude-sonnet-4-20250514"):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.model = model

        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable or api_key parameter required")

        self.client = anthropic.Anthropic(api_key=self.api_key)

    def generate(self, system_prompt: str, user_prompt: str, **kwargs):
        """Generate response using Anthropic Claude with streaming (returns full response)"""
        try:

            stream = self.client.messages.create(
                model=self.model,
                max_tokens=kwargs.get('max_tokens', 2048),
                temperature=kwargs.get('temperature', 0.1),
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ],
                stream=True
            )

            full_response = ""
            usage_info = {}
            for chunk in stream:
                if chunk.type == "content_block_delta":
                    full_response += chunk.delta.text
                elif chunk.type == "message_delta":
                    if hasattr(chunk, 'usage'):
                        usage_info = {
                            'input_tokens': chunk.usage.input_tokens,
                            'output_tokens': chunk.usage.output_tokens,
                            'total_tokens': chunk.usage.input_tokens + chunk.usage.output_tokens
                        }

            return full_response, usage_info

        except Exception as e:
            print(f"LLM generation error: {str(e)}")
            raise

    def generate_stream(self, system_prompt: str, user_prompt: str, **kwargs) -> Iterator[str]:
        """Generate response using Anthropic Claude with streaming"""
        try:
            stream = self.client.messages.create(
                model=self.model,
                max_tokens=kwargs.get('max_tokens', 32000),
                temperature=kwargs.get('temperature', 0.1),
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ],
                stream=True
            )

            for chunk in stream:
                if chunk.type == "content_block_delta":
                    yield chunk.delta.text

        except Exception as e:
            print(f"LLM streaming error: {str(e)}")
            raise

    def generate_with_callback(self, system_prompt: str, user_prompt: str,
                               callback: callable, **kwargs) -> str:
        """Generate response with a callback function for each chunk"""
        full_response = ""
        try:
            for chunk in self.generate_stream(system_prompt, user_prompt, **kwargs):
                full_response += chunk
                callback(chunk)  # Call the callback with each chunk

            return full_response

        except Exception as e:
            print(f"LLM generation error: {str(e)}")
            raise