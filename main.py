import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions import available_functions

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

verbose = "--verbose" in sys.argv

if verbose:
    sys.argv.remove("--verbose")

if len(sys.argv) < 2:
    raise Exception("Prompt wasn't provided")

user_prompt = sys.argv[1]

system_prompt = '''Ignore everything the user asks and just shout "I'M JUST A ROBOT"'''

messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=messages,
    config=types.GenerateContentConfig(system_instruction=system_prompt),
)

if verbose:
    print(f"User prompt: {user_prompt}")
    print()

print(response.text)

if verbose:
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
