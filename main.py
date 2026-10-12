import os, argparse, sys
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from functions.llm_call_functions import available_functions, call_function
from llm_call_loop import call_lmm_with_retries
from config import max_retries, retry_delay_seconds, max_calls

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")

def api_check():
    if api_key is None:
        raise ValueError("OPENROUTER_API_KEY is not set in the environment variables.")
    else:
        pass
      

def passed_input_msg():
    parser = argparse.ArgumentParser(description="Chatbot message input")
    parser.add_argument("user_prompt", type=str, help="User input prompt for LLM")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    return parser.parse_args()

def llm_response(client) -> None:

    content_arg = passed_input_msg()

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": content_arg.user_prompt}
        ]

    #print(json.dumps(available_functions, indent=2))
    completed_loop = False
    
    #limits the llm calls to prevent runaway
    for llm_calls in range(1, max_calls +1):

        
        response = call_lmm_with_retries(client, messages, available_functions, max_retries, retry_delay_seconds)
        message = response.choices[0].message
        messages.append(message)

    #message = response.choices[0].message

        if content_arg.verbose is True:
            #print(f"User Prompt: {input_message[0]['content']}")
            print(f"User prompt:{content_arg.user_prompt}")
            
            usage = response.usage
            
            if usage is None:
                raise RuntimeError("Error no Output from API")
                
            else:
                print(f"Prompt tokens:{usage.prompt_tokens}")
                print(f"Response tokens:{usage.completion_tokens}")
        
        if message.tool_calls is not None:
            for tool_call in message.tool_calls:    
                        #function_args = json.loads(tool_call.function.arguments or "{}")
                result_message = call_function(tool_call, content_arg.verbose)
                messages.append(result_message)

                if not result_message['content']: 
                    raise Exception("content message is empty")
                    
                if content_arg.verbose is True:
                    
                    print(f"-> {result_message['content']}")
                #print(f"Calling function: {tool_call.function.name}({function_args})")
        
        else:
            print(message.content)
            completed_loop = True
            break

    if not completed_loop:
        print(f"Error maximum number of calls ({max_calls}) reached so llm has not finished")       
        sys.exit(1)


def main():
    api_check()
    client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"
)
    llm_response(client)


if __name__ == "__main__":
    main()
