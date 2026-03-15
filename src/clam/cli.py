"""clam — CLI Agent for Mac."""

from __future__ import annotations

import sys

import click

from clam.i18n import get_lang, save_lang, set_lang, t
from clam.output import console, error, output, status, success
from clam.registry import registry
from clam.scanner.app_scanner import find_app, find_basic_app, scan_applications, suggest_app
from clam.scanner.sdef_parser import parse_sdef
from clam.generator.applescript_gen import (
    check_command_support,
    generate_basic_wrapper, generate_ui_wrapper, generate_wrapper,
    get_ui_wrapper_info, get_wrapper_info,
)
from clam.scanner.menu_scanner import scan_menus
from clam.generator.installer import install_wrapper, uninstall_wrapper


# ── App descriptions ────────────────────────────────────────────────────────
# app_id → (emoji, category_key, description_key)
_APP_DESCRIPTIONS: dict[str, tuple[str, str, str]] = {
    # Media
    "music":              ("🎵", "cat.media", "app.desc.music"),
    "tv":                 ("📺", "cat.media", "app.desc.tv"),
    "quicktime-player":   ("🎬", "cat.media", "app.desc.quicktime-player"),
    "garageband":         ("🎸", "cat.media", "app.desc.garageband"),
    "photos":             ("📷", "cat.media", "app.desc.photos"),
    "spotify":            ("🎵", "cat.media", "app.desc.spotify"),
    "qqmusic":            ("🎵", "cat.media", "app.desc.qqmusic"),
    # Browser
    "google-chrome":      ("🌐", "cat.browser", "app.desc.google-chrome"),
    "safari":             ("🌐", "cat.browser", "app.desc.safari"),
    "arc":                ("🌐", "cat.browser", "app.desc.arc"),
    "doubao":             ("🌐", "cat.browser", "app.desc.doubao"),
    # Office
    "microsoft-word":     ("📝", "cat.office", "app.desc.microsoft-word"),
    "microsoft-excel":    ("📊", "cat.office", "app.desc.microsoft-excel"),
    "microsoft-powerpoint": ("📊", "cat.office", "app.desc.microsoft-powerpoint"),
    "microsoft-outlook":  ("📧", "cat.office", "app.desc.microsoft-outlook"),
    "keynote":            ("📊", "cat.office", "app.desc.keynote"),
    "pages":              ("📝", "cat.office", "app.desc.pages"),
    "numbers":            ("📊", "cat.office", "app.desc.numbers"),
    "notion":             ("📝", "cat.office", "app.desc.notion"),
    "obsidian":           ("📝", "cat.office", "app.desc.obsidian"),
    # Productivity
    "mail":               ("📧", "cat.productivity", "app.desc.mail"),
    "calendar":           ("📅", "cat.productivity", "app.desc.calendar"),
    "contacts":           ("👤", "cat.productivity", "app.desc.contacts"),
    "messages":           ("💬", "cat.productivity", "app.desc.messages"),
    "notes":              ("📝", "cat.productivity", "app.desc.notes"),
    "reminders":          ("✅", "cat.productivity", "app.desc.reminders"),
    "ticktick":           ("✅", "cat.productivity", "app.desc.ticktick"),
    # Communication
    "telegram":           ("💬", "cat.communication", "app.desc.telegram"),
    "wechat":             ("💬", "cat.communication", "app.desc.wechat"),
    "qq":                 ("💬", "cat.communication", "app.desc.qq"),
    "dingtalk":           ("💬", "cat.communication", "app.desc.dingtalk"),
    "lark":               ("💬", "cat.communication", "app.desc.lark"),
    "discord":            ("💬", "cat.communication", "app.desc.discord"),
    "slack":              ("💬", "cat.communication", "app.desc.slack"),
    "zoom":               ("📹", "cat.communication", "app.desc.zoom"),
    # Design
    "figma":              ("🎨", "cat.design", "app.desc.figma"),
    # Development
    "xcode":              ("🔨", "cat.development", "app.desc.xcode"),
    "visual-studio-code": ("💻", "cat.development", "app.desc.visual-studio-code"),
    "cursor":             ("💻", "cat.development", "app.desc.cursor"),
    # System
    "finder":             ("📂", "cat.system", "app.desc.finder"),
    "terminal":           ("💻", "cat.system", "app.desc.terminal"),
    "system-settings":    ("🔧", "cat.system", "app.desc.system-settings"),
    "shortcuts":          ("🔗", "cat.system", "app.desc.shortcuts"),
    # Tools
    "amphetamine":        ("🔋", "cat.tools", "app.desc.amphetamine"),
    "flow":               ("🕐", "cat.tools", "app.desc.flow"),
    "the-unarchiver":     ("📦", "cat.tools", "app.desc.the-unarchiver"),
    "bluetooth-file-exchange": ("📡", "cat.tools", "app.desc.bluetooth-file-exchange"),
    "screen-sharing":     ("🖥️", "cat.tools", "app.desc.screen-sharing"),
    "console":            ("🔍", "cat.tools", "app.desc.console"),
    "clashx-pro":         ("🌐", "cat.tools", "app.desc.clashx-pro"),
    "chatgpt-atlas":      ("🤖", "cat.tools", "app.desc.chatgpt-atlas"),
}

