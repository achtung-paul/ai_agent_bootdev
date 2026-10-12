from openai import OpenAI, APIError
import time

def call_lmm_with_retries(client, messages, available_functions, max_retries, retry_delay_seconds) -> list | None:   
    
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

            error = getattr(response, "error", None)
            if error:
                print(f"Error: {error}. Retrying ({attempt}/{max_retries})...")
                if attempt < max_retries:
                    time.sleep(retry_delay_seconds)
                    continue
                else:
                    return None

            if response.choices:
                return response
            

            else:
                print(f"Error: Something has gone wrong no choices found, retrying({attempt}/{max_retries})...")
                if attempt < max_retries:
                    time.sleep(retry_delay_seconds)
                    continue
                else:
                    return None

        except APIError as e:
            print(f"Error: LLM API request failed: {e}, Retrying ({attempt}/{max_retries})")
            if attempt < max_retries:
                time.sleep(retry_delay_seconds)
            else:
                return None
