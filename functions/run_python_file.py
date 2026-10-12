import os
import subprocess


def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
      
    output_holder = []
    
    try:

        llm_allowed_path = os.path.abspath(working_directory)
        llm_target_file = os.path.abspath(os.path.join(llm_allowed_path, file_path))

        valid_target_file = os.path.commonpath([llm_allowed_path, llm_target_file]) == llm_allowed_path
                    
        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
                    
    
        if not os.path.isfile(llm_target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not llm_target_file.endswith('.py'):
           return f'Error: "{file_path}" is not a Python file'

        command = ["python", llm_target_file]  

        if args is not None:
             command.extend(args)

        CompletedProcess = subprocess.run(command, cwd=llm_allowed_path, capture_output=True, timeout=30, text=True)

        if CompletedProcess.returncode != 0:
            output_holder.append(f'Process exited with code {CompletedProcess.returncode}')
        
        if CompletedProcess.stdout: 
            output_holder.append(f'STDOUT:\n{CompletedProcess.stdout}')
    
        if CompletedProcess.stderr:
            output_holder.append(f'STDERR:\n{CompletedProcess.stderr}')
        
        if not CompletedProcess.stderr and not CompletedProcess.stdout:
            output_holder.append(f'No output produced')

        return "\n".join(output_holder)

    except Exception as e:
            return f"Error: executing Python file: {e}"


    #Note for ref on setting up a sub-process
    #subprocess.run(args, *, stdin=None, input=None, stdout=None, stderr=None,
    # capture_output=False, shell=False, cwd=None, timeout=None, check=False,
    #  encoding=None, errors=None, text=None, env=None, universal_newlines=None, **other_popen_kwargs)

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Runs a specified Python file as a subprocess outside of the main proccess.  It Executes the function and returns the output",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path to the file relative to the working directory."
                },
                "args": {
                    "type": "array",
                    "description": "Optional arguments",
                    "items": {
                        "type": "string"
                    }
                }
            },
            "required": ["file_path"],
            "additionalProperties": False,
        },
    },
}    
    