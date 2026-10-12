import os, json, argparse, time
from dotenv import load_dotenv
from openai import OpenAI, APIError
from prompts import system_prompt
from functions.llm_call_functions import available_functions

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
    max_retries = 3
    retry_delay_seconds = 3

    for attempt in range(1, max_retries + 1):
        try:
            response = client.chat.completions.create(
                #model="openrouter/free",
                #model="nvidia/nemotron-3-ultra-550b-a55b:free",
                model="deepseek/deepseek-v4.1-flash",
                messages=messages,
                temperature=0,
                tools=available_functions,
                )
        except APIError as e:
            print(f"Error: LLM API request failed: {e}")
            return

        if response.choices:
            break

        error = getattr(response, "error", None)
        if error and attempt < max_retries:
            print(f"Error: {error}. Retrying ({attempt}/{max_retries})...")
            time.sleep(retry_delay_seconds)
        else:
            break

    if not response.choices:
        print("DEBUG - full response:", response)

    else:

        message = response.choices[0].message

        if content_arg.verbose is True:
            #print(f"User Prompt: {input_message[0]['content']}")
            print(f"User prompt:{content_arg.user_prompt}")
        
            usage = response.usage
        
            if usage is None:
                raise RuntimeError("Error no Output from API")
            
            else:
                print(f"Prompt tokens:{usage.prompt_tokens}")
                print(f"Response tokens:{usage.completion_tokens}")
        
        if message.tool_calls:
            for tool_call in message.tool_calls:
                function_args = json.loads(tool_call.function.arguments or "{}")
                print(f"Calling function: {tool_call.function.name}({function_args})")
        
        else:
            
            print(message.content)



def main():
    api_check()
    client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"
)
    llm_response(client)


if __name__ == "__main__":
    main()
