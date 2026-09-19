import httpx
from loguru import logger
from app.core.config import get_settings


class OpenRouterClient:
    """HTTP client for OpenRouter LLM API requests."""

    BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

    @classmethod
    def call(cls, system_prompt: str, user_prompt: str) -> str:
        """Call OpenRouter API with given system and user prompts."""
        settings = get_settings()
        api_key = settings.openrouter_api_key
        model = settings.openrouter_model or "anthropic/claude-3.5-sonnet"

        if not api_key:
            logger.warning("OPENROUTER_API_KEY is not configured. Returning fallback diagnosis.")
            raise ValueError("OPENROUTER_API_KEY is missing")

        headers = {
            "Authorization": f"Bearer {api_key}",
            "HTTP-Referer": "https://ai-kubernetes-agent.local",
            "X-Title": "AI Kubernetes Agent",
            "Content-Type": "application/json",
        }

        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.1,
            "response_format": {"type": "json_object"},
        }

        logger.info("Sending request to OpenRouter API (model: {})", model)

        try:
            with httpx.Client(timeout=30.0) as client:
                response = client.post(cls.BASE_URL, headers=headers, json=payload)
                response.raise_for_status()
                data = response.json()
                
                content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
                if not content:
                    raise ValueError("Empty response received from OpenRouter API")
                
                logger.info("Successfully received response from OpenRouter API")
                return content
        except httpx.HTTPStatusError as e:
            logger.error("OpenRouter HTTP error: {} | response: {}", e.response.status_code, e.response.text)
            raise
        except Exception as e:
            logger.error("Error communicating with OpenRouter API: {}", e)
            raise
