import ollama

# Memory
messages = [
    {
        "role": "system",
        "content": "Behave like a Data Scientist and answer the questions accordingly. You are a helpful assistant."
    }
]

while True:
    try:
        question = input("\n You: ")   

        if question.lower() == "exit":
            break

        messages.append(
            {
                "role": "user",
                "content": question,
            }    
        )

        response = ollama.chat(
            model="llama3.1:latest",
            messages=messages
        )   

        ans = response.message.content

        print("\n AI:", ans)

        messages.append(
            {
                "role": "assistant",
                "content": ans,
            }    
        )

    except Exception as e:
        print("\nSomething went wrong:", e)
