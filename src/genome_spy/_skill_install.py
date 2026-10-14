"""Opt-in installation of packaged agent instructions; no import side effects."""

from __future__ import annotations

import argparse
from importlib.resources import files
from importlib.resources.abc import Traversable
from pathlib import Path
import sys
from tempfile import TemporaryDirectory

__all__ = ["main"]

_SKILL_NAME = "create-genomespy-visualization"
_ROOTS = {"codex": Path(".agents/skills"), "claude": Path(".claude/skills")}


class SkillInstallError(RuntimeError):
    """An installation cannot proceed without changing the requested operation."""


def _source() -> Traversable:
    bundled = files("genome_spy").joinpath("skills", _SKILL_NAME)
    if bundled.joinpath("SKILL.md").is_file():
        return bundled
    # Editable installs use the single canonical source, not a maintained copy.
    checkout = Path(__file__).resolve().parents[2]
    source = checkout / "skills" / _SKILL_NAME
    if (checkout / "pyproject.toml").is_file() and (source / "SKILL.md").is_file():
        return source
    raise SkillInstallError("Bundled skill is missing; reinstall genome-spy-python.")


def _contents(source: Traversable, prefix: Path = Path()) -> dict[Path, bytes]:
    result: dict[Path, bytes] = {}
    for child in sorted(source.iterdir(), key=lambda entry: entry.name):
        relative = prefix / child.name
        if child.is_dir():
            result.update(_contents(child, relative))
        else:
            result[relative] = child.read_bytes()
    return result


def _matches(destination: Path, contents: dict[Path, bytes]) -> bool:
    if not destination.is_dir() or destination.is_symlink():
        return False
    entries = list(destination.rglob("*"))
    if any(entry.is_symlink() for entry in entries):
        return False
    return {
        entry.relative_to(destination): entry.read_bytes()
        for entry in entries
        if entry.is_file()
    } == contents


def _install(
    destinations: list[Path], contents: dict[Path, bytes], force: bool
) -> None:
    # Preflight every requested agent before writing any skill.
    pending = []
    for destination in destinations:
        if destination.is_symlink():
            raise SkillInstallError(f"Refusing symlink destination: {destination}")
        if _matches(destination, contents):
            continue
        if destination.exists():
            if not destination.is_dir():
                raise SkillInstallError(
                    f"Destination is not a directory: {destination}"
                )
            if not force:
                raise SkillInstallError(
                    f"Existing skill differs: {destination}. Use --force to replace it."
                )
        pending.append(destination)
    for destination in pending:
        destination.parent.mkdir(parents=True, exist_ok=True)
        with TemporaryDirectory(
            prefix=".genomespy-skill-", dir=destination.parent
        ) as work:
            staging = Path(work) / "skill"
            staging.mkdir()
            for relative, content in contents.items():
                target = staging / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(content)
            backup = Path(work) / "previous"
            if destination.exists():
                destination.rename(backup)
            try:
                staging.rename(destination)
            except OSError:
                if backup.exists():
                    backup.rename(destination)
                raise
    for destination in destinations:
        sys.stdout.write(
            f"{'Installed' if destination in pending else 'Unchanged'} {destination}\n"
        )


def main(argv: list[str] | None = None) -> int:
    """Install the visualization skill for Codex and/or Claude Code.

    Copies packaged instructions only on explicit invocation. Modified existing
    skills require ``--force``; identical installations are left untouched.

    Args:
        argv: Command-line arguments, or None to read the process arguments.

    Returns:
        Zero on success, one for an installation error.

    Raises:
        SystemExit: Argument parsing fails or help is requested.

    Example:
        >>> main(["--print-path"])  # doctest: +SKIP
        0
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--agent", choices=["codex", "claude", "both"], default="both")
    scope = parser.add_mutually_exclusive_group()
    scope.add_argument(
        "--project", type=Path, help="Project root (default: current directory)"
    )
    scope.add_argument(
        "--user", action="store_true", help="Install into personal skill roots"
    )
    parser.add_argument(
        "--force", action="store_true", help="Replace a modified skill directory"
    )
    parser.add_argument(
        "--print-path", action="store_true", help="Show source without installing"
    )
    args = parser.parse_args(argv)
    try:
        source = _source()
        if args.print_path:
            sys.stdout.write(f"{source}\n")
            return 0
        base = Path.home() if args.user else (args.project or Path.cwd())
        agents = list(_ROOTS) if args.agent == "both" else [args.agent]
        destinations = [
            base.expanduser().resolve() / _ROOTS[agent] / _SKILL_NAME
            for agent in agents
        ]
        _install(destinations, _contents(source), args.force)
    except (OSError, SkillInstallError) as exc:
        sys.stderr.write(f"Skill installation failed: {exc}\n")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
