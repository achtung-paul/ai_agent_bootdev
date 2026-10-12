import os
from config import MAX_CHARS

def get_file_content(working_directory: str, file_path: str) -> str:

    #get directory info to allow check of path to stop LLM escaping.
    llm_allowed_path = os.path.abspath(working_directory)
    llm_target_file = os.path.abspath(os.path.join(llm_allowed_path, file_path))
    

    try:

        valid_target_file = os.path.commonpath([llm_allowed_path, llm_target_file]) == llm_allowed_path
            
        if not valid_target_file:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
        if not os.path.isfile(llm_target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(llm_target_file, "r") as f:
                    file_content_string = f.read(MAX_CHARS)
                    if f.read(1):
                        file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                        
                    return file_content_string

    except Exception as e:
            return f"Error: {e}"


schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Reads a files contents and returns a string of the content, the string is truncated over a max character setting",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path to the file relative to the working directory."
                },
                
            },
            "required": ["file_path"],
            "additionalProperties": False,
        },
    },
}    