# macOS internal components, hidden from scan results
_HIDDEN_APPS: set[str] = {
    "applescript-utility",
    "folder-actions-dispatcher",
    "folderactionsdispatcher",
    "image-events",
    "shortcuts-events",
    "system-events",
    "voiceover",
}

# Category display order (by key)
_CAT_ORDER = [
    "cat.office", "cat.design", "cat.media", "cat.browser",
    "cat.communication", "cat.productivity", "cat.development",
    "cat.system", "cat.tools", "cat.other",
]


def _auto_describe(cmd_names: list[str]) -> str:
    """Auto-generate capability description from command names."""
    caps: list[str] = []
    names = {n.lower() for n in cmd_names}
    if names & {"play", "pause", "stop", "playpause", "resume"}:
        caps.append(t("cap.playback"))
    if names & {"next-track", "previous-track", "back-track"}:
        caps.append(t("cap.track_switch"))
    if names & {"reload", "go-back", "go-forward"}:
        caps.append(t("cap.navigation"))
    if names & {"send", "reply", "forward"}:
        caps.append(t("cap.messaging"))
    if names & {"search", "find"}:
        caps.append(t("cap.search"))
    if names & {"export", "import"}:
        caps.append(t("cap.import_export"))
    if names & {"build", "run", "test"}:
        caps.append(t("cap.build_run"))
    if names & {"start", "stop", "reset"}:
        caps.append(t("cap.start_stop"))
    if not caps:
        caps.append(t("cap.scriptable"))
    return t("join.comma").join(caps[:4])


@click.group()
@click.option("--json", "use_json", is_flag=True, help=t("cli.help_json"))
@click.pass_context
def cli(ctx, use_json):
    """clam — CLI Agent for Mac"""
    ctx.ensure_object(dict)
    ctx.obj["json"] = use_json


@cli.command()
@click.pass_context
def scan(ctx):
    """Scan local scriptable apps / \u626b\u63cf\u672c\u5730\u53ef\u811a\u672c\u5316\u5e94\u7528"""
    json_mode = ctx.obj["json"]

    if not json_mode:
        status(f"\U0001f50d {t('scan.scanning')}")

    apps = scan_applications()

    results = []
    for app in apps:
        if app.app_id in _HIDDEN_APPS:
            continue
        if app.sdef_path:
            try:
                sdef_info = parse_sdef(app.sdef_path, app.name)
                wrapper_info = get_wrapper_info(sdef_info, app.app_id)
                results.append({
                    "name": app.name,
                    "app_id": app.app_id,
                    "sdef_path": app.sdef_path,
                    "commands": len(wrapper_info["commands"]),
                    "properties": len(wrapper_info["properties"]),
                    "nested_groups": len(wrapper_info["nested_groups"]),
                    "installed": app.installed,
                    "cmd_names": [c.cli_name for c in wrapper_info["commands"]],
                    "mode": "full",
                })
            except Exception:
                continue
        else:
            results.append({
                "name": app.name,
                "app_id": app.app_id,
                "sdef_path": "",
                "commands": 0,
                "properties": 0,
                "nested_groups": 0,
                "installed": app.installed,
                "cmd_names": [],
                "mode": "ui",
            })

    if json_mode:
        json_results = [{k: v for k, v in r.items() if k != "cmd_names"} for r in results]
        output(json_results, json_mode=True)
    else:
        if not results:
            console.print(t("scan.no_apps"))
            return

        console.print(
            f"\n\U0001f50d [bold]{t('scan.done')}[/bold] — "
            f"{t('scan.found', count=len(results))}"
        )

        from collections import defaultdict

        grouped: dict[str, list[dict]] = defaultdict(list)
        for r in results:
            entry = _APP_DESCRIPTIONS.get(r["app_id"])
            cat_key = entry[1] if entry else "cat.other"
            grouped[cat_key].append(r)

        sorted_cats = sorted(
            grouped.keys(),
            key=lambda c: _CAT_ORDER.index(c) if c in _CAT_ORDER else 99,
        )

        def _rich_label(r):
            entry = _APP_DESCRIPTIONS.get(r["app_id"])
            emoji = entry[0] if entry else "\U0001f4ce"
            return f"{emoji} {r['name']} [dim]({r['app_id']})[/dim]"

        idx = 1
        for cat_key in sorted_cats:
            console.rule(f"[bold]{t(cat_key)}[/bold]", style="dim")
            for r in grouped[cat_key]:
                entry = _APP_DESCRIPTIONS.get(r["app_id"])
                desc = t(entry[2]) if entry else _auto_describe(r["cmd_names"])
                rich = _rich_label(r)
                mark = " [green]\u2713[/green]" if r["installed"] else ""
                console.print(
                    f"  {idx:2d}.  {rich}  [dim]\u2014[/dim] {desc}{mark}"
                )
                idx += 1
            console.print()

        console.print(
            f"[dim]\U0001f4a1 {t('scan.hint')}[/dim]"
        )


