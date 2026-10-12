import os


def write_file(working_directory: str, file_path: str, content: str) -> str:

    llm_allowed_path = os.path.abspath(working_directory)
    llm_target_file = os.path.abspath(os.path.join(llm_allowed_path, file_path))
        
    
    try:
    
        valid_target_file = os.path.commonpath([llm_allowed_path, llm_target_file]) == llm_allowed_path
                
        if not valid_target_file:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(llm_target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        else: 
            dir_path= os.path.dirname(llm_target_file)
            os.makedirs(dir_path, exist_ok=True)
        
            with open(llm_target_file, "w") as f:
                f.write(content)
                return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
                return f"Error: {e}"


schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "writes a file to the relative working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path to the file relative to the working directory."
                },
                "content": {
                    "type": "string",
                    "description": "the content of the file, it is not optional",
                }
            },
            "required": ["file_path", "content"],
            "additionalProperties": False,
        },
    },
}    
    