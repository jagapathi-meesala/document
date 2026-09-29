import os
from typing import Any, Dict
from contracts.tool_contract import ToolContract
from pypdf import PdfReader

class ExtractDocumentTextTool(ToolContract):
    def name(self) -> str:
        return "extract-document-text"

    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        source_path = input_data.get("source_path")
        if not source_path:
            raise ValueError("source_path is required.")

        if not os.path.exists(source_path):
            raise ValueError(f"File not found: {source_path}")

        max_pages = input_data.get("max_pages", None)
        _, ext = os.path.splitext(source_path.lower())

        result = {
            "source": source_path,
            "document_type": ext.lstrip('.'),
            "text": "",
            "page_count": 0,
            "metadata": {}
        }

        if ext == ".txt":
            try:
                with open(source_path, 'r', encoding='utf-8') as f:
                    result["text"] = f.read()
                result["page_count"] = 1
            except Exception as e:
                raise RuntimeError(f"Error reading TXT file: {str(e)}")

        elif ext == ".pdf":
            try:
                reader = PdfReader(source_path)
                result["page_count"] = len(reader.pages)
                pages_to_extract = result["page_count"]
                if max_pages and max_pages < pages_to_extract:
                    pages_to_extract = max_pages

                text_parts = []
                for i in range(pages_to_extract):
                    page_text = reader.pages[i].extract_text()
                    if page_text:
                        text_parts.append(page_text)
                
                result["text"] = "\n".join(text_parts)
                if not result["text"].strip():
                    result["metadata"]["warning"] = "Extraction produced empty text. Scanned images are not supported."
            except Exception as e:
                raise RuntimeError(f"Error reading PDF file: {str(e)}")

        else:
            raise ValueError(f"Unsupported format: {ext}. Only .txt and .pdf are supported.")

        return result
