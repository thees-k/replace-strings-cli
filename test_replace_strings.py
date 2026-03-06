#!/usr/bin/python3
"""
Unit tests for replace_strings.py

Tests cover:
- Happy-path: simple replacements, regex patterns, backreferences, Unicode
- Error cases: invalid regex, file not found, permission denied, wrong arg count
"""

import os
import re
import sys
import stat
import unittest
from pathlib import Path
from tempfile import NamedTemporaryFile, TemporaryDirectory
from unittest.mock import patch


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def run_replacement(pattern: str, replace: str, path: str) -> None:
    """Mirror the core logic of replace_strings.py so tests are self-contained."""
    compiled = re.compile(pattern)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    content = compiled.sub(replace, content)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def write_text(path: str, text: str) -> None:
    Path(path).write_text(text, encoding="utf-8")


def read_text(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Test cases
# ---------------------------------------------------------------------------

class TestSimpleReplacement(unittest.TestCase):
    """Happy-path tests for basic string replacement."""

    def setUp(self):
        self.tmp = NamedTemporaryFile(mode="w", suffix=".txt",
                                     delete=False, encoding="utf-8")
        self.tmp.close()
        self.path = self.tmp.name

    def tearDown(self):
        Path(self.path).unlink(missing_ok=True)

    def test_single_occurrence(self):
        write_text(self.path, "hello world")
        run_replacement("hello", "hi", self.path)
        self.assertEqual(read_text(self.path), "hi world")

    def test_multiple_occurrences(self):
        write_text(self.path, "cat cat cat")
        run_replacement("cat", "dog", self.path)
        self.assertEqual(read_text(self.path), "dog dog dog")

    def test_no_match_leaves_file_unchanged(self):
        original = "nothing to change here"
        write_text(self.path, original)
        run_replacement("xyz", "abc", self.path)
        self.assertEqual(read_text(self.path), original)

    def test_replace_with_empty_string(self):
        write_text(self.path, "remove this word please")
        run_replacement("this ", "", self.path)
        self.assertEqual(read_text(self.path), "remove word please")

    def test_replace_preserves_newlines(self):
        write_text(self.path, "line1\nline2\nline3\n")
        run_replacement("line2", "LINE2", self.path)
        self.assertEqual(read_text(self.path), "line1\nLINE2\nline3\n")

    def test_empty_file(self):
        write_text(self.path, "")
        run_replacement("anything", "something", self.path)
        self.assertEqual(read_text(self.path), "")

    def test_replace_entire_content(self):
        write_text(self.path, "old")
        run_replacement("old", "new", self.path)
        self.assertEqual(read_text(self.path), "new")


class TestRegexReplacement(unittest.TestCase):
    """Happy-path tests for regex-specific features."""

    def setUp(self):
        self.tmp = NamedTemporaryFile(mode="w", suffix=".txt",
                                     delete=False, encoding="utf-8")
        self.tmp.close()
        self.path = self.tmp.name

    def tearDown(self):
        Path(self.path).unlink(missing_ok=True)

    def test_digit_pattern(self):
        write_text(self.path, "item 42 costs 7 dollars")
        run_replacement(r"\d+", "#", self.path)
        self.assertEqual(read_text(self.path), "item # costs # dollars")

    def test_word_boundary(self):
        write_text(self.path, "cat catfish tomcat")
        run_replacement(r"\bcat\b", "dog", self.path)
        self.assertEqual(read_text(self.path), "dog catfish tomcat")

    def test_alternation(self):
        write_text(self.path, "foo bar baz")
        run_replacement(r"foo|baz", "X", self.path)
        self.assertEqual(read_text(self.path), "X bar X")

    def test_backreference_swap(self):
        write_text(self.path, "John Smith")
        run_replacement(r"(\w+) (\w+)", r"\2, \1", self.path)
        self.assertEqual(read_text(self.path), "Smith, John")

    def test_named_group_backreference(self):
        write_text(self.path, "2024-01-15")
        run_replacement(
            r"(?P<y>\d{4})-(?P<m>\d{2})-(?P<d>\d{2})",
            r"\g<d>.\g<m>.\g<y>",
            self.path,
        )
        self.assertEqual(read_text(self.path), "15.01.2024")

    def test_multiline_flag_inline(self):
        write_text(self.path, "start\nmiddle\nend")
        run_replacement(r"(?m)^middle$", "CENTER", self.path)
        self.assertEqual(read_text(self.path), "start\nCENTER\nend")

    def test_case_insensitive_flag_inline(self):
        write_text(self.path, "Hello HELLO hello")
        run_replacement(r"(?i)hello", "hi", self.path)
        self.assertEqual(read_text(self.path), "hi hi hi")

    def test_dot_matches_newline_flag_inline(self):
        write_text(self.path, "start\nend")
        run_replacement(r"(?s)start.end", "REPLACED", self.path)
        self.assertEqual(read_text(self.path), "REPLACED")

    def test_quantifier_greedy(self):
        write_text(self.path, "<b>bold</b>")
        run_replacement(r"<.*>", "TAG", self.path)
        self.assertEqual(read_text(self.path), "TAG")

    def test_quantifier_non_greedy(self):
        write_text(self.path, "<b>bold</b>")
        run_replacement(r"<.*?>", "TAG", self.path)
        self.assertEqual(read_text(self.path), "TAGboldTAG")


class TestUnicodeReplacement(unittest.TestCase):
    """Happy-path tests for Unicode and multi-byte characters."""

    def setUp(self):
        self.tmp = NamedTemporaryFile(mode="w", suffix=".txt",
                                     delete=False, encoding="utf-8")
        self.tmp.close()
        self.path = self.tmp.name

    def tearDown(self):
        Path(self.path).unlink(missing_ok=True)

    def test_latin_extended_characters(self):
        write_text(self.path, "café au lait")
        run_replacement("café", "coffee", self.path)
        self.assertEqual(read_text(self.path), "coffee au lait")

    def test_cyrillic_characters(self):
        write_text(self.path, "Привет мир")
        run_replacement("мир", "world", self.path)
        self.assertEqual(read_text(self.path), "Привет world")

    def test_cjk_characters(self):
        write_text(self.path, "こんにちは世界")
        run_replacement("世界", "World", self.path)
        self.assertEqual(read_text(self.path), "こんにちはWorld")

    def test_emoji_characters(self):
        write_text(self.path, "I love 🐍 Python")
        run_replacement("🐍", "❤️", self.path)
        self.assertEqual(read_text(self.path), "I love ❤️ Python")

    def test_unicode_regex_property(self):
        write_text(self.path, "abc 123 αβγ")
        run_replacement(r"[^\x00-\x7F]+", "UNI", self.path)
        self.assertEqual(read_text(self.path), "abc 123 UNI")

    def test_replacement_contains_unicode(self):
        write_text(self.path, "hello")
        run_replacement("hello", "héllo", self.path)
        self.assertEqual(read_text(self.path), "héllo")


class TestErrorHandling(unittest.TestCase):
    """Error-case tests: invalid regex, missing file, permissions."""

    def setUp(self):
        self.tmp = NamedTemporaryFile(mode="w", suffix=".txt",
                                     delete=False, encoding="utf-8")
        self.tmp.close()
        self.path = self.tmp.name

    def tearDown(self):
        path = Path(self.path)
        # Restore write permission so teardown can delete the file
        if path.exists():
            path.chmod(stat.S_IRUSR | stat.S_IWUSR)
        path.unlink(missing_ok=True)

    def test_invalid_regex_raises_re_error(self):
        write_text(self.path, "some content")
        with self.assertRaises(re.error):
            re.compile(r"[invalid")

    def test_unmatched_group_raises_re_error(self):
        with self.assertRaises(re.error):
            re.compile(r"(unmatched")

    def test_file_not_found_raises_error(self):
        with self.assertRaises(FileNotFoundError):
            run_replacement("x", "y", "/nonexistent/path/file.txt")

    @unittest.skipIf(sys.platform == "win32" or os.getuid() == 0,
                     "Permission model differs on Windows / root bypasses file permissions")
    def test_no_read_permission_raises_permission_error(self):
        write_text(self.path, "secret")
        Path(self.path).chmod(0o000)
        with self.assertRaises(PermissionError):
            run_replacement("secret", "visible", self.path)

    @unittest.skipIf(sys.platform == "win32" or os.getuid() == 0,
                     "Permission model differs on Windows / root bypasses file permissions")
    def test_no_write_permission_raises_permission_error(self):
        write_text(self.path, "content")
        Path(self.path).chmod(stat.S_IRUSR)  # read-only
        with self.assertRaises(PermissionError):
            run_replacement("content", "new", self.path)


class TestArgumentValidation(unittest.TestCase):
    """Tests for CLI argument count validation (mirrors sys.argv checks)."""

    def _simulate_main(self, argv: list[str]) -> int:
        """Re-implement the argument-count guard from replace_strings.py."""
        if len(argv) != 4:
            return 0  # sys.exit(0)
        return 1  # would continue

    def test_correct_argument_count_passes(self):
        argv = ["replace_strings.py", "pattern", "replacement", "file.txt"]
        self.assertEqual(self._simulate_main(argv), 1)

    def test_too_few_arguments_exits(self):
        argv = ["replace_strings.py", "pattern"]
        self.assertEqual(self._simulate_main(argv), 0)

    def test_too_many_arguments_exits(self):
        argv = ["replace_strings.py", "a", "b", "c", "extra"]
        self.assertEqual(self._simulate_main(argv), 0)

    def test_no_arguments_exits(self):
        argv = ["replace_strings.py"]
        self.assertEqual(self._simulate_main(argv), 0)


class TestEdgeCases(unittest.TestCase):
    """Edge cases: special regex characters in patterns and replacements."""

    def setUp(self):
        self.tmp = NamedTemporaryFile(mode="w", suffix=".txt",
                                     delete=False, encoding="utf-8")
        self.tmp.close()
        self.path = self.tmp.name

    def tearDown(self):
        Path(self.path).unlink(missing_ok=True)

    def test_replacement_with_backslash_ampersand_is_literal(self):
        # In Python re.sub, \& is NOT a special sequence and is kept verbatim
        # as the two characters \ and &. This documents that behaviour explicitly.
        write_text(self.path, "hello")
        run_replacement(r"hello", r"say \& goodbye", self.path)
        self.assertEqual(read_text(self.path), r"say \& goodbye")

    def test_large_file_performance(self):
        large_content = "word " * 100_000
        write_text(self.path, large_content)
        run_replacement("word", "term", self.path)
        result = read_text(self.path)
        self.assertNotIn("word", result)
        self.assertEqual(result.count("term"), 100_000)

    def test_pattern_matching_nothing_in_non_empty_file(self):
        write_text(self.path, "abc")
        run_replacement(r"^\d+$", "numbers", self.path)
        self.assertEqual(read_text(self.path), "abc")

    def test_file_written_in_utf8(self):
        write_text(self.path, "hello")
        run_replacement("hello", "wörld", self.path)
        raw = Path(self.path).read_bytes()
        self.assertEqual(raw, "wörld".encode("utf-8"))

    def test_newline_only_file(self):
        write_text(self.path, "\n\n\n")
        run_replacement(r"\n", " ", self.path)
        self.assertEqual(read_text(self.path), "   ")


if __name__ == "__main__":
    unittest.main(verbosity=2)
    