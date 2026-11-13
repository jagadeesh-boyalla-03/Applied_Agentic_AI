#using LLM through ollama in the python code
import ollama
response=ollama.chat(
    model="llama3.1:latest",
    messages=[
        {
            "role": "user",
            "content": "popular jobs title related to GENAI"
        }
    ]
)
print(response.message.content)