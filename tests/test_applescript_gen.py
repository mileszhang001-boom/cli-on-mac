"""Tests for applescript_gen — parameter injection, no allowlist, complex types."""

import tempfile
from pathlib import Path

from clam.generator.applescript_gen import (
    _should_include_command,
    generate_wrapper,
)


class TestNoAllowlist:
    def test_all_app_properties_generated(self, music_sdef_info):
        with tempfile.TemporaryDirectory() as d:
            generate_wrapper(music_sdef_info, Path(d))
            code = (Path(d) / "cli_music.py").read_text()
            assert "get_sound_volume" in code
            app_props = [p for p in music_sdef_info.properties
                         if p.class_name == "application" and not p.hidden]
            for prop in app_props:
                assert f"get_{prop.func_name}" in code, (
                    f"Missing getter for '{prop.name}'"
                )

    def test_no_track_section(self, music_sdef_info):
        with tempfile.TemporaryDirectory() as d:
            generate_wrapper(music_sdef_info, Path(d))
            code = (Path(d) / "cli_music.py").read_text()
            assert "track_prop_names" not in code
            assert "get-current-artist" not in code
            assert "get-current-album" not in code


class TestNamedParamInjection:
    def test_format_value_in_generated_code(self, calendar_sdef_info):
        with tempfile.TemporaryDirectory() as d:
            generate_wrapper(calendar_sdef_info, Path(d))
            code = (Path(d) / "cli_calendar.py").read_text()
            assert "_format_value" in code

    def test_switch_view_has_to_param(self, calendar_sdef_info):
        with tempfile.TemporaryDirectory() as d:
            generate_wrapper(calendar_sdef_info, Path(d))
            code = (Path(d) / "cli_calendar.py").read_text()
            assert '"to"' in code

    def test_dynamic_applescript_building(self, music_sdef_info):
        with tempfile.TemporaryDirectory() as d:
            generate_wrapper(music_sdef_info, Path(d))
            code = (Path(d) / "cli_music.py").read_text()
            assert 'parts = ["' in code
            assert '" ".join(parts)' in code


class TestNestedGroups:
    """Nested object property access (e.g. current track properties)."""

    def test_current_track_group_exists(self, music_sdef_info):
        from clam.generator.applescript_gen import get_wrapper_info
        wi = get_wrapper_info(music_sdef_info)
        group_names = {g.cli_name for g in wi["nested_groups"]}
        assert "current-track" in group_names

    def test_current_track_has_name_property(self, music_sdef_info):
        from clam.generator.applescript_gen import get_wrapper_info
        wi = get_wrapper_info(music_sdef_info)
        track_group = next(g for g in wi["nested_groups"] if g.cli_name == "current-track")
        prop_names = {p.cli_name for p in track_group.properties}
        assert "name" in prop_names
        assert "artist" in prop_names
        assert "album" in prop_names

    def test_nested_commands_in_generated_code(self, music_sdef_info):
        with tempfile.TemporaryDirectory() as d:
            generate_wrapper(music_sdef_info, Path(d))
            code = (Path(d) / "cli_music.py").read_text()
            assert "get-current-track-name" in code
            assert "get-current-track-artist" in code
            assert "get-current-track-album" in code

    def test_compound_command_returns_json(self, music_sdef_info):
        with tempfile.TemporaryDirectory() as d:
            generate_wrapper(music_sdef_info, Path(d))
            code = (Path(d) / "cli_music.py").read_text()
            assert 'name="get-current-track")' in code
            assert "json.dumps(data" in code

    def test_nested_set_commands_for_rw_properties(self, music_sdef_info):
        with tempfile.TemporaryDirectory() as d:
            generate_wrapper(music_sdef_info, Path(d))
            code = (Path(d) / "cli_music.py").read_text()
            # rating is rw on track
            assert "set-current-track-rating" in code

    def test_app_properties_exclude_nested_types(self, music_sdef_info):
        """Application properties that are class references should NOT appear
        as simple get-<prop> commands (they return unhelpful specifiers)."""
        from clam.generator.applescript_gen import get_wrapper_info
        wi = get_wrapper_info(music_sdef_info)
        simple_prop_names = {p.cli_name for p in wi["properties"]}
        # "current track" should NOT be a simple property
        assert "current-track" not in simple_prop_names
        # But "sound volume" should remain
        assert "sound-volume" in simple_prop_names


class TestCommandFiltering:
    def test_complex_type_commands_not_dropped(self, music_sdef_info):
        add_cmd = next(c for c in music_sdef_info.commands if c.name == "add")
        assert _should_include_command(add_cmd) is True

    def test_hidden_commands_still_dropped(self, calendar_sdef_info):
        hidden = [c for c in calendar_sdef_info.commands if c.hidden]
        for cmd in hidden:
            assert _should_include_command(cmd) is False

    def test_standard_suite_still_dropped(self, music_sdef_info):
        std = [c for c in music_sdef_info.commands if c.is_standard_suite]
        for cmd in std:
            assert _should_include_command(cmd) is False

    def test_search_command_now_included(self, music_sdef_info):
        search_cmd = next(
            (c for c in music_sdef_info.commands if c.name == "search"), None,
        )
        if search_cmd:
            assert _should_include_command(search_cmd) is True
