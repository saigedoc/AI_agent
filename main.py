import ollama
import asyncio
from tools import available_functions, tools

async def main():
    client = ollama.AsyncClient(
        host="http://127.0.0.1:11434"
    )

    max_deep = 5
    model = "ToolAce"
    messages = [
        {
            "role": "system",
            "content": """
Ты умный ИИ помошник в Windows 11. Ты помогаешь пользователю искать информацию, файлы, открывать файлы и программы  т. д. Твои ответы должны быть краткими и информативными.
Ты пользуешься функциями для выполнения поставленных задач. Всегда говори на русском. Всегда выполняй задачу. Никогда не ври и не придумывай, если ты не знаешь информации, скажи что не знаешь.
Если тебе не удалось выполнить задачу, скажу что ты не смог её выполнить. НИКОГДА НЕ ВРИ И НЕ ПРИДУМЫВАЙ. ТЕБЕ ЗАПРЕЩЕНО ВРАТЬ И ПРИДУМЫВАТЬ. НЕЛЬЗЯ ПРИДУМЫВАТЬ. НЕЛЬЗЯ ВРАТЬ.
"""
        },
    ]

    last_user_prompt = [
        {
            "role": "user",
            "content": "найди игру Baldurs Gate на диске D"
        }
    ]
    messages=messages+last_user_prompt
    t = 0
    think = True
    while think:
        think = False
        print(f"______________deep#{t}______________")

        responce = await client.chat(
            model=model,
            messages=messages,
            tools=tools
        )
        print("resp:", responce["message"]["content"])
        messages.append(responce["message"])
        #if not responce['message'].get('tool_calls'):
        #    print(responce["message"]["content"])
        if responce['message'].get('tool_calls'):
            print("tools:", responce["message"]["tool_calls"])
            for tool in responce["message"]["tool_calls"]:
                function_to_call = available_functions[tool["function"]["name"]]
                args = list(tool["function"]["arguments"].values())
                function_responce = function_to_call(*args)
                print("tool:", function_responce)
                if function_responce == "think":
                    think = True
                    messages.append(
                        {
                            "role": "tool",
                            "content": "Продолжение решения задачи."
                        }
                    )
                else:
                    messages.append(
                        {
                            "role": "tool",
                            "content": function_responce
                        }
                    )
        else:
            final_responce = await client.chat(model=model, messages=messages)
            print(final_responce["message"]["content"])
            #print("resp:", responce["message"]["content"])
            #messages.append(responce["message"])

        t += 1
        if t >= max_deep:
            think = False
    
    print("end__deep")
    final_responce = await client.chat(model=model, messages=messages)
    print(final_responce["message"]["content"])
    return

if __name__ == "__main__":
    #available_functions["find_file"]
    #print(available_functions["find_file"](['*.mkv'], 'E:/'))
    #1/0
    asyncio.run(main())