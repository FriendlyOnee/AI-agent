from functions.write_file import write_file

tests = [
    (write_file, ("calculator", "lorem.txt", "wait, this isn't lorem ipsum")),
    (write_file, ("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")),
    (write_file, ("calculator", "/tmp/temp.txt", "this should not be allowed")),
]

for func, args in tests:
    print(f"Calling: {func.__name__}{args}")
    result = func(*args)
    print(f"Result: {result}\n")
