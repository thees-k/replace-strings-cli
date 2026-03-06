#!/usr/bin/python3
# replace_strings.py
"""
Replaces all occurrences of a regex pattern with a string in a text file.

Examples:

# Replace one or more digits with #
replace_strings.py "\d+" "#" mytext.txt

# Swap first and last name (e.g. "John Smith" → "Smith, John")
replace_strings.py "(\w+) (\w+)" "\2, \1" mytext.txt

# Remove lines that contain only whitespace (multiline not needed for this)
replace_strings.py "(?m)^\s+$" "" mytext.txt
"""
import sys
import re

if len(sys.argv) != 4:
    print(f"Usage: {sys.argv[0]} \"search pattern\" \"replacement string\" textfile")
    print("-> Put both strings in quotation marks!")
    print("-> The search pattern supports Python regex syntax.")
    sys.exit(0)

pattern = sys.argv[1]
replace = sys.argv[2]
path    = sys.argv[3]

try:
    compiled = re.compile(pattern)
except re.error as e:
    print(f"Error: Invalid regex pattern: {e}")
    sys.exit(1)

try:
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
except FileNotFoundError:
    print(f"Error: File not found: {path}")
    sys.exit(1)
except PermissionError:
    print(f"Error: Permission denied: {path}")
    sys.exit(1)

content = compiled.sub(replace, content)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)