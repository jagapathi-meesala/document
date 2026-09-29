import pytest
import os
import yaml

def test_agent_yaml_validity():
    with open("agent.yaml", "r") as f:
        agent = yaml.safe_load(f)
        
    assert agent["name"] == "document-intelligence-agent"
    assert agent["version"] == "0.1.0"
    assert "description" in agent
    assert "extract-document-text" in agent["tools"]

def test_tool_yamls_validity():
    tools_dir = "tools"
    for filename in os.listdir(tools_dir):
        if filename.endswith(".yaml"):
            with open(os.path.join(tools_dir, filename), "r") as f:
                tool = yaml.safe_load(f)
            assert "name" in tool
            assert "description" in tool
            assert "input_schema" in tool
