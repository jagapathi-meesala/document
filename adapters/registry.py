from typing import Dict
from .adapter import FrameworkAdapter
from core.agent_core import AgentCore

class AdapterRegistry:
    """
    A registry to manage different framework adapters if needed.
    """
    def __init__(self):
        self.adapters: Dict[str, FrameworkAdapter] = {}
        
    def register(self, name: str, adapter: FrameworkAdapter):
        self.adapters[name] = adapter
        
    def get(self, name: str) -> FrameworkAdapter:
        if name not in self.adapters:
            raise ValueError(f"Adapter {name} not found.")
        return self.adapters[name]
