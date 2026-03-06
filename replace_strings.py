#!/usr/bin/python3

# replace_strings.py

import sys

"""
Replaces all occurrences of a string with another string in a text file.
"""

if len(sys.argv) != 4:
    print(f"Usage: {sys.argv[0]} \"search string\" \"replacement string\" textfile")
    print("-> Put both strings in quotation marks!")
    sys.exit(0)

search  = sys.argv[1]
replace = sys.argv[2]
path    = sys.argv[3]

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(search, replace)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

