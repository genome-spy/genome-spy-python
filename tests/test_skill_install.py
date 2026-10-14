"""Opt-in installation preserves existing instructions and portable references."""

from pathlib import Path

import pytest

from genome_spy import _skill_install as installer


@pytest.fixture
def source(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    source = tmp_path / "source"
    (source / "references").mkdir(parents=True)
    (source / "SKILL.md").write_text("[Details](references/details.md)")
    (source / "references/details.md").write_text("Portable instructions")
    monkeypatch.setattr(installer, "_source", lambda: source)
    return source


def destination(base: Path, agent: str) -> Path:
    root = ".agents" if agent == "codex" else ".claude"
    return base / root / "skills" / "create-genomespy-visualization"


def test_installs_complete_tree_for_both_agents(source: Path, tmp_path: Path) -> None:
    project = tmp_path / "project"
    assert installer.main(["--project", str(project)]) == 0
    for agent in ("codex", "claude"):
        dest = destination(project, agent)
        assert (dest / "SKILL.md").read_bytes() == (source / "SKILL.md").read_bytes()
        assert (dest / "references/details.md").read_bytes() == (
            source / "references/details.md"
        ).read_bytes()
        assert not dest.is_symlink()


def test_unchanged_reinstall_does_not_write(source: Path, tmp_path: Path) -> None:
    project = tmp_path / "project"
    args = ["--project", str(project), "--agent", "codex"]
    assert installer.main(args) == 0
    file = destination(project, "codex") / "SKILL.md"
    before = file.stat().st_mtime_ns
    assert installer.main(args) == 0
    assert file.stat().st_mtime_ns == before
    assert not destination(project, "claude").exists()


def test_conflict_preflight_leaves_both_destinations_untouched(
    source: Path, tmp_path: Path
) -> None:
    project = tmp_path / "project"
    dest = destination(project, "claude")
    dest.mkdir(parents=True)
    (dest / "SKILL.md").write_text("Custom instructions")
    assert installer.main(["--project", str(project)]) == 1
    assert (dest / "SKILL.md").read_text() == "Custom instructions"
    assert not destination(project, "codex").exists()


def test_force_replaces_entire_tree(source: Path, tmp_path: Path) -> None:
    project = tmp_path / "project"
    args = ["--project", str(project), "--agent", "claude"]
    assert installer.main(args) == 0
    dest = destination(project, "claude")
    (dest / "references/details.md").write_text("Edited locally")
    (dest / "obsolete.md").write_text("Old version")
    assert installer.main(args) == 1
    assert (dest / "obsolete.md").exists()
    assert installer.main([*args, "--force"]) == 0
    assert not (dest / "obsolete.md").exists()
    assert (dest / "references/details.md").read_text() == "Portable instructions"


def test_user_scope_and_print_path_do_not_touch_project(
    source: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    personal = tmp_path / "home"
    project = tmp_path / "project"
    project.mkdir()
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: personal))
    monkeypatch.chdir(project)
    assert installer.main(["--print-path"]) == 0
    assert not personal.exists() and not list(project.iterdir())
    assert installer.main(["--user", "--agent", "codex"]) == 0
    assert (destination(personal, "codex") / "SKILL.md").exists()
    assert not list(project.iterdir())


def test_force_refuses_symlink_destination(source: Path, tmp_path: Path) -> None:
    dest = destination(tmp_path, "codex")
    dest.parent.mkdir(parents=True)
    dest.symlink_to(source, target_is_directory=True)
    assert (
        installer.main(["--project", str(tmp_path), "--agent", "codex", "--force"]) == 1
    )
    assert dest.is_symlink() and (source / "SKILL.md").exists()


def test_failed_replacement_restores_previous_skill(
    source: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    args = ["--project", str(tmp_path), "--agent", "codex"]
    assert installer.main(args) == 0
    dest = destination(tmp_path, "codex")
    (dest / "SKILL.md").write_text("Keep this")
    original = Path.rename

    def fail_staging(path: Path, target: Path) -> Path:
        if path.name == "skill":
            raise OSError("simulated rename failure")
        return original(path, target)

    monkeypatch.setattr(Path, "rename", fail_staging)
    assert installer.main([*args, "--force"]) == 1
    assert (dest / "SKILL.md").read_text() == "Keep this"


def test_real_skill_includes_all_linked_references() -> None:
    import re

    contents = installer._contents(installer._source())
    assert Path("SKILL.md") in contents
    assert Path("agents/openai.yaml") in contents
    for path, content in contents.items():
        if path.suffix != ".md":
            continue
        for link in re.findall(r"\]\(([^)]+)\)", content.decode()):
            if "://" not in link and not link.startswith("#"):
                target = path.parent / link.split("#")[0]
                assert target in contents, (path, link)
