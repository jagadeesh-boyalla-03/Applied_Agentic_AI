import ollama

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break

    response = ollama.chat(
        model="llama3.1:latest",
        messages=[
            {
                "role": "user",
                "content": user_input
            }
        ]
    )
    print("\n AI:", response.message.content)