def _app_not_found(app_name: str) -> None:
    """Output app-not-found error."""
    suggestions = suggest_app(app_name)
    if suggestions:
        error(t("err.app_not_found", name=app_name, suggestions=", ".join(suggestions)))
    else:
        error(t("err.app_not_found_generic", name=app_name))
    sys.exit(1)


@cli.command()
@click.argument("app_name")
@click.pass_context
def install(ctx, app_name):
    """Install CLI wrapper for an app / \u5b89\u88c5\u5e94\u7528\u7684 CLI wrapper"""
    json_mode = ctx.obj["json"]

    app = find_app(app_name)
    if not app:
        app = find_basic_app(app_name)
    if not app:
        _app_not_found(app_name)

    mode = "full"
    menu_scan = None
    if not app.sdef_path:
        if not json_mode:
            status(f"\U0001f50d {t('install.probing_menus', name=app.name)}")
        menu_scan = scan_menus(app.name, app.process_name or None)
        if menu_scan and menu_scan.total_items > 0:
            mode = "ui"
        else:
            mode = "basic"

    mode_label = t(f"install.mode.{mode}")
    if not json_mode:
        status(f"\U0001f4e6 {t('install.generating', name=app.name, mode=mode_label)}")

    wrapper_dir = registry.REGISTRY_DIR / "wrappers" / app.app_id

    if mode == "basic":
        try:
            generate_basic_wrapper(app.name, wrapper_dir, app_id=app.app_id)
        except Exception as e:
            error(t("install.gen_failed", error=e))
            sys.exit(1)
        cmd_count = 3
        prop_count = 3
    elif mode == "ui":
        try:
            generate_ui_wrapper(app.name, menu_scan.process_name, menu_scan, wrapper_dir, app_id=app.app_id)
        except Exception as e:
            error(t("install.gen_failed", error=e))
            sys.exit(1)
        ui_info = get_ui_wrapper_info(menu_scan)
        cmd_count = ui_info["menu_cmd_count"] + 3
        prop_count = 3
    else:
        try:
            sdef_info = parse_sdef(app.sdef_path, app.name)
        except Exception as e:
            error(t("install.sdef_failed", error=e))
            sys.exit(1)
        try:
            generate_wrapper(sdef_info, wrapper_dir, app_id=app.app_id)
        except Exception as e:
            error(t("install.gen_failed", error=e))
            sys.exit(1)
        wrapper_info = get_wrapper_info(sdef_info, app.app_id)
        cmd_count = len(wrapper_info["commands"])
        prop_count = len(wrapper_info["properties"])

    if not json_mode:
        status(f"\U0001f4e6 {t('install.installing', app_id=app.app_id)}")

    if not install_wrapper(app.app_id, wrapper_dir):
        error(t("install.pip_failed"))
        sys.exit(1)

    registry.register(
        app_id=app.app_id,
        app_name=app.name,
        sdef_path=app.sdef_path,
        wrapper_dir=str(wrapper_dir),
        command_count=cmd_count,
        property_count=prop_count,
    )

    if json_mode:
        output({
            "app_id": app.app_id,
            "entry_point": f"clam-{app.app_id}",
            "commands": cmd_count,
            "properties": prop_count,
            "mode": mode,
        }, json_mode=True)
    else:
        ep = f"clam-{app.app_id}"
        if mode == "basic":
            success(t("install.success_basic", name=app.name, ep=ep))
            console.print(f"   {t('install.cmd_prop', cmds=cmd_count, props=prop_count)}")
            console.print(f"\n   [dim]{t('install.quickstart')}[/dim]")
            console.print(f"   [dim]  $ {ep} activate       {t('install.activate_hint')}[/dim]")
            console.print(f"   [dim]  $ {ep} get-version    {t('install.version_hint')}[/dim]")
            console.print(f"   [dim]  $ {ep} quit-app       {t('install.quit_hint')}[/dim]")
        elif mode == "ui":
            ui_info = get_ui_wrapper_info(menu_scan)
            success(t("install.success_ui", name=app.name, ep=ep))
            console.print(f"   {t('install.menu_cmd', menus=ui_info['menu_cmd_count'])}")
            console.print(f"\n   [dim]{t('install.quickstart')}[/dim]")
            for g in ui_info["menu_groups"][:2]:
                if g.items:
                    item = g.items[0]
                    console.print(f"   [dim]  $ {ep} {item.cli_name:<20}{item.name}[/dim]")
            console.print(f"   [dim]  $ {ep} activate            {t('install.activate_hint')}[/dim]")
        else:
            nested_count = len(wrapper_info["nested_groups"])
            nested_str = t("install.nested_count", count=nested_count) if nested_count else ""
            success(t("install.success_full", name=app.name, ep=ep))
            console.print(f"   {t('install.cmd_prop', cmds=cmd_count, props=prop_count)}{nested_str}")

            example_cmds = []
            if wrapper_info["properties"]:
                first_prop = wrapper_info["properties"][0]
                example_cmds.append(f"{ep} get-{first_prop.cli_name}")
            if wrapper_info["commands"]:
                first_cmd = wrapper_info["commands"][0]
                example_cmds.append(f"{ep} {first_cmd.cli_name}")
            if wrapper_info["nested_groups"]:
                first_group = wrapper_info["nested_groups"][0]
                example_cmds.append(f"{ep} get-{first_group.cli_name}")

            console.print(f"\n   [dim]{t('install.quickstart')}[/dim]")
            for ex in example_cmds[:3]:
                console.print(f"   [dim]  $ {ex}[/dim]")

        console.print(f"   [dim]  $ {ep}         {t('install.view_summary')}[/dim]")
        console.print(f"   [dim]  $ {ep} api     {t('install.view_api')}[/dim]")
        console.print()
        console.print(f"   [bold]{t('install.ai_title')}[/bold]")
        console.print(f"   {t('install.ai_configured', ep=ep)}")
        console.print(f"   {t('install.ai_guide', app_id=app.app_id)}")


