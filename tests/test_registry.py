import pytest
from core.registry import DynamicToolRegistry

def test_registry_discovery():
    registry = DynamicToolRegistry()
    registry.discover()
    tools = registry.list_tools()
    
    assert "extract-document-text" in tools
    assert "analyze-document-structure" in tools
    assert "extract-key-information" in tools
    assert "summarize-document" in tools
    assert "compare-documents" in tools
