"""Tests for app_scanner — scan macOS apps (shared scan result)."""

import pytest

from clam.scanner.app_scanner import find_app, find_basic_app, scan_applications


@pytest.fixture(scope="module")
def scanned_apps():
    """Scan once per module, not per test."""
    return scan_applications()


class TestScanApplications:
    def test_scan_finds_music(self, scanned_apps):
        ids = {a.app_id for a in scanned_apps}
        assert "music" in ids

    def test_scan_finds_calendar(self, scanned_apps):
        ids = {a.app_id for a in scanned_apps}
        assert "calendar" in ids

    def test_scan_returns_sdef_paths(self, scanned_apps):
        for app in scanned_apps:
            # UI-scriptable apps have no sdef
            if not app.basic_mode:
                assert app.sdef_path.endswith(".sdef")

    def test_scan_returns_bundle_paths(self, scanned_apps):
        for app in scanned_apps:
            assert app.bundle_path.endswith(".app")


class TestFindApp:
    def test_find_by_id(self):
        app = find_app("music")
        assert app is not None
        assert app.name == "Music"

    def test_find_by_name(self):
        app = find_app("Music")
        assert app is not None
        assert app.app_id == "music"

    def test_find_case_insensitive(self):
        app = find_app("MUSIC")
        assert app is not None
        assert app.app_id == "music"

    def test_find_not_found(self):
        assert find_app("nonexistent_app_xyz_123") is None


class TestFinderAndFigma:
    """Tests for Finder (CoreServices .sdef) and Figma (known UI app) in scan."""

    def test_scan_finds_finder(self, scanned_apps):
        ids = {a.app_id for a in scanned_apps}
        assert "finder" in ids

    def test_finder_has_sdef(self, scanned_apps):
        finder = next(a for a in scanned_apps if a.app_id == "finder")
        assert finder.sdef_path.endswith(".sdef")
        assert not finder.basic_mode

    def test_scan_finds_figma(self, scanned_apps):
        ids = {a.app_id for a in scanned_apps}
        assert "figma" in ids

    def test_figma_is_basic_mode(self, scanned_apps):
        figma = next(a for a in scanned_apps if a.app_id == "figma")
        assert figma.basic_mode
        assert figma.sdef_path == ""

    def test_find_app_finder(self):
        app = find_app("finder")
        assert app is not None
        assert app.name == "Finder"

    def test_find_basic_app_figma(self):
        app = find_basic_app("figma")
        assert app is not None
        assert app.app_id == "figma"
