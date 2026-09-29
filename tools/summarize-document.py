import re
from typing import Any, Dict
from contracts.tool_contract import ToolContract

class SummarizeDocumentTool(ToolContract):
    def name(self) -> str:
        return "summarize-document"

    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        text = input_data.get("text")
        if not text:
            raise ValueError("text is required.")
            
        max_sentences = input_data.get("max_sentences", 3)
        
        # Split into sentences (basic regex for .!?)
        sentences = re.split(r'(?<=[.!?])\s+', text.strip())
        sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
        
        if not sentences:
            return {
                "summary": "",
                "key_points": [],
                "source_statistics": {"total_sentences": 0},
                "method": {"type": "extractive", "external_model": False}
            }

        # Naive scoring based on word count (longer sentences score higher up to a limit)
        # And positional bonus (first and last sentences often important)
        scored_sentences = []
        for i, s in enumerate(sentences):
            words = len(s.split())
            score = words
            if i == 0 or i == len(sentences) - 1:
                score += 10
            scored_sentences.append((score, i, s))
            
        # Sort by score descending, pick top max_sentences, then sort by original index
        scored_sentences.sort(key=lambda x: x[0], reverse=True)
        top_sentences = scored_sentences[:max_sentences]
        top_sentences.sort(key=lambda x: x[1])
        
        summary_text = " ".join([s[2] for s in top_sentences])
        
        return {
            "summary": summary_text,
            "key_points": [s[2] for s in top_sentences],
            "source_statistics": {
                "total_sentences": len(sentences),
                "extracted_sentences": len(top_sentences)
            },
            "method": {
                "type": "extractive",
                "external_model": False
            }
        }
