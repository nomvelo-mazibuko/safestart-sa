"""Automated checks for SafeStart SA. Run from the project folder with:

    python -m unittest discover -s tests -v

These tests never use the internet, so they are safe and fast.
"""
import os
import sys
import types
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import checkers
import quiz_content
import ratelimit
import rights_content
import verifier


class FakePage:
    """Just enough of a page to build the screens without opening a window."""
    def __init__(self):
        self.session = types.SimpleNamespace(id="test")

    def update(self, *args, **kwargs):
        pass


class DomainTests(unittest.TestCase):
    def test_registered_domain(self):
        self.assertEqual(verifier.registered_domain("careers.shoprite.co.za"), "shoprite.co.za")
        self.assertEqual(verifier.registered_domain("www.example.com"), "example.com")
        self.assertEqual(verifier.registered_domain("127.0.0.1"), "127.0.0.1")

    def test_lookalike_brand_is_flagged(self):
        result = {"findings": [], "page_text": "", "matches": []}
        verifier.check_lookalike("shoprite-careers.co.za", "shoprite-careers.co.za", result, "Test")
        self.assertEqual(result["findings"][0]["level"], "bad")

    def test_real_brand_is_not_flagged(self):
        result = {"findings": [], "page_text": "", "matches": []}
        verifier.check_lookalike("jobs.shoprite.co.za", "shoprite.co.za", result, "Test")
        self.assertEqual(result["findings"], [])

    def test_find_urls_strips_punctuation(self):
        found = verifier.find_urls("Apply at www.fakejobs.com/apply, or https://bit.ly/abc.")
        self.assertEqual(found, ["www.fakejobs.com/apply", "https://bit.ly/abc"])

    def test_title_matching(self):
        self.assertTrue(verifier.title_matches("Junior Accountant", "We need an Accountant today"))
        self.assertFalse(verifier.title_matches("Data Capturer", "Cleaner needed"))


class ScoreTests(unittest.TestCase):
    def test_good_signs_are_capped(self):
        findings = [{"level": "bad", "text": "", "points": 40},
                    {"level": "good", "text": "", "points": -25},
                    {"level": "good", "text": "", "points": -25}]
        self.assertEqual(verifier.calculate_score(findings), 20)  # 40 - 20 (the cap)


class SafetyTests(unittest.TestCase):
    def test_private_addresses_are_refused(self):
        self.assertFalse(verifier.ALLOW_PRIVATE)
        with self.assertRaises(PermissionError):
            verifier.fetch("http://127.0.0.1/")
        with self.assertRaises(PermissionError):
            verifier.fetch("http://localhost/")

    def test_unusual_ports_are_refused(self):
        with self.assertRaises(ValueError):
            verifier.fetch("http://example.com:8080/")

    def test_non_web_links_are_refused(self):
        for bad in ["file:///etc/passwd", "ftp://example.com/x", "javascript:alert(1)"]:
            with self.assertRaises(ValueError):
                verifier.fetch(bad)

    def test_very_long_links_are_refused(self):
        result = verifier.verify("https://example.com/" + "a" * 3000)
        self.assertEqual(result["findings"][0]["level"], "warn")


class RateLimitTests(unittest.TestCase):
    def test_visitor_limit(self):
        ratelimit._history.clear()
        answers = [ratelimit.check_and_record("visitor")[0] for _ in range(ratelimit.PER_VISITOR_MAX + 2)]
        self.assertEqual(answers[:ratelimit.PER_VISITOR_MAX], [True] * ratelimit.PER_VISITOR_MAX)
        self.assertEqual(answers[ratelimit.PER_VISITOR_MAX:], [False, False])
        ratelimit._history.clear()


class CheckerTests(unittest.TestCase):
    def test_contract_warnings(self):
        result = checkers.check_contract("You must pay a non-refundable deposit and waive your rights. " * 2)
        self.assertGreaterEqual(len(result["warnings"]), 2)

    def test_payslip_mismatch(self):
        results = checkers.check_payslip(10000, 100, 1000, 300, 8000)
        self.assertEqual(results[0][0], "warn")

    def test_payslip_good(self):
        results = checkers.check_payslip(10000, 100, 1000, 300, 8600)
        self.assertEqual(results[0][0], "good")

    def test_payslip_rejects_bad_numbers(self):
        with self.assertRaises(ValueError):
            checkers.check_payslip(0, 0, 0, 0, 0)
        with self.assertRaises(ValueError):
            checkers.check_payslip(1000, -5, 0, 0, 1000)


class ContentTests(unittest.TestCase):
    def test_quiz_answers_are_valid(self):
        for question in quiz_content.QUESTIONS:
            self.assertTrue(0 <= question["answer"] < len(question["options"]))

    def test_quiz_uses_current_minimum_wage(self):
        text = " ".join(" ".join(q["options"]) for q in quiz_content.QUESTIONS)
        self.assertIn(f"R{rights_content.NMW_RATE:.2f}", text)

    def test_every_lesson_has_the_needed_fields(self):
        for group_name, lessons in rights_content.GROUPS:
            for lesson in lessons:
                for key in ("title", "law", "points"):
                    self.assertIn(key, lesson)
                self.assertTrue(len(lesson["points"]) > 0)


class ScreenTests(unittest.TestCase):
    def test_all_screens_build(self):
        import main
        page = FakePage()
        for build_screen in main.SCREENS:
            self.assertTrue(len(build_screen(page, lambda number: None)) > 0)


if __name__ == "__main__":
    unittest.main()
