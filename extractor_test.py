#!/usr/bin/env python3
import unittest
import extractor


class TestExtractor(unittest.TestCase):
    def test_test(self):
        self.assertEqual(extractor.line_to_html_paragraph(
            ["a", "A"]), "<p>A</p>", "a")

    def test_extra_section_condition_extracted(self):
        re = extractor.EXTRA_SECTION_CONDITION_RE.search(
            'if(GetGlobalFlag(GCensor) < 10){ModCallScriptSection("zonik_004_vm0x_n01","dialog005");}'
        )
        self.assertEqual(re.group(1), "<")
        self.assertEqual(re.group(3), "10")

        re = extractor.EXTRA_SECTION_CONDITION_RE.search(
            'if(GetGlobalFlag(GCensor)     ==    0){ModCallScriptSection("zonik_004_vm0x_n01","dialog005");}'
        )
        self.assertEqual(re.group(1), "==")
        self.assertEqual(re.group(3), "0")

        re = extractor.EXTRA_SECTION_CONDITION_RE.search(
            'if(GetGlobalFlag(GCensor) >= 2){ModCallScriptSection("zonik_004_vm0x_n01","dialog005");}'
        )
        self.assertEqual(re.group(1), ">=")
        self.assertEqual(re.group(3), "2")

    def test_extra_section_goto_extracted(self):
        re = extractor.SUBSCRIPT_RE.search(
            '{ModCallScriptSection("zonik_004_vm0x_n01","dialog005");}'
        )
        self.assertEqual(re.group(1), "zonik_004_vm0x_n01")
        self.assertEqual(re.group(2), "dialog005")

        re = extractor.SUBSCRIPT_RE.search(
            '{ModCallScriptSection("zozozozo_007_vm1x_n01","dialog999");}'
        )
        self.assertEqual(re.group(1), "zozozozo_007_vm1x_n01")
        self.assertEqual(re.group(2), "dialog999")

    def test_extra_section_goto_matches(self):
        re = extractor.SUBSCRIPT_RE.search(
            '{ModCallScriptSection("zonik_004_vm0x_n01","dialog005");}'
        )
        self.assertIsNotNone(re)

        re = extractor.SUBSCRIPT_RE.search("if(GetGlobalFlag(GCensor) == 0)")
        self.assertIsNone(re)

    def test_extra_section_condition_matches(self):
        re = extractor.EXTRA_SECTION_CONDITION_RE.search(
            'if(GetGlobalFlag(GCensor) >= 3){ModCallScriptSection("zonik_004_vm0x_n01","dialog005");}'
        )
        self.assertIsNotNone(re)

        re = extractor.EXTRA_SECTION_CONDITION_RE.search(
            'if(GetGlobalFlag(GCensor) <=  3){ModCallScriptSection("zonik_004_vm0x_n01","dialog005");}'
        )
        self.assertIsNotNone(re)

        re = extractor.EXTRA_SECTION_CONDITION_RE.search(
            'if(GetGlobalFlag(GCensor) == 3){ModCallScriptSection("zonik_004_vm0x_n01","dialog005");}'
        )
        self.assertIsNotNone(re)

        re = extractor.EXTRA_SECTION_CONDITION_RE.search(
            'if(GetGlobalFlag(GCensor) > 3){ModCallScriptSection("zonik_004_vm0x_n01","dialog005");}'
        )
        self.assertIsNotNone(re)

        re = extractor.EXTRA_SECTION_CONDITION_RE.search(
            'if(GetGlobalFlag(GCensor) < 3){ModCallScriptSection("zonik_004_vm0x_n01","dialog005");}'
        )
        self.assertIsNotNone(re)

        re = extractor.EXTRA_SECTION_CONDITION_RE.search(
            'if(GetGlobalFlag(GCensor) = 3){ModCallScriptSection("zonik_004_vm0x_n01","dialog005");}'
        )
        self.assertIsNone(re)

        re = extractor.EXTRA_SECTION_CONDITION_RE.search(
            'if(GetGlobalFlag(GCensor) * 3){ModCallScriptSection("zonik_004_vm0x_n01","dialog005");}'
        )
        self.assertIsNone(re)


if __name__ == "__main__":
    unittest.main()
