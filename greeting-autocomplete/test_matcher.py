"""Unit tests for the greeting matcher."""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

import pytest
from greetings import GREETINGS, DEFAULT_RESPONSE
from matcher import match_greeting


class TestDataIntegrity:
    """Tests for the integrity of the greetings dictionary."""

    def test_greetings_dict_not_empty(self):
        assert len(GREETINGS) > 0, "GREETINGS dictionary must not be empty"

    def test_all_keys_are_lowercase(self):
        for key in GREETINGS:
            assert key == key.lower(), f"Key '{key}' is not lowercase"

    def test_all_keys_are_stripped(self):
        for key in GREETINGS:
            assert key == key.strip(), f"Key '{key}' has leading/trailing whitespace"

    def test_all_responses_are_non_empty_strings(self):
        for key, value in GREETINGS.items():
            assert isinstance(value, str), f"Response for '{key}' is not a string"
            assert value.strip(), f"Response for '{key}' is empty"

    def test_default_response_is_non_empty_string(self):
        assert isinstance(DEFAULT_RESPONSE, str)
        assert DEFAULT_RESPONSE.strip()


class TestExactMatches:
    """Tests for exact matching behavior."""

    def test_exact_hello(self):
        assert match_greeting("hello") == GREETINGS["hello"]

    def test_exact_hi(self):
        assert match_greeting("hi") == GREETINGS["hi"]

    def test_exact_good_morning(self):
        assert match_greeting("good morning") == GREETINGS["good morning"]

    def test_exact_how_are_you(self):
        assert match_greeting("how are you") == GREETINGS["how are you"]

    def test_exact_greetings(self):
        assert match_greeting("greetings") == GREETINGS["greetings"]

    def test_exact_good_night(self):
        assert match_greeting("good night") == GREETINGS["good night"]


class TestCaseInsensitive:
    """Tests for case-insensitive matching."""

    def test_uppercase_hello(self):
        assert match_greeting("HELLO") == GREETINGS["hello"]

    def test_mixed_case_hi(self):
        assert match_greeting("Hi") == GREETINGS["hi"]

    def test_mixed_case_good_morning(self):
        assert match_greeting("Good Morning") == GREETINGS["good morning"]

    def test_all_caps_how_are_you(self):
        assert match_greeting("HOW ARE YOU") == GREETINGS["how are you"]

    def test_mixed_case_hey(self):
        assert match_greeting("HEY") == GREETINGS["hey"]


class TestWhitespaceNormalization:
    """Tests for whitespace stripping."""

    def test_leading_whitespace(self):
        assert match_greeting("  hello") == GREETINGS["hello"]

    def test_trailing_whitespace(self):
        assert match_greeting("hello  ") == GREETINGS["hello"]

    def test_leading_and_trailing_whitespace(self):
        assert match_greeting("  good morning  ") == GREETINGS["good morning"]


class TestFuzzyMatches:
    """Tests for fuzzy/partial matching via TF-IDF cosine similarity."""

    def test_fuzzy_helo(self):
        result = match_greeting("helo")
        assert result in GREETINGS.values(), "Fuzzy match should return a known response"

    def test_fuzzy_gooood_morning(self):
        result = match_greeting("gooood morning")
        assert result in GREETINGS.values() or result == DEFAULT_RESPONSE

    def test_fuzzy_howdy_partial(self):
        result = match_greeting("howd")
        assert result in GREETINGS.values() or result == DEFAULT_RESPONSE

    def test_fuzzy_hi_there_typo(self):
        result = match_greeting("hi ther")
        assert result in GREETINGS.values(), "Should fuzzy-match 'hi there'"


class TestEdgeCases:
    """Tests for edge cases and fallback behavior."""

    def test_empty_string_returns_empty(self):
        assert match_greeting("") == ""

    def test_whitespace_only_returns_empty(self):
        assert match_greeting("   ") == ""

    def test_tab_only_returns_empty(self):
        assert match_greeting("\t") == ""

    def test_newline_only_returns_empty(self):
        assert match_greeting("\n") == ""

    def test_unknown_input_returns_default(self):
        result = match_greeting("xyzzy plugh zork")
        assert result == DEFAULT_RESPONSE

    def test_numeric_input_returns_default(self):
        result = match_greeting("12345")
        assert result == DEFAULT_RESPONSE

    def test_special_characters_returns_default(self):
        result = match_greeting("!@#$%")
        assert result == DEFAULT_RESPONSE

    def test_very_long_unknown_input(self):
        result = match_greeting("a" * 500)
        assert result == DEFAULT_RESPONSE or result in GREETINGS.values()
