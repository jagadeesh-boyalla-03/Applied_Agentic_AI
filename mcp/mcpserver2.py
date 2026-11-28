from mcp.server import MCPServer

mcp = MCPServer("AI Student mentor")

# In-memory student dataset
students = {
    "101": {"name": "Nihantha", "score": 70},
    "102": {"name": "Balaji", "score": 100},
}


@mcp.tool()
def list_students() -> list:
    """List all students and their records."""
    return [
        {"id": student_id, **details}
        for student_id, details in students.items()
    ]


@mcp.tool()
def add_student(student_id: str, name: str, score: int) -> str:
    """Add a student using a unique ID, name, and score."""
    if student_id in students:
        return "Student ID already exists."

    if not 0 <= score <= 100:
        return "Score must be between 0 and 100."

    students[student_id] = {"name": name, "score": score}
    return f"Student {name} added successfully."


@mcp.tool()
def delete_student(sid: str) -> str:
    """Delete a student using their student ID."""
    if sid not in students:
        return "Student not found."

    del students[sid]
    return f"Student {sid} deleted successfully."


if __name__ == "__main__":
    mcp.run()