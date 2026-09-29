# Document Intelligence Agent

## Purpose
A deterministic, framework-independent document intelligence agent built for the HiDevs x Lyzr Agent Passport program. It reliably extracts text, analyzes structure, and extracts key information from documents without relying on generative AI hallucinations.

## Features
- **Deterministic Processing**: Rule-based and heuristic document analysis.
- **Dynamic Tool Registry**: Discovers tools dynamically via OpenGAP YAML manifests.
- **Framework Agnostic**: Core business logic is decoupled from any specific AI framework (LangChain, CrewAI, etc.).
- **Structured Error Handling**: Returns predictable, machine-readable results.

## Architecture
```
External Framework / CLI / Tests
            |
            v
      Adapter Layer
            |
            v
        AgentCore
            |
            v
   Dynamic Tool Registry
            |
            v
       Tool Contracts
            |
            v
        Domain Tools
            |
            v
      Document Services
```

## Project Structure
- `agent.yaml`: OpenGAP agent manifest.
- `tools/`: OpenGAP compliant tool YAML definitions and Python implementations.
- `core/`: AgentCore and structured Result definitions.
- `contracts/`: Tool and agent interfaces.
- `adapters/`: Integration layer for external frameworks.
- `tests/`: Pytest suite.
- `verification/`: Readiness audits, security checks, and OpenGAP validation research.

## Supported Document Formats
- Text files (`.txt`)
- PDF documents (`.pdf`, text-layer only)

## Tool List
1. `extract-document-text`
2. `analyze-document-structure`
3. `extract-key-information`
4. `summarize-document`
5. `compare-documents`

## Installation
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage
The agent can be tested locally using the provided test suite or by directly invoking the `AgentCore` in Python:

```python
from core.agent_core import AgentCore
from core.result import Result

core = AgentCore()
request = {
    "tool": "extract-document-text",
    "input": {
        "source_path": "sample.txt"
    }
}
result = core.execute(request)
print(result.to_dict())
```

## Example Input
```json
{
  "tool": "summarize-document",
  "input": {
    "source_path": "report.pdf",
    "max_sentences": 3
  }
}
```

## Example Output
```json
{
  "success": true,
  "tool": "summarize-document",
  "result": {
    "summary": "This is the first important sentence. This is the second. And the third.",
    "method": {
      "type": "extractive",
      "external_model": false
    }
  },
  "error": null
}
```

## Testing
Run the test suite:
```bash
python3 -m pytest -q
```

## OpenGAP Validation
This project targets OpenGAP specification `0.1.0`. Validation can be run if the official CLI is installed:
```bash
opengap validate
```

## Security
- Treats all documents as untrusted.
- Never executes `eval()` or arbitrary code from documents.
- Stores no credentials or API keys (purely deterministic operations).

## Portability
- Core is written in pure Python.
- Framework interoperability is strictly architectural (adapters can be written, but core runs standalone).

## Limitations
- No generative AI is used.
- No OCR (cannot read scanned images).

## Verification
Run all audits before pushing:
```bash
python3 verification/security_audit.py
python3 verification/documentation_audit.py
python3 verification/hidevs_readiness_audit.py
```

## Repository Status
- **LOCALLY VERIFIED**: Dynamic registry, tool execution, tests, security audit, documentation audit.
- **NOT VERIFIED**: HiDevs platform cloning and Passport issuance (requires external submission).

## HiDevs Status
- **Cloning**: NOT VERIFIED
- **Validation**: NOT VERIFIED
- **Exporting**: NOT VERIFIED
- **Issuing**: NOT VERIFIED
- **Passport**: NOT VERIFIED
