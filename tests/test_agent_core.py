import pytest
import os
from core.agent_core import AgentCore
from core.result import Result

@pytest.fixture
def core():
    return AgentCore()

def test_agent_core_execute_unknown_tool(core):
    request = {"tool": "fake-tool", "input": {}}
    result = core.execute(request)
    assert result.success is False
    assert result.error["code"] == "UNKNOWN_TOOL"

def test_agent_core_execute_invalid_request(core):
    result = core.execute("not-a-dict")
    assert result.success is False
    assert result.error["code"] == "INVALID_REQUEST"

def test_agent_core_extract_text(core):
    # Create sample doc
    with open("sample.txt", "w") as f:
        f.write("Hello world.")
    
    request = {"tool": "extract-document-text", "input": {"source_path": "sample.txt"}}
    result = core.execute(request)
    assert result.success is True
    assert result.result["text"] == "Hello world."
    
    os.remove("sample.txt")
