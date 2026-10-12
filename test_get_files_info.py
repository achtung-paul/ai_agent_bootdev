from functions.get_files_info import get_files_info

#run test on the diretory the LLM will be working inside and make sure it can't escape

if __name__ == "__main__":

    result1 = get_files_info("calculator", ".")
    result2 = get_files_info("calculator", "pkg")
    result3 = get_files_info("calculator", "/bin")
    result4 = get_files_info("calculator", "../")

    print(f"Result for current directory: \n {result1}")
    print(f"Result for 'pkg' directory: \n {result2}")
    print(f"Result for '/bin' directory: \n {result3}")
    print(f"Result for '../' directory: \n {result4}")