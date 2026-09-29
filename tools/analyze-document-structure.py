import re
from typing import Any, Dict
from contracts.tool_contract import ToolContract

class AnalyzeDocumentStructureTool(ToolContract):
    def name(self) -> str:
        return "analyze-document-structure"

    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        text = input_data.get("text")
        if text is None:
            raise ValueError("text is required.")

        if not text.strip():
            return {
                "character_count": 0,
                "word_count": 0,
                "line_count": 0,
                "paragraph_count": 0,
                "heading_candidates": [],
                "empty_sections": True
            }

        char_count = len(text)
        words = text.split()
        word_count = len(words)
        
        lines = text.split('\n')
        line_count = len(lines)
        
        paragraphs = [p for p in text.split('\n\n') if p.strip()]
        paragraph_count = len(paragraphs)
        
        # Simple heuristic for headings: short lines that are Title Cased or ALL CAPS
        heading_candidates = []
        for line in lines:
            stripped = line.strip()
            if 0 < len(stripped) < 100:
                if stripped.istitle() or (stripped.isupper() and len(stripped.split()) > 1):
                    # Exclude very short single words unless they look like headers
                    if len(stripped.split()) >= 1 or len(stripped) > 3:
                        heading_candidates.append(stripped)

        return {
            "character_count": char_count,
            "word_count": word_count,
            "line_count": line_count,
            "paragraph_count": paragraph_count,
            "heading_candidates": heading_candidates[:20],  # cap at 20
            "empty_sections": False
        }