@cli.command(name="list")
@click.pass_context
def list_cmd(ctx):
    """List installed wrappers / \u67e5\u770b\u5df2\u5b89\u88c5\u7684 wrapper"""
    json_mode = ctx.obj["json"]
    wrappers = registry.list_all()

    if json_mode:
        output(list(wrappers.values()), json_mode=True)
        return

    if not wrappers:
        console.print(t("list.empty"))
        return

    from rich.table import Table
    table = Table(
        title=t("list.title"),
        show_header=True,
        header_style="bold cyan",
    )
    table.add_column(t("list.col.app"), style="bold")
    table.add_column(t("list.col.entry"))
    table.add_column(t("list.col.commands"), justify="right")
    table.add_column(t("list.col.properties"), justify="right")
    table.add_column(t("list.col.installed_at"))

    for app_id, info in wrappers.items():
        table.add_row(
            info["app_name"],
            info["entry_point"],
            str(info["command_count"]),
            str(info["property_count"]),
            info["installed_at"][:10],
        )
    console.print(table)


@cli.command()
@click.argument("app_name")
@click.pass_context
def info(ctx, app_name):
    """View app commands and properties / \u67e5\u770b\u5e94\u7528\u7684\u547d\u4ee4\u548c\u5c5e\u6027\u6e05\u5355"""
    json_mode = ctx.obj["json"]

    app = find_app(app_name)
    if not app:
        _app_not_found(app_name)

    try:
        sdef_info = parse_sdef(app.sdef_path, app.name)
    except Exception as e:
        error(t("install.sdef_failed", error=e))
        sys.exit(1)

    wrapper_info = get_wrapper_info(sdef_info, app.app_id)
    commands = wrapper_info["commands"]
    properties = wrapper_info["properties"]
    nested_groups = wrapper_info["nested_groups"]

    support_results = check_command_support(sdef_info, app.app_id)
    support_map = {r["name"]: r["supported"] for r in support_results}

    if json_mode:
        output({
            "app_id": app.app_id,
            "app_name": app.name,
            "entry_point": f"clam-{app.app_id}",
            "commands": [
                {
                    "name": cmd.cli_name,
                    "description": cmd.description,
                    "has_direct_param": cmd.direct_param,
                    "supported": support_map.get(cmd.cli_name, True),
                    "params": [
                        {
                            "name": f"--{p.cli_name}",
                            "description": p.description,
                        }
                        for p in cmd.params
                    ],
                }
                for cmd in commands
            ],
            "properties": [
                {
                    "name": prop.cli_name,
                    "as_name": prop.as_name,
                    "access": prop.access,
                    "type": prop.value_type,
                    "get_command": f"get-{prop.cli_name}",
                    "set_command": (
                        f"set-{prop.cli_name}"
                        if prop.access == "rw" else None
                    ),
                }
                for prop in properties
            ],
            "nested_groups": [
                {
                    "name": group.cli_name,
                    "class": group.class_name,
                    "compound_command": f"get-{group.cli_name}",
                    "properties": [
                        {
                            "name": prop.cli_name,
                            "access": prop.access,
                            "type": prop.value_type,
                            "get_command": f"get-{group.cli_name}-{prop.cli_name}",
                            "set_command": (
                                f"set-{group.cli_name}-{prop.cli_name}"
                                if prop.access == "rw" else None
                            ),
                        }
                        for prop in group.properties
                    ],
                }
                for group in nested_groups
            ],
        }, json_mode=True)
    else:
        from rich.table import Table

        installed = registry.get(app.app_id)
        status_str = (
            f"[green]{t('info.installed')}[/green]" if installed
            else f"[dim]{t('info.not_installed')}[/dim]"
        )
        console.print(f"\n[bold]{app.name}[/bold]  {status_str}")
        console.print(f"  SDEF: [dim]{app.sdef_path}[/dim]")
        console.print(f"  {t('info.entry')} [bold]clam-{app.app_id}[/bold]")
        nested_info = (
            t("info.nested", count=len(nested_groups))
            if nested_groups else ""
        )
        console.print(
            f"  {t('info.cmd_prop', cmds=len(commands), props=len(properties))}"
            f"{nested_info}\n"
        )

        if commands:
            cmd_table = Table(
                title=t("info.tbl.commands"),
                show_header=True,
                header_style="bold",
            )
            cmd_table.add_column(t("info.tbl.name"), style="cyan")
            cmd_table.add_column(t("info.tbl.description"))
            cmd_table.add_column(t("info.tbl.params"))
            for cmd in commands:
                params_str = ""
                if cmd.direct_param:
                    params_str = (
                        "[ITEM] " if cmd.direct_optional else "ITEM "
                    )
                params_str += " ".join(
                    f"--{p.cli_name}" for p in cmd.params
                )
                cmd_table.add_row(
                    cmd.cli_name, cmd.description, params_str.strip(),
                )
            console.print(cmd_table)

        if properties:
            console.print()
            prop_table = Table(
                title=t("info.tbl.properties"),
                show_header=True,
                header_style="bold",
            )
            prop_table.add_column(t("info.tbl.prop_name"), style="cyan")
            prop_table.add_column(t("info.tbl.access"), justify="center")
            prop_table.add_column(t("info.tbl.type"))
            prop_table.add_column(t("info.tbl.prop_desc"))
            for prop in properties:
                access_str = (
                    "[green]rw[/green]"
                    if prop.access == "rw" else "[dim]r[/dim]"
                )
                prop_table.add_row(
                    prop.cli_name, access_str,
                    prop.value_type, prop.description_short,
                )
            console.print(prop_table)

        for group in nested_groups:
            console.print()
            grp_table = Table(
                title=t("info.nested_title", name=group.as_name, class_name=group.class_name),
                show_header=True,
                header_style="bold",
            )
            grp_table.add_column(t("info.tbl.command"), style="cyan")
            grp_table.add_column(t("info.tbl.access"), justify="center")
            grp_table.add_column(t("info.tbl.type"))
            for prop in group.properties:
                access_str = (
                    "[green]rw[/green]"
                    if prop.access == "rw" else "[dim]r[/dim]"
                )
                grp_table.add_row(
                    f"get-{group.cli_name}-{prop.cli_name}",
                    access_str,
                    prop.value_type,
                )
            console.print(grp_table)
            console.print(
                f"  [dim]{t('info.compound_cmd', name=group.cli_name)}[/dim]"
            )


