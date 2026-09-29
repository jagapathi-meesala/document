import os

def run_documentation_audit():
    print("Running Documentation Audit...")
    failed = False
    
    required_docs = ["README.md", "SOUL.md", "RULES.md", "DUTIES.md", "AGENTS.md", "EXPLAINABILITY.md", "agent.yaml"]
    for doc in required_docs:
        if not os.path.exists(doc):
            print(f"FAIL: {doc} is missing.")
            failed = True
            
    if not failed:
        with open("EXPLAINABILITY.md", "r") as f:
            content = f.read()
            # Verify explicit non-claims
            if "OCR" not in content or "LangChain" not in content or "Generative" not in content:
                print("Warning: EXPLAINABILITY.md might not explicitly state all non-claims.")
                # We won't fail just for the warning if it's there
                
    if failed:
        print("Documentation Audit: FAILED")
        exit(1)
    else:
        print("Documentation Audit: PASSED")
        exit(0)

if __name__ == "__main__":
    run_documentation_audit()
