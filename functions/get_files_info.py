import os


def get_files_info(working_directory, directory=None):
    if directory is None:
        directory = working_directory
    else:
        directory = os.path.join(working_directory, directory)

    try:
        abs_working = os.path.abspath(working_directory)
        abs_directory = os.path.abspath(directory)

        common_path = os.path.commonpath([abs_working, abs_directory])
        if common_path != os.path.commonpath([abs_working]):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(abs_directory):
            return f'Error: "{directory}" is not a directory'

        output = []
        for entry in sorted(os.listdir(abs_directory)):
            entry_path = os.path.join(abs_directory, entry)
            try:
                is_dir = os.path.isdir(entry_path)
                size = os.path.getsize(entry_path) if not is_dir else 0
                output.append(f"{entry}: file_size={size} bytes, is_dir={is_dir}")
            except Exception as e:
                output.append(f"{entry}: [Error: {str(e)}]")

        return "\n".join(output) if output else "Directory is empty"

    except Exception as e:
        return f"Error: {str(e)}"
