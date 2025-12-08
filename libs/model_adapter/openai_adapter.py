from .base import ModelAdapter
from openai import AsyncOpenAI
from typing import Union, AsyncIterator
from libs.utils.config import config
from libs.utils.logging import setup_logger
from libs.utils.metrics import llm_api_calls_total, llm_tokens_used_total

logger = setup_logger("openai-adapter")

class OpenAIAdapter(ModelAdapter):
    def __init__(self):
        self.client = AsyncOpenAI(api_key=config.OPENAI_API_KEY)
        self.pricing = {
            "gpt-3.5-turbo": {"input": 0.0015 / 1000, "output": 0.002 / 1000},
            "gpt-4": {"input": 0.03 / 1000, "output": 0.06 / 1000},
            "gpt-4-turbo": {"input": 0.01 / 1000, "output": 0.03 / 1000},
        }
    
    async def complete(
        self,
        prompt: str,
        model: str = "gpt-3.5-turbo",
        stream: bool = False
    ) -> Union[str, AsyncIterator[str]]:
        try:
            response = await self.client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                stream=stream
            )
            
            if stream:
                async def stream_generator():
                    async for chunk in response:
                        if chunk.choices[0].delta.content:
                            yield chunk.choices[0].delta.content
                return stream_generator()
            else:
                tokens = response.usage.total_tokens
                cost = self.estimate_cost(tokens, model)
                
                llm_api_calls_total.labels(provider="openai", model=model).inc()
                llm_tokens_used_total.labels(provider="openai", model=model).inc(tokens)
                
                logger.info(f"OpenAI call: {model}, tokens: {tokens}, cost: ${cost:.4f}")
                return response.choices[0].message.content
        
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise
    
    def estimate_cost(self, tokens: int, model: str) -> float:
        if model not in self.pricing:
            return 0.0
        # Simplified: assume 50/50 input/output split
        input_tokens = tokens // 2
        output_tokens = tokens // 2
        return (input_tokens * self.pricing[model]["input"] + 
                output_tokens * self.pricing[model]["output"])
    
    def count_tokens(self, text: str) -> int:
        # Simplified token counting
        return len(text.split()) * 1.3  # Rough approximation
