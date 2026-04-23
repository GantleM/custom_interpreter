import sys
from my import My

if __name__ == "__main__":
    file_name = sys.argv[1]
    with open(file_name) as f:
        code = f.read()
    running = My(code)
