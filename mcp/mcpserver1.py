# code the mcp server
# mcp server will help to connect with the tools/functions

# Libraries
import os
from dotenv import load_dotenv
from groq import Groq
from mcp.server import MCPServer  # help to connect with tools

load_dotenv()

mcp = MCPServer("AI Student Mentor")  # Create the mcp server and assign a name

llm = Groq(api_key=os.environ["GROQ_API_KEY"])

students = {
    "101": {"name": "Nihantha", "score": 70},
    "102": {"name": "Balaji", "score": 100}
}

# listing/printing all the students in the database/dictionary
@mcp.tool()
def list_students() -> list:
    """list all students"""

    student_list = [
        {"id": key, **value}
        for key, value in students.items()
    ]

    return student_list


@mcp.tool()
def add_student(student_id: str, name: str, score: int) -> str:
    """Add a student"""

    if student_id in students:
        return "Student ID already exist"

    students[student_id] = {"name": name, "score": score}
    return "Student added Successfully"


@mcp.tool()
def delete_student(sid: str) -> str:
    """Delete a Student"""

    if sid not in students:
        return "Student not found"

    del students[sid]
    return "Student deleted Successfully"

#using llm to gett the advice based upon marks
@mcp.tool()
def student_advice(sid : str) -> str:
    """Generate AI student Advice"""
    student = students.get(sid)
    if not student:
        return "Student not found"

    result = llm.chat.completions.create(
        model = "openai/gpt-oss-120b",

        messages = [
            {"role" : "system", "content" : "Behave like a teacher. Give reply in meaningful way based upon the student score"},
            {"role" : "user", "content" : f"Provide feedback for {students[sid]}" }
        ]
    )
    return result.choices[0].message.content