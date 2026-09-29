from typing import Any, Dict
from core.agent_core import AgentCore
from core.result import Result

class FrameworkAdapter:
    """
    Example base adapter to show how external frameworks (e.g., LangChain)
    can wrap the AgentCore.
    """
    def __init__(self, core: AgentCore):
        self.core = core
        
    def invoke(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generic invocation method that translates framework calls into 
        AgentCore requests.
        """
        request = {
            "tool": tool_name,
            "input": parameters
        }
        result = self.core.execute(request)
        return result.to_dict()
