from typing import Any, Dict
from abc import ABC, abstractmethod

class ToolContract(ABC):
    """
    Interface that all domain tools must implement.
    """
    
    @abstractmethod
    def name(self) -> str:
        """Return the unique name of the tool, matching the YAML manifest."""
        pass
        
    @abstractmethod
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the tool with the given input data.
        Should return a dictionary containing the structured result.
        Raises ValueError on invalid input or RuntimeError on processing failures.
        """
        pass
