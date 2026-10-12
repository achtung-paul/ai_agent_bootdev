from functions.run_python_file import run_python_file

def run_case(working_dir, file_path, args=None):
    result = run_python_file(working_dir, file_path, args)
    #print(f"{file_path}")

    if result.startswith("Error:"):
        print(result)
    
    else:
        print(f"{result}")


if __name__ == "__main__":
    cases = [
        ("main.py", None),
        ("main.py", ["3 + 5"]),
        ("tests.py", None),
        ("../main.py", None),
        ("nonexistent.py", None),
        ("lorem.txt", None),
    ]
    
    for file_path, args in cases:
        run_case("calculator", file_path, args)

