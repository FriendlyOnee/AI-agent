import os
import subprocess
import sys


def run_python_file(working_directory, file_path):
    try:
        abs_working = os.path.abspath(working_directory)
        abs_file = os.path.abspath(os.path.join(working_directory, file_path))

        if not os.path.commonpath([abs_file]).startswith(
            os.path.commonpath([abs_working])
        ):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(abs_file):
            return f'Error: File "{file_path}" not found.'

        if not os.path.splitext(abs_file)[1] in {".py", ".pyw"}:
            return f'Error: "{file_path}" is not a Python file.'

        result = subprocess.run(
            [sys.executable, abs_file], capture_output=True, text=True, timeout=30
        )

        stdout = result.stdout.strip()
        stderr = result.stderr.strip()
        returncode = result.returncode

        output_lines = []

        if stdout:
            output_lines.append(f"STDOUT:\n{stdout}")

        if stderr:
            output_lines.append(f"STDERR:\n{stderr}")

        if returncode != 0:
            output_lines.append(f"Process exited with code {returncode}")

        if not output_lines:
            return "No output produced."

        return "\n\n".join(output_lines)

    except Exception as e:
        return f"Error: executing Python file: {e}"
