import os
import json
import yaml

def run_readiness_audit():
    issues = []
    
    # 1-3. agent.yaml
    if not os.path.exists("agent.yaml"):
        issues.append("agent.yaml is missing.")
    else:
        try:
            with open("agent.yaml", "r") as f:
                agent = yaml.safe_load(f)
            if "name" not in agent or "version" not in agent or "description" not in agent:
                issues.append("agent.yaml missing required fields (name, version, description).")
        except Exception as e:
            issues.append(f"agent.yaml fails to parse: {e}")

    # 4-6. Tools
    tools_dir = "tools"
    if not os.path.exists(tools_dir):
        issues.append("tools/ directory is missing.")
    else:
        tool_yamls = [f for f in os.listdir(tools_dir) if f.endswith(".yaml")]
        for ty in tool_yamls:
            try:
                with open(os.path.join(tools_dir, ty), "r") as f:
                    t = yaml.safe_load(f)
                if "name" not in t or "description" not in t or "input_schema" not in t:
                    issues.append(f"Tool {ty} missing required schema fields.")
            except Exception as e:
                issues.append(f"Tool {ty} fails to parse: {e}")
                
            py_impl = ty.replace(".yaml", ".py")
            if not os.path.exists(os.path.join(tools_dir, py_impl)):
                issues.append(f"Implementation {py_impl} missing for {ty}.")

    # 7-11. Core, Registry, Adapters, Contracts
    if not os.path.exists("core/registry.py"): issues.append("Registry missing.")
    if not os.path.exists("core/agent_core.py"): issues.append("AgentCore missing.")
    if not os.path.exists("adapters/adapter.py"): issues.append("Adapters missing.")
    if not os.path.exists("contracts/tool_contract.py"): issues.append("Contracts missing.")
    
    # 13-20. Docs
    docs = ["README.md", "SOUL.md", "RULES.md", "DUTIES.md", "AGENTS.md", "EXPLAINABILITY.md", ".gitignore", ".env.example"]
    for d in docs:
        if not os.path.exists(d):
            issues.append(f"{d} missing.")

    if not os.path.exists("verification/checkpoint_matrix.yaml"):
        issues.append("checkpoint_matrix.yaml missing.")

    result = {
        "status": "FAILED" if issues else "PASSED",
        "issues": issues,
        "details": []
    }
    
    print(json.dumps(result, indent=2))
    
    if issues:
        exit(1)
    else:
        exit(0)

if __name__ == "__main__":
    run_readiness_audit()