@cli.command()
@click.argument("app_name")
@click.pass_context
def doctor(ctx, app_name):
    """Check command reliability / \u68c0\u67e5\u547d\u4ee4\u53ef\u9760\u6027"""
    json_mode = ctx.obj["json"]

    app = find_app(app_name)
    if not app:
        _app_not_found(app_name)

    try:
        sdef_info = parse_sdef(app.sdef_path, app.name)
    except Exception as e:
        error(t("install.sdef_failed", error=e))
        sys.exit(1)

    results = check_command_support(sdef_info, app.app_id)
    supported = [r for r in results if r["supported"]]
    unsupported = [r for r in results if not r["supported"]]

    if json_mode:
        output({
            "app_id": app.app_id,
            "total": len(results),
            "supported": len(supported),
            "unsupported": len(unsupported),
            "commands": results,
        }, json_mode=True)
    else:
        console.print(f"\n[bold]{app.name}[/bold] {t('doctor.title', name='')}\n")
        console.print(
            f"  [green]{t('doctor.supported', n=len(supported), total=len(results))}[/green]"
        )
        if unsupported:
            console.print(
                f"  [yellow]{t('doctor.unsupported', n=len(unsupported))}[/yellow]\n"
            )
            for r in unsupported:
                issues = t("join.comma").join(r["issues"])
                console.print(f"    [yellow]\u26a0[/yellow] {r['name']} — {issues}")
        console.print()


