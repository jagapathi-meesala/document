from dataclasses import dataclass
from typing import Any, Dict, Optional

@dataclass
class Result:
    success: bool
    tool: str
    result: Optional[Dict[str, Any]]
    error: Optional[Dict[str, Any]]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "tool": self.tool,
            "result": self.result,
            "error": self.error
        }

    @staticmethod
    def ok(tool: str, result: Dict[str, Any]) -> 'Result':
        return Result(success=True, tool=tool, result=result, error=None)

    @staticmethod
    def fail(tool: str, code: str, message: str) -> 'Result':
        return Result(success=False, tool=tool, result=None, error={"code": code, "message": message})
