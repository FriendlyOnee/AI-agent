import os


def get_file_content(working_directory, file_path):
    try:
        abs_working = os.path.abspath(working_directory)
        abs_file = os.path.abspath(os.path.join(working_directory, file_path))

        if not os.path.commonpath([abs_file]).startswith(
            os.path.commonpath([abs_working])
        ):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(abs_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        MAX_CHARS = 10000

        with open(abs_file, "r") as f:
            content = f.read(MAX_CHARS)
            if f.read(1):
                return f'{content}\n[...File "{file_path}" truncated at {MAX_CHARS} characters]'

            return content

    except Exception as e:
        return f"Error: {str(e)}"

    return None
