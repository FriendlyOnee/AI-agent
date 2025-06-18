import os


def write_file(working_directory, file_path, content):
    try:
        abs_working = os.path.abspath(working_directory)
        abs_file = os.path.abspath(os.path.join(working_directory, file_path))

        if not os.path.commonpath([abs_file]).startswith(
            os.path.commonpath([abs_working])
        ):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        with open(abs_file, "w") as f:
            f.write(content)

        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )

    except Exception as e:
        return f"Error: {str(e)}"
