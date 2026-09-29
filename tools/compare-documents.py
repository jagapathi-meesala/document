import difflib
from typing import Any, Dict
from contracts.tool_contract import ToolContract

class CompareDocumentsTool(ToolContract):
    def name(self) -> str:
        return "compare-documents"

    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        text1 = input_data.get("text1")
        text2 = input_data.get("text2")

        if text1 is None or text2 is None:
            raise ValueError("text1 and text2 are required.")

        lines1 = text1.splitlines()
        lines2 = text2.splitlines()

        matcher = difflib.SequenceMatcher(None, lines1, lines2)
        added_lines = 0
        removed_lines = 0
        unchanged_lines = 0

        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == 'replace':
                removed_lines += (i2 - i1)
                added_lines += (j2 - j1)
            elif tag == 'delete':
                removed_lines += (i2 - i1)
            elif tag == 'insert':
                added_lines += (j2 - j1)
            elif tag == 'equal':
                unchanged_lines += (i2 - i1)

        total_lines = max(len(lines1), len(lines2))
        similarity = matcher.ratio()

        return {
            "added_content_lines": added_lines,
            "removed_content_lines": removed_lines,
            "unchanged_lines": unchanged_lines,
            "similarity_metrics": {
                "ratio": round(similarity, 4)
            },
            "structural_differences": {
                "line_count_diff": len(lines2) - len(lines1)
            }
        }
