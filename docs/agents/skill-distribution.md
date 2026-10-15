# Install the visualization skill

Installation is opt-in: package installation and imports do not change agent
configuration. These commands require a package build containing the installer.

## Project or personal scope

```bash
# Both agents, current project.
genome-spy-install-skills

# Choose agent and destination.
genome-spy-install-skills --agent codex --project /path/to/project
genome-spy-install-skills --agent claude --user
genome-spy-install-skills --user --agent both
```

| Agent | Project root | Personal root |
| --- | --- | --- |
| Codex | `.agents/skills/` | `~/.agents/skills/` |
| Claude Code | `.claude/skills/` | `~/.claude/skills/` |

Each root receives `create-genomespy-visualization/`, including `SKILL.md`,
`agents/openai.yaml` and all references. Start a new agent session if it is not visible.

## Inspect or update

```bash
# Inspect the bundled source without installing.
genome-spy-install-skills --print-path

# After upgrading the package; save local skill edits before replacing.
genome-spy-install-skills --agent both --project /path/to/project --force
```

| Destination | Behavior |
| --- | --- |
| Identical contents | Unchanged; no rewrite. |
| Modified contents or extra files | Refused unless `--force`. |
| Symlink or file destination | Refused even with `--force`. |
| Multiple destinations | All checked for conflicts before copying. |
| Forced replacement | Replaces the entire folder, including local/obsolete files; restores the old folder if final rename fails. |

## Development checkout

```bash
uv run genome-spy-install-skills
uv run python -m genome_spy._skill_install
```

Canonical source: `skills/create-genomespy-visualization/`. Wheels bundle it under
`genome_spy/skills/create-genomespy-visualization/`; source distributions include
the source and build mapping. Editable installs fall back to the canonical folder
when no bundled resource exists. Installed copies are not editable sources.

The installer does not install plugins or configure cloud agents. See
[Codex skill locations](https://learn.chatgpt.com/docs/build-skills) and
[Claude Code skill locations](https://code.claude.com/docs/en/skills).

Agent Markdown and `llms.txt` publish with successful documentation builds;
live deployment follows the release/manual-dispatch policy. A local build does
not prove public availability. See [the index](https://genomespy.app/genome-spy-python/llms.txt).
