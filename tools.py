import subprocess
import os
import fnmatch
import time

def execute_command(command: str):
    print(command)
    responce = subprocess.run(command.split(), shell=True, capture_output=True)
    return f"returncode: {responce.returncode}, stdout: {responce.stdout}, stderr: {responce.stderr}"

def find_file(path: str, pattern: str):
    result = []
    time_start = time.time()
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern) and os.path.join(root, name) not in result:
                result.append(os.path.join(root, name))
            if time.time() - time_start >= 10:
                return ';'.join(result) if result != [] else "Nothing was find."
    return ';'.join(result) if result != [] else "Nothing was find."

def continue_think():
    return "think"

def read_file(path):
    with open(path, 'r') as f:
        text = f.read()
    return text

def write_file(path, text):
    with open(path, 'w') as f:
        f.write(text)

tools=[
    {
        "type": 'function',
        "function": {
            "name": "execute_command",
            "description": "Function to execute cmd commands in windows 11. Example: start cmd /c",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "string command which will be execute."
                        }
                    },
                "required": ["command"],
                }
            }
    },
    {
        "type": 'function',
        "function": {
            "name": "continue_think",
            "description": "Function to repeat your work, if you didn't complete the task. Example: you need find file, you finded nothink you need, you use this function to repeat it on another drive or try with another command.",
            }
    },
    {
        "type": 'function',
        "function": {
            "name": "find_file",
            "description": "Function to find files in path with come pattern. Function with time limit, if find nothing try find with more accurate search. Example: you need to find video.",
            "parameters": {
                "type": "object",
                "properties": {
                    "pattern": {
                        "type": "str",
                        "description": "Str pattern, use pattern which will be very accurate and maximum repeat target filename. Example: '*.mkv' or '*film*.*'."
                        },
                    "path": {
                        "type": "str",
                        "description": "Path in drive. Example: 'E:/' or 'D:/!Games'."
                    }
                    },
                "required": ["patterns", "path"],
                }
            }
    },
    {
        "type": 'function',
        "function": {
            "name": "read_file",
            "description": "Function to read file in path. Example: you need to read code in 'main.py'.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "str",
                        "description": "path to file you want to read. Example: 'myproject/data/microcontroler.cpp' or 'заметки/список фильмов.txt'."
                        }
                    },
                "required": ["path"],
                }
            }
    },
    {
        "type": 'function',
        "function": {
            "name": "write_file",
            "description": "Function to write/rewrite file in path. Example: you need to rewrite code in 'main.py'.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "str",
                        "description": "Path to file you want to read. Example: 'myproject/data/microcontroler.cpp' or 'заметки/список фильмов.txt'."
                        },
                    "text": {
                        "type": "str",
                        "description": r"Text you want to write in file include \n, \t and other. Example: 'import random\nprint(f'your number is {random.randint(1,10)}')'."
                        }
                    },
                "required": ["path", "text"],
                }
            }
    }
]

available_functions = {
                'execute_command': execute_command,
                'continue_think': continue_think,
                'find_file': find_file,
                'read_file': read_file,
                'write_file': write_file
            }