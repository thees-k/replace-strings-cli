#!/usr/bin/python3
# replace_strings.py
"""
Replaces all occurrences of a regex pattern with a string in a text file.
"""
import sys
import re

def parse_args() -> tuple[str, str, str, bool]:
    args = sys.argv[1:]
    test_mode = "-t" in args
    if test_mode:
        args = [a for a in args if a != "-t"]

    if len(args) != 3:
        print(f"Usage: {sys.argv[0]} [-t] \"search pattern\" \"replacement string\" textfile")
        print("-> Put both strings in quotation marks!")
        print("-> The search pattern supports Python regex syntax.")
        print("-> Use -t to preview changes without modifying the file.")
        sys.exit(0)

    return args[0], args[1], args[2], test_mode


def main() -> None:
    pattern, replace, path, test_mode = parse_args()

    try:
        compiled = re.compile(pattern)
    except re.error as e:
        print(f"Error: Invalid regex pattern: {e}")
        sys.exit(1)

    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: File not found: {path}")
        sys.exit(1)
    except PermissionError:
        print(f"Error: Permission denied: {path}")
        sys.exit(1)

    if test_mode:
        matches_found = False
        for i, line in enumerate(lines, start=1):
            new_line = compiled.sub(replace, line)
            if new_line != line:
                matches_found = True
                print(f"Line {i}:")
                print(f"  - {line.rstrip()}")
                print(f"  + {new_line.rstrip()}")
        if not matches_found:
            print("No matches found.")
    else:
        new_lines = [compiled.sub(replace, line) for line in lines]
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.writelines(new_lines)
        except PermissionError:
            print(f"Error: Permission denied: {path}")
            sys.exit(1)


if __name__ == "__main__":
    main()