@cli.command()
@click.argument("app_name")
@click.pass_context
def remove(ctx, app_name):
    """Uninstall CLI wrapper / \u5378\u8f7d CLI wrapper"""
    json_mode = ctx.obj["json"]

    needle = app_name.lower().strip()
    wrappers = registry.list_all()

    app_id = None
    for wid, winfo in wrappers.items():
        if wid == needle or winfo["app_name"].lower() == needle:
            app_id = wid
            break

    if not app_id:
        error(t("remove.not_found", name=app_name))
        sys.exit(1)

    if not json_mode:
        status(f"\U0001f5d1  {t('remove.removing', app_id=app_id)}")

    uninstall_wrapper(app_id)

    if json_mode:
        output({"removed": app_id}, json_mode=True)
    else:
        success(t("remove.success", app_id=app_id))


@cli.command()
@click.argument("language", required=False, type=click.Choice(["en", "zh"]))
def lang(language):
    """Set display language / \u8bbe\u7f6e\u663e\u793a\u8bed\u8a00"""
    if language is None:
        click.echo(t("lang.current", lang=get_lang()))
        return
    save_lang(language)
    set_lang(language)
    # Re-init to use new language for this message
    click.echo(t("lang.switched", lang=language))


@cli.command(name="mcp-setup")
@click.option("--remove", is_flag=True, help="Unregister MCP server")
def mcp_setup(remove):
    """Register clam MCP server for Claude Code / 注册 MCP 服务器"""
    import shutil
    import subprocess

    claude_bin = shutil.which("claude")
    if not claude_bin:
        error(t("mcp.no_claude"))
        sys.exit(1)

    if remove:
        result = subprocess.run(
            [claude_bin, "mcp", "remove", "-s", "user", "clam"],
            capture_output=True, text=True,
        )
        if result.returncode == 0:
            success(t("mcp.removed"))
        else:
            error(t("mcp.not_registered"))
        return

    # Check if already registered
    result = subprocess.run(
        [claude_bin, "mcp", "list"],
        capture_output=True, text=True,
    )
    if "clam" in result.stdout and "Connected" in result.stdout:
        success(t("mcp.already"))
        return

    # Find clam-mcp binary
    clam_mcp_bin = shutil.which("clam-mcp")
    if not clam_mcp_bin:
        error(t("mcp.failed", error="clam-mcp not found on PATH"))
        sys.exit(1)

    status(t("mcp.registering"))
    result = subprocess.run(
        [claude_bin, "mcp", "add", "-s", "user", "clam", "--", clam_mcp_bin],
        capture_output=True, text=True,
    )
    if result.returncode == 0:
        success(t("mcp.success"))
    else:
        msg = result.stderr.strip() or result.stdout.strip()
        error(t("mcp.failed", error=msg))
