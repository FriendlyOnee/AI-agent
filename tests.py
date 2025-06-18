from functions.run_python_file import run_python_file

tests = [
    (run_python_file, ("calculator", "main.py")),
    (run_python_file, ("calculator", "tests.py")),
    (run_python_file, ("calculator", "../main.py")),
    (run_python_file, ("calculator", "nonexistent.py")),
]

for func, args in tests:
    print(f"Calling: {func.__name__}{args}")
    result = func(*args)
    print(f"Result: {result}\n")
