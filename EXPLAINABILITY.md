# Purpose
This document explains the internal mechanisms, algorithms, and limitations of the Document Intelligence Agent to ensure transparency and trust in its operations.

# Inputs and Data Sources
The agent accepts local file paths as inputs. Currently supported formats are `.txt` and `.pdf`. The agent does not connect to external data sources or databases to retrieve documents.

# Processing Pipeline
Requests are routed through a `DynamicToolRegistry` by the `AgentCore`. The core validates inputs against the expected schema, invokes the requested tool, and returns a structured result. 

# Document Extraction
- **TXT**: Read directly using Python's standard `open` function with UTF-8 encoding.
- **PDF**: Extracted using the `pypdf` library. 
- *Note:* No Optical Character Recognition (OCR) is implemented. If a PDF consists only of images, the text extraction will return empty or minimal text, and this will be explicitly reported.

# Structural Analysis
Structural analysis is purely heuristic:
- **Character/Word/Line Count**: Calculated via string splitting and length measurements.
- **Paragraph Count**: Estimated by splitting on double newlines (`\n\n`).
- **Heading Candidates**: Identified by looking for short lines that are capitalized or precede structural breaks.

# Key Information Extraction
Key information extraction relies on deterministic, rule-based heuristics (e.g., regex, keyword proximity, line position) rather than LLM inference.
- If a requested field (e.g., "date") cannot be confidently identified, it is returned as `null` with a reason (e.g., `not_found`), rather than fabricated.

# Summarization
Summarization is *extractive*, not *generative*.
- Sentences are split and scored based on term frequency and position.
- The highest-scoring sentences are returned as the summary.
- *Note:* No external AI model or API is used for summarization.

# Document Comparison
Comparison uses deterministic string comparison algorithms (e.g., Python's `difflib`). It detects added, removed, and unchanged lines. It does not perform semantic similarity comparison.

# Decision and Reasoning
The agent does not make business or external decisions. Its "reasoning" is limited to parsing structured input, routing to the correct tool, and assembling the output.

# Tools and Capabilities
- `extract-document-text`: Reads and returns raw text.
- `analyze-document-structure`: Returns heuristic counts and structural elements.
- `extract-key-information`: Locates specific data points using rules.
- `summarize-document`: Generates an extractive summary.
- `compare-documents`: Finds line-by-line differences between two files.

# Dynamic Tool Discovery
Tools are defined as YAML files conforming to the OpenGAP specification in the `tools/` directory. The `DynamicToolRegistry` scans this directory at runtime, loads the schemas, and maps them to corresponding Python implementations.

# AgentCore
The `AgentCore` is the central orchestrator. It acts as the execution engine, isolating business logic from external frameworks.

# Error Handling
Errors are caught and translated into structured `Result` objects with stable codes (e.g., `FILE_NOT_FOUND`, `UNSUPPORTED_FORMAT`). Stack traces are not leaked to the user.

# Security
- Document content is treated as untrusted and is never executed (no `eval()` or `exec()`).
- The agent does not require API keys for its deterministic operations.
- Environment variables (if any) are managed securely and not hardcoded.

# Portability
The core logic relies entirely on pure Python standard libraries (plus `pypdf`). It does not depend on LangChain, CrewAI, or any other framework, though it can be easily wrapped for use within them.

# Verification
The agent includes automated test scripts and readiness audits that inspect the code for compliance with these claims.

# Limitations and Constraints
- No OCR.
- No generative AI or semantic understanding.
- File sizes and processing times may be constrained by local hardware.

# Expected Output
Outputs are deterministic JSON objects containing `success`, `result`, and `error` fields.

# Non-Claims
We explicitly DO NOT claim:
- GPT or Gemini usage.
- OCR capabilities.
- Cloud storage or vector database integration.
- LangChain, MCP, or A2A execution (unless explicitly adapted and tested in a host environment).
