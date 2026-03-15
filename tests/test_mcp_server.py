"""Tests for CLAM MCP Server — tool registration and handler logic."""

import json

from clam.mcp_server import (
    clam_doctor,
    clam_find_app,
    clam_info,
    clam_scan,
)


class TestToolRegistration:
    def test_all_tools_registered(self):
        from clam.mcp_server import mcp
        tools = mcp._tool_manager._tools
        expected = {"clam_scan", "clam_info", "clam_install", "clam_execute", "clam_doctor", "clam_find_app"}
        assert set(tools.keys()) == expected

    def test_tool_count(self):
        from clam.mcp_server import mcp
        assert len(mcp._tool_manager._tools) == 6


class TestScanTool:
    def test_scan_returns_valid_json(self):
        result = clam_scan()
        data = json.loads(result)
        assert isinstance(data, list)
        assert len(data) > 0

    def test_scan_has_music(self):
        result = clam_scan()
        data = json.loads(result)
        ids = {app["app_id"] for app in data}
        assert "music" in ids

    def test_scan_fields(self):
        result = clam_scan()
        data = json.loads(result)
        first = data[0]
        assert "name" in first
        assert "app_id" in first
        assert "commands" in first
        assert "mode" in first
        assert "installed" in first


class TestInfoTool:
    def test_info_music(self):
        result = clam_info("music")
        data = json.loads(result)
        assert data["app_name"] == "Music"
        assert data["app_id"] == "music"
        assert len(data["commands"]) > 0
        assert len(data["properties"]) > 0

    def test_info_has_supported_field(self):
        result = clam_info("music")
        data = json.loads(result)
        for cmd in data["commands"]:
            assert "supported" in cmd

    def test_info_has_nested_groups(self):
        result = clam_info("music")
        data = json.loads(result)
        assert "nested_groups" in data
        group_names = {g["name"] for g in data["nested_groups"]}
        assert "current-track" in group_names

    def test_info_not_found(self):
        result = clam_info("nonexistent_xyz_abc")
        data = json.loads(result)
        assert "error" in data

    def test_info_fuzzy_match(self):
        result = clam_info("chrome")
        data = json.loads(result)
        # Should match google-chrome if installed, or return error
        assert "app_id" in data or "error" in data


class TestDoctorTool:
    def test_doctor_music(self):
        result = clam_doctor("music")
        data = json.loads(result)
        assert data["app_id"] == "music"
        assert data["total"] > 0
        assert data["supported"] + data["unsupported"] == data["total"]

    def test_doctor_not_found(self):
        result = clam_doctor("nonexistent_xyz_abc")
        data = json.loads(result)
        assert "error" in data


class TestExecuteTool:
    def test_execute_not_installed(self):
        from clam.mcp_server import clam_execute
        result = clam_execute("nonexistent_xyz_abc", "play")
        data = json.loads(result)
        assert "error" in data
        assert "未安装" in data["error"]


class TestFindAppTool:
    def test_find_app_music_english(self):
        result = clam_find_app("music")
        data = json.loads(result)
        assert data["found"] is True
        assert data["best_match"]["app_id"] == "music"

    def test_find_app_qqmusic_chinese(self):
        result = clam_find_app("QQ音乐")
        data = json.loads(result)
        assert data["found"] is True
        assert data["best_match"]["app_id"] == "qqmusic"

    def test_find_app_wechat_chinese(self):
        result = clam_find_app("微信")
        data = json.loads(result)
        assert data["found"] is True
        assert data["best_match"]["app_id"] == "wechat"

    def test_find_app_chrome_fuzzy(self):
        result = clam_find_app("chrome")
        data = json.loads(result)
        assert data["found"] is True
        assert data["best_match"]["app_id"] == "google-chrome"

    def test_find_app_calendar_chinese(self):
        result = clam_find_app("日历")
        data = json.loads(result)
        assert data["found"] is True
        assert data["best_match"]["app_id"] == "calendar"

    def test_find_app_not_found_returns_suggestions(self):
        result = clam_find_app("xyzzy_nonexistent_9999")
        data = json.loads(result)
        assert data["found"] is False
        assert "suggestions" in data

    def test_find_app_installed_flag_is_bool(self):
        result = clam_find_app("music")
        data = json.loads(result)
        assert isinstance(data["best_match"]["installed"], bool)

    def test_find_app_has_workflow(self):
        result = clam_find_app("spotify")
        data = json.loads(result)
        assert data["found"] is True
        assert "workflow" in data
        assert "clam_execute" in data["workflow"] or "clam_install" in data["workflow"]

    def test_find_app_present_on_mac_flag(self):
        # Music.app is always present on macOS
        result = clam_find_app("music")
        data = json.loads(result)
        assert isinstance(data["best_match"]["present_on_mac"], bool)
