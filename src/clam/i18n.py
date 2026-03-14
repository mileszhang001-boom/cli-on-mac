"""i18n — internationalization support for CLAM."""

from __future__ import annotations

import json
import locale
import os
from pathlib import Path

from clam.strings import en, zh

_LANGS: dict[str, dict[str, str]] = {"en": en.STRINGS, "zh": zh.STRINGS}
_current: str = "en"

CONFIG_PATH = Path.home() / ".clam" / "config.json"


def _detect_lang() -> str:
    """Detect language from env, config file, or system locale."""
    # 1. Environment variable (highest priority)
    env_lang = os.environ.get("CLAM_LANG")
    if env_lang in _LANGS:
        return env_lang

    # 2. Config file
    if CONFIG_PATH.exists():
        try:
            cfg = json.loads(CONFIG_PATH.read_text())
            if cfg.get("lang") in _LANGS:
                return cfg["lang"]
        except Exception:
            pass

    # 3. System locale auto-detect
    try:
        loc = locale.getdefaultlocale()[0] or ""
        if loc.startswith("zh"):
            return "zh"
    except Exception:
        pass

    return "en"


def init_lang() -> None:
    """Initialize language from env/config/locale. Called at module load."""
    global _current
    _current = _detect_lang()


def set_lang(lang: str) -> None:
    """Set the current language."""
    global _current
    if lang in _LANGS:
        _current = lang


def get_lang() -> str:
    """Get the current language code."""
    return _current


def save_lang(lang: str) -> None:
    """Persist language choice to ~/.clam/config.json."""
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    cfg: dict = {}
    if CONFIG_PATH.exists():
        try:
            cfg = json.loads(CONFIG_PATH.read_text())
        except Exception:
            pass
    cfg["lang"] = lang
    CONFIG_PATH.write_text(json.dumps(cfg, indent=2))


def t(key: str, **kwargs: object) -> str:
    """Translate a string key to the current language.

    Usage: t("scan.found", count=5) → "Found 5 controllable apps"
    """
    strings = _LANGS.get(_current, _LANGS["en"])
    text = strings.get(key, _LANGS["en"].get(key, key))
    return text.format(**kwargs) if kwargs else text


def get_template_i18n(**extra: str) -> dict[str, str]:
    """Get all tpl.* strings for Jinja2 template context.

    Returns a dict like {"summary_full": "...", "capabilities": "...", ...}
    with the tpl. prefix stripped.
    """
    prefix = "tpl."
    strings = _LANGS.get(_current, _LANGS["en"])
    result = {
        k[len(prefix):]: v
        for k, v in strings.items()
        if k.startswith(prefix)
    }
    result.update(extra)
    return result


# Auto-initialize on import
init_lang()
