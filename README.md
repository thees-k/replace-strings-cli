# replace_strings.py

A simple command-line tool to perform regex-based string replacements in text files.

I needed it for programming.

Mainly written by **Claude Sonnet 4.6**.

## Features

- Use Python regular expressions to search and replace text.
- Supports a test mode (`-t` flag) to preview changes line-by-line without modifying the file.
- Handles common file errors gracefully (file not found, permission denied).

## Usage

```bash
python replace_strings.py [-t] "search pattern" "replacement string" textfile
```

- `-t` (optional): Preview changes without modifying the file.
- `"search pattern"`: A Python regex pattern to search for.
- `"replacement string"`: The string to replace matches with.
- `textfile`: Path to the text file to modify.

### Examples

#### Simple replacement without using regex

```bash
replace_strings.py "Hello" "Hi" mytext.txt
```

#### Preview changes without modifying the file

```bash
replace_strings.py -t "Hello" "Hi" mytext.txt
```

#### Replace one or more digits with "#"

```bash
replace_strings.py "\d+" "#" mytext.txt
```

#### Remove all lines that contain only whitespace

```bash
replace_strings.py "(?m)^\s+$" "" mytext.txt
```

→ For more examples see [test_replace_strings.py](test_replace_strings.py).

## Installation

No installation required. Requires Python 3.7+.

## Testing

The project includes a helper function in `test_replace_strings.py` to mirror the core replacement logic for testing purposes.

## Error Handling

- Invalid regex patterns will print an error and exit.
- File not found or permission errors will print an error and exit.

## License

[MIT License](LICENSE)
