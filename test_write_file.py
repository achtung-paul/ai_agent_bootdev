from functions.write_file import write_file

def run_case(working_dir, file_path, content):
    result = write_file(working_dir, file_path, content)
    #print(f"{file_path}")

    if result.startswith("Error:"):
        print(result)
    
    else:
        print(f"{result}")


if __name__ == "__main__":
    cases = [
        ("lorem.txt", "wait, this isn't lorem ipsum"),
        ("pkg/morelorem.txt", "lorem ipsum dolor sit amet"),
        ("/tmp/temp.txt", "this should not be allowed"),
    ]
    
    for path_tuple, text_tuple in cases:
        run_case("calculator", path_tuple, text_tuple)

