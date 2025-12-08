from abc import ABC, abstractmethod
from typing import Union, AsyncIterator

class ModelAdapter(ABC):
    @abstractmethod
    async def complete(
        self,
        prompt: str,
        model: str,
        stream: bool = False
    ) -> Union[str, AsyncIterator[str]]:
        """Generate completion from LLM"""
        pass
    
    @abstractmethod
    def estimate_cost(self, tokens: int, model: str) -> float:
        """Estimate cost for token usage"""
        pass
    
    @abstractmethod
    def count_tokens(self, text: str) -> int:
        """Count tokens in text"""
        pass
