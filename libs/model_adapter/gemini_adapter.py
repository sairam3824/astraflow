from .base import ModelAdapter
import google.generativeai as genai
from typing import Union, AsyncIterator
from libs.utils.config import config
from libs.utils.logging import setup_logger
from libs.utils.metrics import llm_api_calls_total, llm_tokens_used_total

logger = setup_logger("gemini-adapter")

class GeminiAdapter(ModelAdapter):
    def __init__(self):
        genai.configure(api_key=config.GEMINI_API_KEY)
        self.pricing = {
            "gemini-pro": {"input": 0.00025 / 1000, "output": 0.0005 / 1000},
        }
    
    async def complete(
        self,
        prompt: str,
        model: str = "gemini-pro",
        stream: bool = False
    ) -> Union[str, AsyncIterator[str]]:
        try:
            model_instance = genai.GenerativeModel(model)
            
            if stream:
                response = model_instance.generate_content(prompt, stream=True)
                async def stream_generator():
                    for chunk in response:
                        if chunk.text:
                            yield chunk.text
                return stream_generator()
            else:
                response = model_instance.generate_content(prompt)
                tokens = self.count_tokens(prompt + response.text)
                cost = self.estimate_cost(tokens, model)
                
                llm_api_calls_total.labels(provider="gemini", model=model).inc()
                llm_tokens_used_total.labels(provider="gemini", model=model).inc(tokens)
                
                logger.info(f"Gemini call: {model}, tokens: {tokens}, cost: ${cost:.4f}")
                return response.text
        
        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            raise
    
    def estimate_cost(self, tokens: int, model: str) -> float:
        if model not in self.pricing:
            return 0.0
        input_tokens = tokens // 2
        output_tokens = tokens // 2
        return (input_tokens * self.pricing[model]["input"] + 
                output_tokens * self.pricing[model]["output"])
    
    def count_tokens(self, text: str) -> int:
        return len(text.split()) * 1.3
