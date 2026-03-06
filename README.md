# replace_strings.py

A simple command-line tool to perform regex-based string replacements in text files.

I needed it for programming.

Mainly implemented by **Claude Sonnet 4.6**.

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

Many examples can be found in [test_replace_strings.py](test_replace_strings.py).

#### Simple replacement without using regex

```bash
replace_strings.py "Hello" "Hi" mytext.txt
```
Note that "hello" would not be replaced. The script works **case sensitive**.

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

#### Swap first two words of each line and add comma

e.g. "John Smith" → "Smith, John"

```bash
replace_strings.py "(\w+) (\w+)" "\2, \1" mytext.txt
```

#### Reformat ISO dates

e.g. "2026-03-06" → "06.03.2026".

```bash
replace_strings.py "(?P<y>\d{4})-(?P<m>\d{2})-(?P<d>\d{2})" "\g<d>.\g<m>.\g<y>" mytext.txt
```

## Installation

No installation required. Requires Python 3.7+.

## Testing

The project includes a helper function in `test_replace_strings.py` to mirror the core replacement logic for testing purposes.

## Error Handling

- Invalid regex patterns will print an error and exit.
- File not found or permission errors will print an error and exit.

## License

[MIT License](LICENSE)
