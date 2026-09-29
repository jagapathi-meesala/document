import os
import re

def run_security_audit():
    print("Running Security Audit...")
    failed = False
    
    if not os.path.exists(".env.example"):
        print("FAIL: .env.example does not exist.")
        failed = True
        
    if os.path.exists(".gitignore"):
        with open(".gitignore", "r") as f:
            if ".env" not in f.read():
                print("FAIL: .env not found in .gitignore.")
                failed = True
    else:
        print("FAIL: .gitignore does not exist.")
        failed = True

    # Scan files for obvious secrets (skip .git, venv)
    secret_patterns = [
        re.compile(r'API_KEY\s*=\s*[a-zA-Z0-9]{10,}'),
        re.compile(r'SECRET\s*=\s*[a-zA-Z0-9]{10,}'),
        re.compile(r'PASSWORD\s*=\s*[a-zA-Z0-9]{10,}'),
        re.compile(r'TOKEN\s*=\s*[a-zA-Z0-9]{10,}'),
        re.compile(r'BEGIN\s+PRIVATE\s+KEY'),
    ]

    for root, dirs, files in os.walk("."):
        if ".git" in root or "venv" in root or "__pycache__" in root:
            continue
            
        for file in files:
            if file == ".env" or file.endswith(".pyc") or file.endswith(".log"):
                continue
                
            path = os.path.join(root, file)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                    for pattern in secret_patterns:
                        if pattern.search(content):
                            print(f"FAIL: Suspicious secret found in {path}")
                            failed = True
            except UnicodeDecodeError:
                pass
                
    if failed:
        print("Security Audit: FAILED")
        exit(1)
    else:
        print("Security Audit: PASSED")
        exit(0)

if __name__ == "__main__":
    run_security_audit()
