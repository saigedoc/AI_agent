import ollama
import asyncio
import subprocess

def execute_command(command: str):
    return subprocess.run(command.split(), shell=True, capture_output=True).stdout.decode("utf-8")

async def main():
    client = ollama.AsyncClient(
        host="http://127.0.0.1:11434"
    )
    messages = [
        {
            "role": "user",
            "content": "Исполни команду 'ollama list' и напиши результат"
        }
    ]

    responce = await client.chat(
        model="qwen2.5-coder:3b",
        messages=messages,
        tools=[
            {
                "type": 'function',
                "function": {
                    "name": "execute_command",
                    "description": "function which execute cmd command on windows 11.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "command": {
                                "type": "string",
                                "description": "string command which wil be execute."
                            }
                        },
                        "required": ["command"],
                    }
                }
            }
        ]
    )

    messages.append(responce["message"])
    if not responce['message'].get('tool_calls'):
        print(responce["message"]["content"])
        return
    if responce['message'].get('tool_calls'):
        available_functions = {
            'execute_command': execute_command
        }
        for tool in responce["message"]["tool_calls"]:
            function_to_call = available_functions[tool["function"]["name"]]
            function_responce = function_to_call(tool["function"]["arguments"]["command"])

            messages.append(
                {
                    "role": "tool",
                    "content": function_responce
                }
            )

    final_responce = await client.chat(model="qwen2.5-coder:3b", messages=messages)
    print(final_responce["message"]["content"])

if __name__ == "__main__":
    asyncio.run(main())