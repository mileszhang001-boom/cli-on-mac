"""Tests for i18n infrastructure."""

import os

import pytest

from clam.i18n import get_lang, init_lang, set_lang, t
from clam.strings import en, zh


class TestStringCompleteness:
    """Verify en and zh string files have identical key sets."""

    def test_same_keys(self):
        en_keys = set(en.STRINGS.keys())
        zh_keys = set(zh.STRINGS.keys())
        missing_in_zh = en_keys - zh_keys
        missing_in_en = zh_keys - en_keys
        assert not missing_in_zh, f"Keys in en but not zh: {missing_in_zh}"
        assert not missing_in_en, f"Keys in zh but not en: {missing_in_en}"

    def test_no_empty_values(self):
        for key, val in en.STRINGS.items():
            # Some keys are intentionally empty (e.g. install.mode.full)
            if key == "install.mode.full":
                continue
            assert val, f"Empty value in en.py: {key}"
        for key, val in zh.STRINGS.items():
            if key == "install.mode.full":
                continue
            assert val, f"Empty value in zh.py: {key}"


class TestTranslation:
    def test_t_returns_english_by_default(self):
        set_lang("en")
        assert t("scan.done") == "Scan complete"

    def test_t_returns_chinese(self):
        set_lang("zh")
        assert t("scan.done") == "扫描完成"
        set_lang("en")  # reset

    def test_t_with_kwargs(self):
        set_lang("en")
        result = t("scan.found", count=42)
        assert "42" in result
        assert "controllable" in result

    def test_t_with_kwargs_zh(self):
        set_lang("zh")
        result = t("scan.found", count=42)
        assert "42" in result
        assert "脚本化" in result
        set_lang("en")  # reset

    def test_t_unknown_key_returns_key(self):
        result = t("nonexistent.key.xyz")
        assert result == "nonexistent.key.xyz"

    def test_set_lang_invalid_ignored(self):
        set_lang("en")
        set_lang("fr")  # not supported
        assert get_lang() == "en"  # unchanged


class TestEnvOverride:
    def test_clam_lang_env(self):
        old = os.environ.get("CLAM_LANG")
        try:
            os.environ["CLAM_LANG"] = "zh"
            init_lang()
            assert get_lang() == "zh"
        finally:
            if old is not None:
                os.environ["CLAM_LANG"] = old
            else:
                os.environ.pop("CLAM_LANG", None)
            init_lang()  # restore


class TestTemplateStrings:
    """Verify template strings are properly structured."""

    def test_tpl_keys_exist(self):
        set_lang("en")
        assert t("tpl.capabilities") == "Core capabilities:"
        assert t("tpl.quickstart") == "Quick start:"

    def test_tpl_format_strings(self):
        set_lang("en")
        result = t("tpl.summary_full", app_id="music", app_name="Music")
        assert "clam-music" in result
        assert "Music" in result

    def test_tpl_zh_format_strings(self):
        set_lang("zh")
        result = t("tpl.summary_full", app_id="music", app_name="Music")
        assert "clam-music" in result
        set_lang("en")  # reset
