from typing import Any, Dict
from contracts.agent_contract import AgentContract
from core.result import Result
from core.registry import DynamicToolRegistry

class AgentCore(AgentContract):
    def __init__(self, tools_dir: str = "tools"):
        self.registry = DynamicToolRegistry(tools_dir)
        self.registry.discover()
        
    def execute(self, request: Dict[str, Any]) -> Result:
        if not isinstance(request, dict) or "tool" not in request:
            return Result.fail("unknown", "INVALID_REQUEST", "Request must be a dictionary with a 'tool' field.")
            
        tool_name = request["tool"]
        input_data = request.get("input", {})
        
        if not isinstance(input_data, dict):
            return Result.fail(tool_name, "INVALID_INPUT", "Input must be a dictionary.")
            
        return self.registry.execute_tool(tool_name, input_data)
