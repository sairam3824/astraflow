from typing import Optional
from libs.model_adapter import OpenAIAdapter, GeminiAdapter

class ModelRouter:
    def __init__(self):
        self.openai_adapter = OpenAIAdapter()
        self.gemini_adapter = GeminiAdapter()
    
    def select_model(
        self,
        task_type: Optional[str] = None,
        user_preference: Optional[str] = None,
        context_length: int = 0
    ) -> tuple[str, str]:
        """
        Select appropriate model and provider
        Returns: (provider, model_name)
        """
        # Explicit user preference
        if user_preference:
            if "gpt" in user_preference.lower():
                return ("openai", user_preference)
            elif "gemini" in user_preference.lower():
                return ("gemini", user_preference)
        
        # Automatic routing based on task type
        if task_type == "summarization":
            return ("gemini", "gemini-pro")  # Cost-effective
        elif context_length > 8000:
            return ("openai", "gpt-4-turbo")  # Large context
        else:
            return ("openai", "gpt-3.5-turbo")  # Fast and cheap
    
    async def complete(
        self,
        prompt: str,
        task_type: Optional[str] = None,
        user_preference: Optional[str] = None,
        context_length: int = 0,
        stream: bool = False
    ):
        """Route request to appropriate model"""
        provider, model = self.select_model(task_type, user_preference, context_length)
        
        if provider == "openai":
            return await self.openai_adapter.complete(prompt, model, stream)
        elif provider == "gemini":
            return await self.gemini_adapter.complete(prompt, model, stream)
        else:
            raise ValueError(f"Unknown provider: {provider}")

model_router = ModelRouter()
