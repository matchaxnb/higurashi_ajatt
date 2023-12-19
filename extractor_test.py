#!/usr/bin/env python3
import unittest
from extractor import line_to_html_paragraph


class TestExtractor(unittest.TestCase):
    def test_test(self):
        self.assertEqual(line_to_html_paragraph(["a", "A"]), "<p>A</p>", "a")


if __name__ == "__main__":
    unittest.main()
