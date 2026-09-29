from typing import Any, Dict
from abc import ABC, abstractmethod
from core.result import Result

class AgentContract(ABC):
    """
    Interface for the AgentCore to ensure a consistent boundary.
    """
    
    @abstractmethod
    def execute(self, request: Dict[str, Any]) -> Result:
        """
        Process a structured request.
        Request must contain at least:
        {
            "tool": "tool-name",
            "input": { ... }
        }
        """
        pass
