import os
from dotenv import load_dotenv
from langsmith import traceable

load_dotenv()

@traceable
def student_monitor(name, marks):
    if marks >= 80:
        feedback = "Good Performance"
    else:
        feedback = "Need more Practice"

    return f"{name} : {feedback}"

result = student_monitor("Vijay", 90)
print(result)