import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from av_functions import available_functions, function_implementations

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

verbose = "--verbose" in sys.argv

if verbose:
    sys.argv.remove("--verbose")

if len(sys.argv) < 2:
    raise Exception("Prompt wasn't provided")
user_prompt = sys.argv[1]

system_prompt = """
You are a helpful AI coding agent with these capabilities:
- List files/directories
- Read file contents
- Execute Python files
- Write/overwrite files

All paths should be relative to the working directory.
"""

workdir = "./calculator"
max_iterations = 20
iteration_count = 0


def call_function(
    function_call_part: types.FunctionCall, verbose: bool = False
) -> types.Content:
    """Executes a function call with automatic working directory injection."""
    function_name = function_call_part.name
    args = function_call_part.args.copy() if function_call_part.args else {}

    args["working_directory"] = workdir

    if verbose:
        print(f"Calling function: {function_name}({args})")
    else:
        print(f" - Calling function: {function_name}")

    try:
        function_to_call = function_implementations.get(function_name)
        if not function_to_call:
            raise ValueError(f"Unknown function: {function_name}")

        function_result = function_to_call(**args)

        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name, response={"result": function_result}
                )
            ],
        )
    except Exception as e:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name, response={"error": str(e)}
                )
            ],
        )


messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]

# [Previous imports and setup remain the same until the messages initialization]

messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]
max_iterations = 20
iteration_count = 0

while iteration_count < max_iterations:
    iteration_count += 1

    if verbose:
        print(f"\n=== Iteration {iteration_count} ===")

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt,
        ),
    )

    if hasattr(response, "candidates"):
        for candidate in response.candidates:
            if hasattr(candidate, "content"):
                messages.append(candidate.content)

    if response.text:
        print(response.text)

    function_called = False
    if hasattr(response, "function_calls") and response.function_calls:
        for function_call in response.function_calls:
            function_result = call_function(function_call, verbose)

            if not (hasattr(function_result, "parts") and function_result.parts):
                raise RuntimeError("Malformed function response")

            if verbose:
                print(f"-> {function_result.parts[0].function_response.response}")

            messages.append(function_result)
            function_called = True

    if verbose and hasattr(response, "usage_metadata"):
        print(f"\nToken usage:")
        print(f"- Prompt: {response.usage_metadata.prompt_token_count}")
        print(f"- Response: {response.usage_metadata.candidates_token_count}")

    if not function_called:
        if verbose:
            print("\nNo more function calls needed, exiting loop")
        break

if iteration_count >= max_iterations and verbose:
    print("\nReached maximum iteration limit (20)")
