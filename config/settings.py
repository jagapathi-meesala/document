import os

DOCUMENT_MAX_SIZE_MB = int(os.getenv("DOCUMENT_MAX_SIZE_MB", "10"))
DOCUMENT_MAX_PAGES = int(os.getenv("DOCUMENT_MAX_PAGES", "100"))
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
