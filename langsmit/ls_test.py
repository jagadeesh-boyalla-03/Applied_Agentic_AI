
import os
from dotenv import load_dotenv
from langsmith import Client

load_dotenv(override=True)

print("API key loaded:", bool(os.getenv("LANGSMITH_API_KEY")))
print("Tracing:", os.getenv("LANGSMITH_TRACING"))

try:
    client = Client()
    projects = list(client.list_projects(limit=3))
    print("LangSmith connection successful!")
    print("Projects:", [p.name for p in projects])

except Exception as e:
    print("LangSmith connection failed:", e)
