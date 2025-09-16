import requests
import json
import time
import os
from dotenv import load_dotenv

load_dotenv()

def generate_llm_content(topic, format_req, constraints, persona=None):
    """
    Constructs an effective prompt from multiple parameters and sends it to the LLM.

    Args:
        topic (str): The main topic or subject for the LLM.
        format_req (str): The desired format for the output (e.g., 'a short blog post', 'a bulleted list').
        constraints (str): Additional details or constraints (e.g., 'use simple language', 'no more than 200 words').
        persona (str, optional): An optional persona to guide the model's behavior.

    Returns:
        str: The generated text content from the LLM, or an error message if the
             request fails.
    """
    # Load the API key from an environment variable for security
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "Error: GEMINI_API_KEY environment variable not set. Please set it before running the script."

    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={api_key}"

    # Construct the effective prompt from the given parameters
    effective_prompt = f"Topic: {topic}\nFormat: {format_req}\n"
    if constraints:
        effective_prompt += f"Constraints: {constraints}\n\n"
    effective_prompt += f"Please generate content based on the above information. With strict adherence to the format and constraints. without addition of the prefix suffix things like 'As an AI language model' or 'Here is the content you requested'. And dont add the Misinformation detection part if not asked specifically.\n\n"

    # Construct the payload for the API request
    payload = {
        "contents": [{"parts": [{"text": effective_prompt}]}],
    }

    # Add the optional persona as a system instruction if it's provided
    if persona:
        payload["systemInstruction"] = {"parts": [{"text": persona}]}

    headers = {'Content-Type': 'application/json'}

    try:
        # Send a POST request to the API with the JSON payload
        response = requests.post(api_url, data=json.dumps(payload), headers=headers)
        
        # Raise an exception for bad status codes (4xx or 5xx)
        response.raise_for_status()

        # Parse the JSON response
        result = response.json()
        
        # Extract the generated text from the nested JSON structure
        candidate = result.get('candidates', [])[0]
        text = candidate.get('content', {}).get('parts', [])[0].get('text', '')

        return text
    
    except requests.exceptions.RequestException as e:
        return f"An error occurred with the API request: {e}"
    except (IndexError, KeyError) as e:
        return f"Could not parse the API response. Error: {e}. Response text: {response.text}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"


if __name__ == "__main__":
    print("Welcome to the LLM Prompt Generator!")
    print("Let's build an effective prompt by gathering some details.\n")
    time.sleep(1)

    # Gather parameters from the user
    persona_input = input("1. Persona (e.g., 'Act as a professional copywriter'): ")
    topic_input = input("2. Topic/Main Subject (e.g., 'the benefits of gardening'): ")
    format_input = input("3. Format (e.g., 'a short blog post', 'a bulleted list'): ")
    constraints_input = input("4. Additional details/constraints (e.g., 'use simple language'): ")
    
    print("\nDrafting an effective prompt based on your input...\n")
    time.sleep(1)

    # Call the updated function with all the collected parameters
    generated_text = generate_llm_content(
        topic=topic_input,
        format_req=format_input,
        constraints=constraints_input,
        persona=persona_input
    )
    
    print("-" * 50)
    print("Generated Content:")
    print(generated_text)
    print("-" * 50)
