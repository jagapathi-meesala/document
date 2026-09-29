# Rules

## Must Always:
- Validate all inputs thoroughly.
- Report processing failures with structured error codes.
- Preserve source boundaries (do not mix content from multiple files unless explicitly comparing).
- Avoid fabricated information (no hallucination).
- Return structured, deterministic results.

## Must Never:
- Expose secrets or credentials in logs or output.
- Invent extracted information that does not exist in the source document.
- Silently ignore malformed input or missing files.
- Claim unsupported file formats (only TXT and PDF are supported initially).
- Claim external API execution when none occurred.
- Claim professional, legal, or medical conclusions based on document content.

## Limitations:
- No Optical Character Recognition (OCR) is implemented. Scanned PDFs without a text layer cannot be read.
- No generative AI (LLMs) is used. Summarization and extraction are purely heuristic and deterministic.
- File sizes and page counts may be limited by environment configuration to prevent resource exhaustion.
