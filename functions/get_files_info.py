import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    
    #get directory info to allow check of path to stop LLM escaping.
    llm_allowed_path = os.path.abspath(working_directory)
    #print(llm_allowed_path)
    llm_target_dir = os.path.normpath(os.path.join(llm_allowed_path, directory))
    valid_target_dir = os.path.commonpath([llm_allowed_path, llm_target_dir]) == llm_allowed_path

    
    try:
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(llm_target_dir):
            return f'Error: "{directory}" is not a directory'
        else:
            
            #dir_full_path = llm_allowed_path + "/" + directory
            #below is OS agnostic as windows uses \ not /
            dir_full_path = os.path.join(llm_allowed_path,directory)
            dir_list = os.listdir(path=dir_full_path)
            
            output_list= []
            for item in dir_list:
                item_path = os.path.join(dir_full_path, item)
                is_a_dir = os.path.isdir(item_path)
                file_size = os.path.getsize(item_path)
                output_list.append(f"    -{item}: file_size={file_size} bytes, is_dir={is_a_dir}")

            
            return '\n'.join(output_list)

    
    except Exception as e:
        return f"Error: {e}"

#JSON for the LLM 

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists the names of files and their attributes such as size and if it's a directory",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}    
    