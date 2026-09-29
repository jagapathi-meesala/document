import re
from typing import Any, Dict
from contracts.tool_contract import ToolContract

class ExtractKeyInformationTool(ToolContract):
    def name(self) -> str:
        return "extract-key-information"

    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        text = input_data.get("text")
        requested_fields = input_data.get("requested_fields")

        if not text or not requested_fields:
            raise ValueError("text and requested_fields are required.")

        result = {}
        lines = text.split('\n')
        
        for field in requested_fields:
            field_lower = field.lower()
            found_value = None
            
            # Simple heuristic: Look for lines like "Field: Value" or "Field - Value"
            pattern = re.compile(rf'^{re.escape(field)}[\s]*[:\-]+[\s]*(.+)$', re.IGNORECASE)
            
            for line in lines[:50]:  # Usually metadata is near the top
                match = pattern.search(line.strip())
                if match:
                    found_value = match.group(1).strip()
                    break
                    
            if found_value:
                result[field] = {"value": found_value, "status": "found"}
            else:
                result[field] = {"value": None, "status": "not_found"}

        return result
