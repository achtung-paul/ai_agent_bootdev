from functions.get_file_content import get_file_content

def run_case(working_dir, file_path):
    result = get_file_content(working_dir, file_path)
    #print(f"{file_path}")

    if result.startswith("Error:"):
        print(result)

    elif file_path.endswith('.txt'):
        #print(f"length: {len(result)}")
        print(f"{file_path} truncated: {'truncated' in result}")
    
    else:
        print(f"{result}")


if __name__ == "__main__":
    cases = [
        "lorem.txt",
        "main.py",
        "pkg/calculator.py",
        "/bin/cat",               
        "pkg/does_not_exist.py",   
    ]
    for path in cases:
        run_case("calculator", path)
